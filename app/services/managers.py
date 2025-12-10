from app.core.strategies import LLMStrategy, VLMStrategy
from typing import Optional

class ChatManager:
    def __init__(self, strategy: LLMStrategy):
        self.strategy = strategy
    
    async def get_response(self, text: str, context: Optional[str] = None) -> str:
        return await self.strategy.generate_response(text, context)

class VLMManager:
    def __init__(self, strategy: VLMStrategy):
        self.strategy = strategy
    
    async def analyze_image(self, image_data: bytes) -> str:
        return await self.strategy.process_image(image_data)

class MultimodalManager:
    def __init__(self, llm_manager: ChatManager, vlm_manager: VLMManager):
        self.llm = llm_manager
        self.vlm = vlm_manager

    async def process_interaction(self, text_query: Optional[str], image_data: Optional[bytes]) -> dict:
        image_context = None
        if image_data:
            image_context = await self.vlm.analyze_image(image_data)
        
        # If there is no text but there is an image, we can just return the caption/description
        if not text_query and image_context:
            return {
                "response": f"I see: {image_context}",
                "context": image_context
            }
            
        final_response = await self.llm.get_response(text_query or "", image_context)
        return {
            "response": final_response,
            "context": image_context
        }
