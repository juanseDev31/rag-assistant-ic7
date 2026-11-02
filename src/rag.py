"""
Núcleo RAG: embeddings, vector store simple, retrieval y generación.

Diseño: para corpus pequeños-medianos (< 10k chunks), un vector store
basado en numpy es suficientemente rápido y evita dependencias con
compilación nativa (chroma-hnswlib, faiss). La API es análoga a ChromaDB
para facilitar un cambio futuro sin tocar el pipeline.

El LLM se abstrae mediante `llm_providers.LLMProvider`, permitiendo
intercambiar entre Groq, Gemini y futuros proveedores sin tocar el pipeline.
"""
import logging
import pickle
from pathlib import Path
from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

import config
from llm_providers import LLMProvider
from loader import chunk_text, load_documents

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """Eres un asistente documental de la empresa. Tu única fuente de \
verdad es el CONTEXTO proporcionado abajo. Responde en español, de forma clara y \
concisa.

REGLAS ESTRICTAS:
1. Si la información requerida NO está en el contexto, responde exactamente:
   "No tengo esa información en los documentos consultados."
2. Nunca inventes datos, nombres, fechas o cifras. Nunca alucines.
3. Si la pregunta solo se responde PARCIALMENTE con el contexto, aclara \
   explícitamente qué parte sí sabes y qué parte no.
4. Cita las fuentes al final de la respuesta en el formato:
   📎 Fuentes: [nombre_archivo_1], [nombre_archivo_2]
5. No agregues información que no esté explícitamente en el contexto, aunque \
   la sepas por conocimiento general.
"""


class SimpleVectorStore:
    """Vector store minimalista basado en numpy, con persistencia a disco.

    - Guarda embeddings como numpy array normalizado (para coseno rápido).
    - Guarda documentos y metadata como listas Python.
    - Persistencia con pickle (archivo único).
    - API inspirada en ChromaDB: add() / query() / count().

    Para 30-10.000 chunks el rendimiento es más que suficiente.
    """

    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.embeddings: np.ndarray = np.empty((0, 0), dtype=np.float32)
        self.documents: List[str] = []
        self.metadatas: List[dict] = []
        self.ids: List[str] = []

    def count(self) -> int:
        return len(self.documents)

    def add(
        self,
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[dict],
        ids: List[str],
    ) -> None:
        emb = np.array(embeddings, dtype=np.float32)
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1e-10, norms)
        emb = emb / norms

        if self.embeddings.size == 0:
            self.embeddings = emb
        else:
            self.embeddings = np.vstack([self.embeddings, emb])

        self.documents.extend(documents)
        self.metadatas.extend(metadatas)
        self.ids.extend(ids)
        self._save()

    def query(
        self, query_embedding: List[float], n_results: int = 3
    ) -> dict:
        """Devuelve los n_results más similares por coseno, formato Chroma-like."""
        if self.count() == 0:
            return {
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]],
                "ids": [[]],
            }

        q = np.array(query_embedding, dtype=np.float32)
        q = q / (np.linalg.norm(q) + 1e-10)

        scores = self.embeddings @ q
        k = min(n_results, len(scores))
        top_idx = np.argsort(scores)[::-1][:k]

        return {
            "documents": [[self.documents[i] for i in top_idx]],
            "metadatas": [[self.metadatas[i] for i in top_idx]],
            "distances": [[float(1.0 - scores[i]) for i in top_idx]],
            "ids": [[self.ids[i] for i in top_idx]],
        }

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "wb") as f:
            pickle.dump(
                {
                    "embeddings": self.embeddings,
                    "documents": self.documents,
                    "metadatas": self.metadatas,
                    "ids": self.ids,
                },
                f,
            )

    def load(self) -> bool:
        if not self.path.exists():
            return False
        try:
            with open(self.path, "rb") as f:
                data = pickle.load(f)
            self.embeddings = data["embeddings"]
            self.documents = data["documents"]
            self.metadatas = data["metadatas"]
            self.ids = data["ids"]
            logger.info(
                f"Vector store cargado desde {self.path}: "
                f"{self.count()} chunks."
            )
            return True
        except Exception as e:
            logger.error(f"Error cargando vector store: {e}")
            return False


