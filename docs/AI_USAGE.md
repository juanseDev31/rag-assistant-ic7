# 🤖 Uso de herramientas de desarrollo asistido por AI

**Candidato:** Juan Sebastian Galeano Guerrero
**Fecha:** Noviembre 2026

Este documento describe de forma transparente qué herramientas de AI-assisted development se utilizaron durante el desarrollo de esta prueba técnica, para qué, qué se revisó manualmente y qué aprendizajes se extrajeron.

---

## 1. Herramienta utilizada

**Claude** (Anthropic) — modelo Claude Opus 4.7, mediante la interfaz web de claude.ai.

Se eligió Claude por:
- Capacidad probada en generación de código Python y arquitecturas RAG.
- Habilidad para seguir instrucciones estrictas (prompt engineering, limitaciones de alcance).
- Explicaciones técnicas detalladas que apoyan el aprendizaje durante el desarrollo.

---

## 2. ¿Para qué se usó?

### 2.1 Análisis del enunciado
Se compartió el PDF de la prueba técnica con Claude para mapear cada requisito del enunciado contra la solución planeada, construir un checklist de cumplimiento punto por punto y validar que ningún requisito quedara descubierto.

### 2.2 Diseño de la arquitectura
Discusión iterativa sobre el stack técnico apropiado para el alcance y tiempo disponible. Se evaluaron explícitamente trade-offs entre:
- Streamlit vs FastAPI vs script por consola (UI).
- OpenAI vs Groq vs Ollama vs IBM watsonx (LLM).
- OpenAI embeddings vs sentence-transformers (embeddings).
- ChromaDB vs FAISS vs pgvector (vector store).
- Streamlit Community Cloud vs AWS App Runner vs EC2 (despliegue).

Las decisiones finales fueron tomadas por el candidato basándose en las comparaciones.

### 2.3 Generación del código base
Claude generó el código inicial de:
- `app.py` (interfaz Streamlit con chat, sidebar y manejo de estado).
- `rag.py` (clase `RAGAssistant` con los métodos de indexación, retrieval y generación).
- `loader.py` (lectura de archivos y función de chunking por párrafos).
- `config.py` (centralización de variables de entorno).
- `Dockerfile`, `.gitignore`, `.env.example`, `requirements.txt`.

### 2.4 Diseño del prompt del LLM
El prompt del sistema (`SYSTEM_PROMPT` en `rag.py`) fue iterado específicamente para:
- Forzar al modelo a usar únicamente el contexto recuperado.
- Declarar explícitamente cuando no tiene la información.
- Citar las fuentes en formato consistente.
- Admitir respuestas parciales con honestidad.

### 2.5 Generación de documentos de prueba
Los 3 documentos de la carpeta `./documentos/` (una empresa ficticia "NovaTech Solutions") fueron generados con Claude siguiendo instrucciones específicas para que las 3 preguntas de prueba (completa, parcial y fuera de alcance) funcionaran de forma clara.

### 2.6 Documentación
Claude generó borradores iniciales de `README.md`, este archivo `AI_USAGE.md` y `PRUEBAS.md`. Las secciones fueron revisadas y ajustadas por el candidato.

### 2.7 Guion del video
El guion de la grabación del video explicativo (máx. 5 min) fue estructurado con Claude.

---

## 3. ¿Qué se revisó manualmente?

- **Lógica del pipeline RAG:** se validó end-to-end que el flujo retrieval → generación funciona y que las fuentes se devuelven correctamente.
- **Pruebas con documentos reales:** las 3 preguntas de prueba (ver `PRUEBAS.md`) fueron ejecutadas manualmente y las respuestas verificadas contra los documentos fuente.
- **Prompt engineering:** se ajustó el `SYSTEM_PROMPT` tras ver que el modelo tendía a complementar respuestas con conocimiento general; se agregaron reglas estrictas de solo-usar-contexto.
- **Chunking:** se validó visualmente que los chunks respetaran párrafos y que ningún chunk cortara una idea importante por la mitad.
- **Configuración de despliegue:** la selección de Streamlit Community Cloud sobre AWS fue una decisión de riesgo que el candidato tomó explícitamente, priorizando entrega segura sobre impacto cloud.
- **Documentación:** cada sección del README fue revisada; se eliminaron fragmentos genéricos y se añadió información específica del contexto.
- **Nombres y claridad de código:** se renombraron variables y se agregaron docstrings donde faltaban claridad.

---

## 4. ¿Qué aprendí durante el desarrollo?

### 4.1 Conceptos técnicos

- **La importancia del prompt engineering en RAG.** Aunque el pipeline técnico esté bien implementado, un prompt mal diseñado hace que el modelo alucine, mezcle conocimiento general con el contexto, o cite incorrectamente las fuentes. El `SYSTEM_PROMPT` es tan crítico como la calidad del retrieval.

- **Trade-offs en chunking.** Un chunk muy pequeño (ej. 100 chars) pierde contexto; uno muy grande (ej. 2000 chars) diluye la señal del embedding. Respetar párrafos ayuda a mantener unidades semánticas coherentes.

- **ChromaDB es sorprendentemente simple.** Con 5 líneas de código tienes un vector store persistente con similitud coseno. Para prototipos no se justifica inicialmente ir a Pinecone/Weaviate.

- **Groq cambia la UX.** La latencia de Llama 3.3 70B vía Groq es significativamente menor que GPT-4 vía OpenAI, lo que mejora la percepción de la aplicación en un chat.

- **sentence-transformers vs embeddings pagados.** El modelo MiniLM-L6-v2 (local, gratis) da resultados muy buenos para corpus pequeños. La diferencia con OpenAI `text-embedding-3-small` solo se nota en corpus grandes y multilingües complejos.

### 4.2 Conceptos de criterio

- **Priorizar entregar sobre impresionar.** La elección de Streamlit Community Cloud en vez de AWS fue consciente: el enunciado dice que cloud es "deseable, no obligatorio", y el riesgo de no entregar por fallar en el deploy AWS no se compensa con los puntos adicionales.

- **Honestidad en el uso de AI.** El enunciado evalúa criterio responsable al usar herramientas AI, no si las usas o no. Documentar transparentemente qué hizo la herramienta y qué revisó el humano es más valioso que ocultarlo.

- **La documentación vale tanto como el código.** El 50% del score está entre documentación (15%) + código ordenado (15%) + explicación clara (10%) + pruebas (10%). Un código brillante mal documentado puntúa peor que uno medio pero bien explicado.

---

## 5. Reflexión final

Las herramientas de AI-assisted development aceleran enormemente el trabajo repetitivo (código boilerplate, documentación estándar, exploración de alternativas), pero no reemplazan el **criterio técnico** del desarrollador en:

- Decidir qué construir y qué dejar fuera.
- Validar que lo generado efectivamente funciona.
- Identificar los trade-offs reales de cada decisión.
- Reconocer y corregir las "alucinaciones" o errores sutiles del código generado.

El patrón de trabajo más efectivo fue: **el humano define la intención y los criterios, la AI genera el borrador, el humano valida y corrige**.
