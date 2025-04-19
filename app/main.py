import os
from openai import OpenAI
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .utils import format_travel_response
from .models import ChatRequest, ChatResponse
from dotenv import load_dotenv

from .utils import rate_limiter

import logging
import redis

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY",""))

app = FastAPI()

""" Middleware for CORS"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://pawait-gpt.vercel.app"],
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
@rate_limiter(max_calls=1, time_frame=20)
async def chat(request: Request,payload: ChatRequest):
    """ chat endpoint.
    Body:
        Request: ChatRequest
        ChatRequest:
            mesaage: List[message]
    Returns :
        formated message
    """
    if not payload.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    try:
        messages = [
            {"role": msg.role, "content": msg.content} for msg in payload.messages
        ]

        system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful travel assistant. For travel-related queries, provide clear, concise answers "
                "including passport requirements, visa requirements, additional information and any other related travel advisory "
                "proof of accommodation, proof of sufficient funds, "
                "return ticket, travel insurance, and COVID-19 restrictions. Format your response in a structured way possible."
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