class RAGAssistant:
    """Orquesta el pipeline RAG completo.

    El LLM NO vive dentro del asistente; se pasa como argumento en cada
    query. Esto permite al usuario cambiar de provider desde la UI sin
    reconstruir el pipeline (que es caro: cargar el modelo de embeddings
    toma ~30 segundos).
    """

    def __init__(self) -> None:
        logger.info(f"Cargando modelo de embeddings: {config.EMBEDDING_MODEL}")
        self.embedder = SentenceTransformer(config.EMBEDDING_MODEL)

        logger.info(f"Inicializando vector store en: {config.VECTORSTORE_PATH}")
        self.store = SimpleVectorStore(config.VECTORSTORE_PATH)
        self.store.load()

    # Expone .collection para compatibilidad con la UI (count())
    @property
    def collection(self) -> SimpleVectorStore:
        return self.store

    # -------------------- Indexación --------------------
    def load_and_index_documents(self, docs_dir: str) -> int:
        existing = self.store.count()
        if existing > 0:
            logger.info(
                f"La colección ya tiene {existing} chunks. Omitiendo reindexado."
            )
            return existing

        documents = load_documents(docs_dir)
        if not documents:
            raise ValueError(f"No se encontraron documentos en {docs_dir}")

        all_chunks: List[str] = []
        all_metadata: List[dict] = []
        all_ids: List[str] = []

        for doc_name, content in documents.items():
            chunks = chunk_text(content, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_metadata.append({"source": doc_name, "chunk_id": i})
                all_ids.append(f"{doc_name}__chunk_{i}")

        logger.info(
            f"Generando embeddings para {len(all_chunks)} chunks "
            f"de {len(documents)} documentos..."
        )
        embeddings = self.embedder.encode(
            all_chunks, show_progress_bar=False
        ).tolist()

        self.store.add(
            embeddings=embeddings,
            documents=all_chunks,
            metadatas=all_metadata,
            ids=all_ids,
        )
        logger.info(f"Indexados {len(all_chunks)} chunks exitosamente.")
        return len(all_chunks)

    # -------------------- Recuperación --------------------
    def retrieve(self, query: str, k: int = None) -> List[dict]:
        if k is None:
            k = config.TOP_K

        query_embedding = self.embedder.encode(query).tolist()
        results = self.store.query(
            query_embedding=query_embedding,
            n_results=k,
        )

        sources: List[dict] = []
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        dists = results["distances"][0]

        for i in range(len(docs)):
            score = max(0.0, 1.0 - dists[i])
            sources.append(
                {
                    "content": docs[i],
                    "source": metas[i]["source"],
                    "chunk_id": metas[i]["chunk_id"],
                    "score": score,
                }
            )
        return sources

    # -------------------- Generación --------------------
    def generate_answer(
        self,
        query: str,
        context_sources: List[dict],
        provider: LLMProvider,
    ) -> str:
        """Genera una respuesta usando el provider LLM proporcionado."""
        if not context_sources:
            return "No tengo esa información en los documentos consultados."

        context_block = "\n\n".join(
            [
                f"[Fuente: {s['source']} | chunk: {s['chunk_id']} | "
                f"relevancia: {s['score']:.3f}]\n{s['content']}"
                for s in context_sources
            ]
        )

        user_prompt = (
            f"CONTEXTO:\n{context_block}\n\n"
            f"PREGUNTA: {query}\n\n"
            f"RESPUESTA:"
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        return provider.generate(
            messages=messages,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.LLM_MAX_TOKENS,
        )

    # -------------------- End-to-end --------------------
    def query(
        self, question: str, provider: LLMProvider
    ) -> Tuple[str, List[dict]]:
        """Flujo completo: retrieve + generate con el provider dado."""
        sources = self.retrieve(question)
        answer = self.generate_answer(question, sources, provider)
        return answer, sources
