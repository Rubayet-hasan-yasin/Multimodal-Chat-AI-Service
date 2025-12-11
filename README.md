# Multimodal Chat AI Service

A compact FastAPI service that accepts text and images and returns AI responses using Google Gemini (multimodal). Includes user authentication, image uploads, conversation logging, and a strategy-based architecture so AI providers can be swapped easily.

## Features
- Register / Login (JWT)
- Multimodal chat: text-only, image-only, or combined
- Image upload stored under `static/images`
- Conversation history saved to the database
- Strategy pattern for AI providers (Gemini by default)

## Quick Start
1. Clone the repo and enter the project folder.
2. Create and activate a Python venv (recommended).
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file — copy from `.env.example` and set values:
- `DATABASE_URL` (e.g. `postgresql+asyncpg://user:pass@localhost/dbname`)
- `SECRET_KEY` (random secret string)
- `GOOGLE_GENERATIVE_AI_API_KEY` or `GEMINI_API_KEY` (Gemini API key)

5. Start the server (Windows PowerShell):

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## API Overview
Base path: `http://127.0.0.1:8000/api/v1`

### Authentication
- `POST /api/v1/auth/register` — create a user
  - Body JSON: `{ "email": "...", "password": "..." }`
- `POST /api/v1/auth/login` — login and get access token
  - Form data: `username` (email), `password`
  - Response: `{ "access_token": "...", "token_type": "bearer" }`

### Multimodal Chat
- `POST /api/v1/multimodal-chat` — main endpoint
  - Requires header: `Authorization: Bearer <TOKEN>`
  - Form fields (multipart/form-data):
    - `text` (optional)
    - `image` (optional file)
  - Response body: `{ id, text_query, image_url, response_text, timestamp, llm_model, vlm_model }`



## Key Files
- `app/main.py` — application entry, static files mounting, DB init
- `app/api/v1/api.py` — router registration
- `app/api/v1/endpoints/auth.py` — register and login endpoints
- `app/api/v1/endpoints/chat.py` — multimodal chat endpoint (saves image, calls managers, logs)
- `app/services/image_service.py` — handles saving uploaded images
- `app/services/managers.py` — `ChatManager`, `VLMManager`, `MultimodalManager` orchestration
- `app/services/gemini_strategies.py` — Gemini LLM/VLM strategy implementations
- `app/core/config.py` — settings loaded from `.env`
- `app/models/` — `User` and `ConversationLog` DB models
- `app/schemas/` — Pydantic schemas for validation

## How it works (short)
1. Client calls `/multimodal-chat` with JWT and multipart data.
2. `get_current_user` validates token and provides the `User` object.
3. If image present, `ImageService` saves it in `static/images` and returns bytes & path.
4. `MultimodalManager` uses the VLM strategy to describe the image (if any) and the LLM strategy to generate a final response using text + image context.
5. The conversation is saved to the DB and returned to the client.

## Swapping AI providers
The code uses a strategy pattern. To replace Gemini with another provider:
- Implement the same methods (`process_image`, `generate_response`) in a new strategy class.
- Wire the new strategy in `app/api/v1/endpoints/chat.py` when constructing managers.

