"""
Abstracción de proveedores LLM.

Permite intercambiar entre Groq, Google Gemini y futuros proveedores
sin tocar el pipeline RAG. Cada proveedor implementa la misma interfaz
`generate(messages, temperature, max_tokens) -> str`.
"""
from abc import ABC, abstractmethod
from typing import List


class LLMProvider(ABC):
    """Interfaz común para proveedores LLM."""

    @abstractmethod
    def generate(
        self,
        messages: List[dict],
        temperature: float = 0.1,
        max_tokens: int = 600,
    ) -> str:
        """Genera una respuesta dado un historial de mensajes estilo OpenAI."""
        ...

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Nombre legible para mostrar en la UI."""
        ...

    @property
    @abstractmethod
    def model_id(self) -> str:
        """ID técnico del modelo (para debugging y logs)."""
        ...


# ============================================================
# Groq Provider
# ============================================================
class GroqProvider(LLMProvider):
    """Wrapper para la API de Groq (modelos open-source: Llama, GPT-OSS, etc.)."""

    def __init__(self, api_key: str, model: str) -> None:
        from groq import Groq

        if not api_key:
            raise RuntimeError("GROQ_API_KEY no configurada en .env")
        self.client = Groq(api_key=api_key)
        self._model = model

    def generate(
        self,
        messages: List[dict],
        temperature: float = 0.1,
        max_tokens: int = 600,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    @property
    def display_name(self) -> str:
        return f"Groq · {self._model}"

    @property
    def model_id(self) -> str:
        return self._model


# ============================================================
# Google Gemini Provider
# ============================================================
class GeminiProvider(LLMProvider):
    """Wrapper para la API de Google Gemini."""

    def __init__(self, api_key: str, model: str) -> None:
        import google.generativeai as genai

        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY no configurada en .env")
        genai.configure(api_key=api_key)
        self._model_name = model
        self._genai = genai

    def generate(
        self,
        messages: List[dict],
        temperature: float = 0.1,
        max_tokens: int = 600,
    ) -> str:
        # Separar system prompt del resto (Gemini lo pide aparte)
        system_instruction = None
        contents = []
        for m in messages:
            if m["role"] == "system":
                system_instruction = m["content"]
            elif m["role"] == "user":
                contents.append({"role": "user", "parts": [m["content"]]})
            elif m["role"] == "assistant":
                contents.append({"role": "model", "parts": [m["content"]]})

        model = self._genai.GenerativeModel(
            model_name=self._model_name,
            system_instruction=system_instruction,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )
        response = model.generate_content(contents)
        return response.text

    @property
    def display_name(self) -> str:
        return f"Google Gemini · {self._model_name}"

    @property
    def model_id(self) -> str:
        return self._model_name


# ============================================================
# Factory
# ============================================================
def build_provider(provider_name: str) -> LLMProvider:
    """Construye el provider solicitado leyendo config/env.

    Args:
        provider_name: "groq" o "gemini"
    """
    import config

    name = provider_name.lower().strip()
    if name == "groq":
        return GroqProvider(config.GROQ_API_KEY, config.LLM_MODEL)
    elif name == "gemini":
        return GeminiProvider(config.GOOGLE_API_KEY, config.GEMINI_MODEL)
    else:
        raise ValueError(
            f"Provider desconocido: '{provider_name}'. "
            f"Opciones válidas: 'groq', 'gemini'."
        )
