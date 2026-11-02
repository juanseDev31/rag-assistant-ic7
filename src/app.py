"""
Interfaz Streamlit del asistente RAG.
Prueba técnica — AI Developer Engineer Junior | I Cloud Seven
"""
import logging
import os
from pathlib import Path

import streamlit as st

import config
from llm_providers import LLMProvider, build_provider
from rag import RAGAssistant

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# -------------- Configuración de la página --------------
st.set_page_config(
    page_title="Asistente RAG | I Cloud Seven",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -------------- Inicialización cacheada --------------
@st.cache_resource(
    show_spinner="⏳ Cargando modelo de embeddings e indexando documentos…"
)
def init_rag() -> RAGAssistant:
    assistant = RAGAssistant()
    assistant.load_and_index_documents(config.DOCS_PATH)
    return assistant


@st.cache_resource
def get_provider(provider_name: str) -> LLMProvider:
    """Cachea los providers (ligero, pero evita recrearlos en cada mensaje)."""
    return build_provider(provider_name)


def reset_index_and_cache() -> None:
    """Borra el vector store y limpia el cache de Streamlit para re-indexar."""
    vs_path = Path(config.VECTORSTORE_PATH)
    if vs_path.exists():
        vs_path.unlink()
    st.cache_resource.clear()


# -------------- Detectar providers configurados --------------
AVAILABLE_PROVIDERS = []
if config.GROQ_API_KEY:
    AVAILABLE_PROVIDERS.append(("groq", f"🚀 Groq · {config.LLM_MODEL}"))
if config.GOOGLE_API_KEY:
    AVAILABLE_PROVIDERS.append(("gemini", f"✨ Gemini · {config.GEMINI_MODEL}"))


# -------------- Sidebar --------------
with st.sidebar:
    st.title("🤖 Asistente RAG")
    st.caption("Prueba técnica — I Cloud Seven")
    st.markdown("---")

    # ---- Selector de provider ----
    st.subheader("🧠 Modelo LLM")
    if not AVAILABLE_PROVIDERS:
        st.error(
            "❌ No hay API keys configuradas. Edita tu `.env` y agrega al "
            "menos `GROQ_API_KEY` o `GOOGLE_API_KEY`."
        )
        selected_provider_name = None
    else:
        provider_labels = {name: label for name, label in AVAILABLE_PROVIDERS}
        default_idx = 0
        if config.DEFAULT_PROVIDER in provider_labels:
            default_idx = list(provider_labels.keys()).index(
                config.DEFAULT_PROVIDER
            )

        selected_provider_name = st.selectbox(
            "Elige el proveedor",
            options=list(provider_labels.keys()),
            format_func=lambda x: provider_labels[x],
            index=default_idx,
            key="provider_selector",
        )
        st.caption(
            "💡 Puedes cambiar entre proveedores en cualquier momento. "
            "El contexto recuperado es el mismo; solo cambia quien genera "
            "la respuesta final."
        )

    st.markdown("---")
    st.subheader("🧰 Stack técnico")
    st.markdown(
        """
- **LLM:** Groq y/o Google Gemini (intercambiable)
- **Embeddings:** sentence-transformers (MiniLM-L6-v2)
- **Vector Store:** SimpleVectorStore (numpy, persistente)
- **UI:** Streamlit
- **Lenguaje:** Python 3.11
"""
    )

    st.markdown("---")
    st.subheader("📄 Documentos indexados")
    if os.path.exists(config.DOCS_PATH):
        docs_in_folder = sorted(
            [
                f
                for f in os.listdir(config.DOCS_PATH)
                if f.lower().endswith((".txt", ".md", ".pdf"))
            ]
        )
        if docs_in_folder:
            for f in docs_in_folder:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"`{f}`")
                with col2:
                    if st.button("🗑️", key=f"del_{f}", help=f"Eliminar {f}"):
                        try:
                            os.remove(os.path.join(config.DOCS_PATH, f))
                            reset_index_and_cache()
                            st.success(f"Eliminado: {f}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error eliminando {f}: {e}")
        else:
            st.info("No hay documentos aún. Sube uno abajo 👇")
    else:
        st.warning(f"No existe el directorio {config.DOCS_PATH}")

    st.markdown("---")
    st.subheader("📤 Subir documentos")
    st.caption("Formatos soportados: .txt, .md, .pdf")
    uploaded_files = st.file_uploader(
        "Arrastra archivos aquí",
        type=["txt", "md", "pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        os.makedirs(config.DOCS_PATH, exist_ok=True)
        saved_files = []
        for uploaded in uploaded_files:
            file_path = os.path.join(config.DOCS_PATH, uploaded.name)
            with open(file_path, "wb") as f:
                f.write(uploaded.getbuffer())
            saved_files.append(uploaded.name)

        if saved_files:
            st.success(
                f"✅ {len(saved_files)} archivo(s) guardado(s). "
                "Haz clic en **Re-indexar** para incluirlos en el chat."
            )

    if st.button("🔄 Re-indexar documentos", use_container_width=True):
        reset_index_and_cache()
        st.rerun()

    st.markdown("---")
    st.subheader("⚙️ Configuración")
    st.markdown(
        f"""
- Chunk size: `{config.CHUNK_SIZE}`
- Chunk overlap: `{config.CHUNK_OVERLAP}`
- Top-K recuperación: `{config.TOP_K}`
"""
    )

    st.markdown("---")
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# -------------- Cuerpo principal --------------
st.title("🤖 Asistente Documental RAG")
st.caption(
    "Haz preguntas sobre los documentos internos. "
    "Las respuestas se generan únicamente con la información de los documentos indexados."
)

# Verificar que al menos un provider esté configurado
if not AVAILABLE_PROVIDERS or not selected_provider_name:
    st.error(
        "❌ **No hay providers LLM configurados.**\n\n"
        "Edita tu `.env` y agrega al menos una de estas keys:\n"
        "- `GROQ_API_KEY` (https://console.groq.com/keys)\n"
        "- `GOOGLE_API_KEY` (https://aistudio.google.com/apikey)"
    )
    st.stop()

# Inicializar el asistente y el provider seleccionado
try:
    assistant = init_rag()
    chunk_count = assistant.collection.count()
    current_provider = get_provider(selected_provider_name)
except Exception as e:
    st.error(f"Error inicializando: {e}")
    st.stop()

col1, col2 = st.columns([3, 2])
with col1:
    st.success(
        f"✅ Sistema listo — **{chunk_count} chunks indexados** en el vector store."
    )
with col2:
    st.info(f"🧠 Generando con: **{current_provider.display_name}**")

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("provider"):
            st.caption(f"🧠 Generado por: {message['provider']}")
        if message.get("sources"):
            with st.expander(
                f"📚 Fuentes consultadas ({len(message['sources'])})"
            ):
                for src in message["sources"]:
                    st.markdown(
                        f"**📄 {src['source']}** — chunk `{src['chunk_id']}` "
                        f"— relevancia `{src['score']:.3f}`"
                    )
                    st.text(src["content"])
                    st.markdown("---")

# Input del usuario
if prompt := st.chat_input("¿Qué quieres preguntar sobre los documentos?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        spinner_label = (
            f"🤔 Buscando contexto y generando con {current_provider.display_name}…"
        )
        with st.spinner(spinner_label):
            try:
                answer, sources = assistant.query(prompt, current_provider)
            except Exception as e:
                answer = f"❌ Error durante la consulta: {e}"
                sources = []

        st.markdown(answer)
        st.caption(f"🧠 Generado por: {current_provider.display_name}")
        if sources:
            with st.expander(f"📚 Fuentes consultadas ({len(sources)})"):
                for src in sources:
                    st.markdown(
                        f"**📄 {src['source']}** — chunk `{src['chunk_id']}` "
                        f"— relevancia `{src['score']:.3f}`"
                    )
                    st.text(src["content"])
                    st.markdown("---")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "provider": current_provider.display_name,
        }
    )
