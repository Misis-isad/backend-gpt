from fastapi import FastAPI, Depends
import json
import logging
from ml import text_processing, create_prompt, decode_text
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from pydantic import BaseModel


class Request(BaseModel):
    text: str


app = FastAPI()
with open("cookies.json", "r") as file:
    cookies = json.load(file)


async def shutdown():
    logging.info("shutting down")


app.on_event("shutdown")(shutdown)


@app.post("/ask")
async def ask_gpt(request: Request):
    bot = await Chatbot.create(cookies=cookies)
    text = text_processing(request.text)
    requests = create_prompt(text, "Prompt.txt")
    responses = []
    for index, request in enumerate(requests):
        print("sending request")
        responses.append(await bot.ask(
                prompt=request,
                conversation_style=ConversationStyle.creative,
                simplify_response=True,
        ))
    return responses

"""
{
    "text": str
    "author": str
    "sources": list[dict]
    "sources_text": str
    "suggestions": list[str]
    "messages_left": int
}
"""
