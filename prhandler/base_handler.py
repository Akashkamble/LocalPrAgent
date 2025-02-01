from abc import ABC, abstractmethod
from typing import Tuple


class BaseAIHandler(ABC):
    def __init__(self):
        self.main_language = None

    @abstractmethod
    async def chat_completion(
            self,
            model: str,
            system: str,
            user: str,
            temperature: float = 0.2
    ) -> Tuple[str, str]:
        """
        Send a chat completion request to the AI model

        Returns:
            Tuple of (response_text, finish_reason)
        """
        pass