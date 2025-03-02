from dotenv import load_dotenv
from typing import Union
from fastapi import FastAPI
from models.models import *
from prompt import prompt
from fastapi import Form, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from urllib.parse import urlparse
import os, requests, json, re

app = FastAPI()

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


def validate_news(question: str) -> Union[AutheniticityChecker|AuthenticityError]:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": prompt.format(user_query=question, k=2)},
            {"role": "user", "content": question},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": AutheniticityChecker.model_json_schema()},
        }
    }
    response = requests.post(url, headers=headers, json=payload).json()
    content = response["choices"][0]["message"]["content"]
    cleaned_content = re.sub(r"^```json\n?|```$", "", content.strip())
    content_json = json.loads(cleaned_content)

    if "Invalid query" in cleaned_content:
        return AuthenticityError(**content_json)

    return AutheniticityChecker(**content_json)


@app.post("/whatsapp-webhook")
async def whatsapp_webhook(
    request: Request, From: str = Form(...), Body: str = Form(...)
):
    """Handles incoming WhatsApp messages from Twilio"""
    response = MessagingResponse()

    # Process the news query
    result = validate_news(Body)

    if isinstance(result, AuthenticityError):
        reply = "Sorry, I couldn't verify this news right now. Please try again later."
    else:
        is_authentic = "✅ Authentic" if result.is_authentic else "❌ Fake or Misleading"
        if result.sources:
            formatted_sources = "\n".join([f"{i+1}. {src}" for i, src in enumerate(result.sources)])
        else:
            formatted_sources = "No credible sources found."

        reply = (
            f"🔍 *News Authenticity Check*\n\n"
            f"📜 *News:* {Body}\n\n"
            f"📝 *Verdict:* {is_authentic}\n\n"
            f"📊 *Authenticity Score:* {result.authenticity_score}\n\n"
            f"📖 *Reasoning:* {result.reasoning}\n\n"
            f"🌐 *Souces:*\n{formatted_sources}"
        )

    response.message(reply)
    return Response(content=str(response), media_type="application/xml")


@app.post("/news-check")
def check_authenticity(news: UserQuery):
    query=news.question
    answer=validate_news(query)
    return {"query": query, "answer": answer}


@app.get("/")
def read_root():
    return {"Hello": "World"}




