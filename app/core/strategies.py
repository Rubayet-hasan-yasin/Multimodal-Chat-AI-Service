from abc import ABC, abstractmethod
from typing import Optional, Any

class VLMStrategy(ABC):
    """Abstract base class for Vision Language Model strategies."""
    
    @abstractmethod
    async def process_image(self, image_data: bytes) -> str:
        """Process an image and return a description or relevant context."""
        pass

class LLMStrategy(ABC):
    """Abstract base class for Large Language Model strategies."""

    @abstractmethod
    async def generate_response(self, text_query: str, context: Optional[str] = None) -> str:
        """Generate a response based on text and optional context."""
        pass
