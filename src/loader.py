"""
Módulo de carga de documentos y chunking.
Soporta: .txt, .md, .pdf
"""
import logging
from pathlib import Path
from typing import Dict, List

from pypdf import PdfReader

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}


def load_text_file(path: Path) -> str:
    """Carga el contenido de un archivo de texto (.txt o .md)."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf_file(path: Path) -> str:
    """Extrae el texto de un archivo PDF."""
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        extracted = page.extract_text() or ""
        pages.append(extracted)
    return "\n".join(pages)


def load_documents(docs_dir: str) -> Dict[str, str]:
    """
    Carga todos los documentos soportados de un directorio.

    Args:
        docs_dir: ruta al directorio con documentos.

    Returns:
        Diccionario {nombre_archivo: contenido_texto}.
    """
    docs_path = Path(docs_dir)
    if not docs_path.exists():
        raise FileNotFoundError(f"El directorio {docs_dir} no existe.")

    documents: Dict[str, str] = {}
    for file_path in sorted(docs_path.iterdir()):
        if not file_path.is_file():
            continue
        ext = file_path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            logger.info(f"Omitiendo archivo no soportado: {file_path.name}")
            continue
        try:
            if ext in {".txt", ".md"}:
                documents[file_path.name] = load_text_file(file_path)
            elif ext == ".pdf":
                documents[file_path.name] = load_pdf_file(file_path)
            logger.info(f"Cargado: {file_path.name}")
        except Exception as e:
            logger.error(f"Error cargando {file_path.name}: {e}")

    return documents


def chunk_text(
    text: str, chunk_size: int = 500, overlap: int = 50
) -> List[str]:
    """
    Divide un texto en chunks respetando párrafos cuando es posible.

    Args:
        text: texto completo a dividir.
        chunk_size: tamaño objetivo en caracteres.
        overlap: solapamiento en caracteres (para párrafos muy largos).

    Returns:
        Lista de chunks.
    """
    if not text or not text.strip():
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        # Si el párrafo cabe en el chunk actual, lo agregamos
        if len(current) + len(para) + 2 <= chunk_size:
            current = (current + "\n\n" + para).strip()
        else:
            # Guardamos el chunk actual
            if current:
                chunks.append(current)
                current = ""
            # Si el párrafo es más grande que chunk_size, lo partimos
            if len(para) > chunk_size:
                step = chunk_size - overlap
                for i in range(0, len(para), step):
                    chunks.append(para[i : i + chunk_size])
            else:
                current = para

    if current:
        chunks.append(current)

    return chunks
