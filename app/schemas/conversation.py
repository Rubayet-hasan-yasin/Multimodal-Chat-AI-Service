from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    text_query: Optional[str] = None
    # Image uploaded via multipart/form-data, so not strictly in Pydantic schema for request body

class ChatResponse(BaseModel):
    id: int
    text_query: Optional[str]
    image_url: Optional[str]
    response_text: Optional[str]
    timestamp: datetime
    llm_model: Optional[str]
    vlm_model: Optional[str]

    class Config:
        from_attributes = True
