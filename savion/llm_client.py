"""
savion.llm_client

Simple wrapper to obtain an AI‑generated rationale.

- Reads LLM_API_KEY from the environment (via python‑dotenv).
- If the key is missing, returns a placeholder string.
- Keeps the implementation deliberately lightweight – you can swap in
  any LLM SDK later (OpenAI, Anthropic, Gemini, etc.).
"""

import os
from typing import Optional

# Load .env variables if present (python‑dotenv is already in requirements)
try:
    from dotenv import load_dotenv
    load_dotenv()  # Populate os.environ from a .env file, if it exists
except Exception:
    # If python‑dotenv cannot be imported we simply continue – the env
    # variable may still be defined elsewhere (e.g., system env)
    pass


def _get_api_key() -> Optional[str]:
    """Return the LLM API key if it exists, otherwise None."""
    return os.getenv("LLM_API_KEY")


def get_rationale(prompt: str) -> str:
    """
    Return a short AI‑generated explanation for a given prompt.

    Args:
        prompt: The text we want the LLM to comment on.

    Returns:
        A string with the AI’s response, or a placeholder if no API key is set.
    """
    api_key = _get_api_key()
    if not api_key:
        # No key → we cannot call an external service.
        return "AI rationale placeholder."

    # -----------------------------------------------------------------
    # INSERT YOUR LLM CALL HERE
    # Example (pseudo‑code):
    #   response = my_llm_client(api_key).chat(prompt)
    #   return response.text.strip()
    # -----------------------------------------------------------------
    # For now we return a dummy string to keep the library functional.
    return "AI rationale placeholder – replace with real LLM call."
