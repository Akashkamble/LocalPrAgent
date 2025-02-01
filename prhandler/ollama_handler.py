from typing import Tuple
import requests
from logger.logger import get_logger
from .base_handler import BaseAIHandler

from settings.config import get_settings


class OllamaAIHandler(BaseAIHandler):
    def __init__(self):
        super().__init__()
        self.api_base = get_settings().get("ollama.api_base")
        self.model = get_settings().get("ollama.model")

    async def chat_completion(
            self,
            model: str,
            system: str,
            user: str,
            temperature: float = get_settings().get("ollama.temperature", 0.2)
    ) -> Tuple[str, str]:
        """Send chat completion request to local Ollama instance"""
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]

        try:
            response = requests.post(
                f"{self.api_base}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"], "stop"

        except Exception as e:
            get_logger().error(f"Ollama API error: {str(e)}")
            raise