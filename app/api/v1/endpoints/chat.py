import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app import schemas, models
from app.db.session import get_db
from app.api.deps import get_current_user
from app.services.managers import MultimodalManager, ChatManager, VLMManager
from app.services.gemini_strategies import GeminiLLMStrategy, GeminiVLMStrategy
from app.services.image_service import ImageService

router = APIRouter()

# Dependency injection for strategies using Gemini
# In a real app, you might use a proper DI container
llm_strategy = GeminiLLMStrategy(model_name="gemini-flash-latest")
vlm_strategy = GeminiVLMStrategy(model_name="gemini-flash-latest")
chat_manager = ChatManager(llm_strategy)
vlm_manager = VLMManager(vlm_strategy)
mm_manager = MultimodalManager(chat_manager, vlm_manager)



@router.post("/multimodal-chat", response_model=schemas.conversation.ChatResponse)
async def multimodal_chat(
    text_query: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if not text_query and not image:
        raise HTTPException(status_code=400, detail="Must provide text or image")

    image_bytes = None
    image_url = None

    if image:
        image_service = ImageService()
        image_bytes, image_url = await image_service.save_image(image)

    result = await mm_manager.process_interaction(text_query, image_bytes)
    
    # Log conversation
    log = models.ConversationLog(
        user_id=current_user.id,
        text_query=text_query,
        image_url=image_url,
        response_text=result["response"],
        llm_model_name=llm_strategy.model_name,
        vlm_model_name=vlm_strategy.model_name, 
        # Context is internal, not stored in this schema iteration, but we have prompt/response
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)

    return schemas.conversation.ChatResponse(
        id=log.id,
        text_query=log.text_query,
        image_url=log.image_url,
        response_text=log.response_text,
        timestamp=log.timestamp,
        llm_model=log.llm_model_name,
        vlm_model=log.vlm_model_name
    )
