import logging
import warnings

import google.generativeai as genai

from schedulebot.config import GEMINI_API_TOKEN
from schedulebot.singleton import Singleton

warnings.filterwarnings("ignore", category=FutureWarning, module="google.generativeai")

logger = logging.getLogger(__name__)


class AIController(metaclass=Singleton):
    def __init__(self, model_name: str, *args, **kwargs) -> None:
        self.model_name = model_name
        self.model: genai.GenerativeModel | None = None
        self.is_configured = False

        if (
            GEMINI_API_TOKEN
            and GEMINI_API_TOKEN.strip()
            and GEMINI_API_TOKEN != "your_gemini_api_key"
        ):
            try:
                genai.configure(api_key=GEMINI_API_TOKEN)
                self.model = genai.GenerativeModel(model_name, *args, **kwargs)
                self.is_configured = True
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini AI model: {e}")
        else:
            logger.info("Gemini API token is not provided. AI features will be disabled.")

    def generate_content(self, prompt: str, *args, **kwargs) -> str:
        if not self.is_configured or self.model is None:
            return (
                "AI notes assistant is currently unavailable (GEMINI_API_TOKEN is not configured)."
            )
        try:
            response = self.model.generate_content(prompt, *args, **kwargs)
            return response.text if hasattr(response, "text") else str(response)
        except Exception as e:
            logger.error(f"Error generating AI content: {e}")
            return f"Failed to generate AI response: {e}"
