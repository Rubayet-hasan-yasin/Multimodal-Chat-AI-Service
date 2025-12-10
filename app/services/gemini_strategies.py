import google.generativeai as genai
from typing import Optional
from app.core.strategies import VLMStrategy, LLMStrategy
from app.core.config import settings
import io
from PIL import Image

# Configure Gemini API
api_key = settings.GEMINI_API_KEY or settings.GEMINI_API_KEY
genai.configure(api_key=api_key)


class GeminiVLMStrategy(VLMStrategy):
    """Vision Language Model using Gemini's multimodal capabilities."""
    
    def __init__(self, model_name: str = "gemini-flash-latest"):
        """
        Initialize Gemini VLM with specified model.
        
        Args:
            model_name: Gemini model to use (e.g., "gemini-1.5-flash-latest", "gemini-1.5-flash-latest")
        """
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    async def process_image(self, image_data: bytes) -> str:
        """
        Process an image using Gemini's vision capabilities.
        
        Args:
            image_data: Raw image bytes
            
        Returns:
            Description of the image content
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Generate description using Gemini
            prompt = "Describe this image in detail. What do you see?"
            response = self.model.generate_content([prompt, image])
            
            return response.text.strip()
        except Exception as e:
            return f"Error processing image with Gemini: {str(e)}"


class GeminiLLMStrategy(LLMStrategy):
    """Large Language Model using Gemini API."""
    
    def __init__(self, model_name: str = "gemini-flash-latest"):
        """
        Initialize Gemini LLM with specified model.
        
        Args:
            model_name: Gemini model to use (e.g., "gemini-pro", "gemini-1.5-flash-latest")
        """
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    async def generate_response(self, text_query: str, context: Optional[str] = None) -> str:
        """
        Generate a response using Gemini LLM.
        
        Args:
            text_query: User's question or prompt
            context: Optional context (e.g., image description)
            
        Returns:
            Generated response text
        """
        try:
            # Construct prompt with context if available
            if context:
                prompt = f"""You are a helpful multimodal assistant. I will provide a description of an image I am looking at, and then ask a question.

Image Description: {context}

User Question: {text_query}

Please provide a helpful and accurate response."""
            else:
                prompt = text_query

            # Generate response
            response = self.model.generate_content(prompt)
            
            return response.text.strip()
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"


class GeminiMultimodalStrategy(VLMStrategy, LLMStrategy):
    """
    Unified multimodal strategy using Gemini's native multimodal capabilities.
    This can handle both image and text in a single API call.
    """
    
    def __init__(self, model_name: str = "gemini-flash-latest"):
        """
        Initialize Gemini multimodal model.
        
        Args:
            model_name: Gemini model to use (e.g., "gemini-1.5-flash-latest", "gemini-1.5-flash-latest")
        """
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)

    async def process_image(self, image_data: bytes) -> str:
        """Process image and return description."""
        try:
            image = Image.open(io.BytesIO(image_data))
            prompt = "Describe this image in detail. What do you see?"
            response = self.model.generate_content([prompt, image])
            return response.text.strip()
        except Exception as e:
            return f"Error processing image: {str(e)}"

    async def generate_response(self, text_query: str, context: Optional[str] = None) -> str:
        """Generate text response with optional context."""
        try:
            if context:
                prompt = f"""You are a helpful multimodal assistant. 

Image Description: {context}

User Question: {text_query}

Please provide a helpful response."""
            else:
                prompt = text_query

            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    async def process_multimodal(self, text_query: str, image_data: Optional[bytes] = None) -> str:
        """
        Process both text and image together in a single Gemini API call.
        This is more efficient than separate VLM + LLM calls.
        
        Args:
            text_query: User's question or prompt
            image_data: Optional raw image bytes
            
        Returns:
            Generated response considering both text and image
        """
        try:
            if image_data:
                # Process text + image together
                image = Image.open(io.BytesIO(image_data))
                response = self.model.generate_content([text_query, image])
            else:
                # Text only
                response = self.model.generate_content(text_query)
            
            return response.text.strip()
        except Exception as e:
            return f"Error processing multimodal input: {str(e)}"
