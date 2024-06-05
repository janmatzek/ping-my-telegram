"""
Send a message to Telegram
"""

import json
import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI

# from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Message(BaseModel):
    """expected structure of incoming request"""

    contact_info: str
    message: str


app = FastAPI()
load_dotenv()


# origins = ["https://janmatzek.github.io"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# TODO: refactor to FAST API


@app.post("/contact_form")
async def form_handler(message: Message):
    """
    Retrieves info from the body of an incoming API request and sends it to telegram.
    """
    print("I'm doing something")
    # env variables
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_POST_BOX")

    # parse payload
    contact_info = message.contact_info
    incoming_message = message.message

    print(contact_info)
    print(incoming_message)

    # construc outgoing message
    outgoing_message = f"""*New message from the interwebs!*
    \n_Reply to:_ {contact_info}
    \n_Message:_ {incoming_message}"""

    # send the message to telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={outgoing_message}&parse_mode=markdown"

    response = requests.get(url=url, timeout=10).json()

    status_code = 500
    message = "failure"
    if response["ok"]:
        status_code = 200
        message = "success"

    response = {
        "statusCode": status_code,
        # "headers": {
        #     "Content-Type": "application/json",
        #     "Access-Control-Allow-Origin": "https://janmatzek.github.io",
        #     "Access-Control-Allow-Headers": "*",
        #     "Access-Control-Allow-Methods": "*",
        #     "Access-Control-Allow-Credentials": "true",
        # },
        "body": json.dumps({"message": f"{message}"}),
    }

    return response
