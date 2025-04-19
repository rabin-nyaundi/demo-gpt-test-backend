import os
from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .utils import format_travel_response
from .models import ChatRequest, ChatResponse
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)


app = FastAPI()

""" Middleware for CORS"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://pawait-gpt.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {
        "mesaage":"API running"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """ chat endpoint.
    Body:
        Request: ChatRequest
        ChatRequest:
            mesaage: List[message]
    Returns :
        formated message
    """
    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    try:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in request.messages
        ]

        system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful travel assistant. For travel-related queries, provide clear, concise answers "
                "including required visa documentation, passport requirements, additional documents and any relevant "
                "travel advisories. Format your response in a structured way possible."
            )
        }
        messages.insert(0, system_prompt)

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7,
        )


        reply = response.choices[0].message.content.strip()

        formatted_reply = format_travel_response(reply)

        return ChatResponse(reply=formatted_reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
