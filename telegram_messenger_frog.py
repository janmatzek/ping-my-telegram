"""
Send a message to Telegram
"""

import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def handler(event, context):
    """
    Retrieves info from the body of an incoming API request and sends it to telegram.
    """
    # env variables
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_POST_BOX")

    # check origin header (like an animal)
    headers = event.get("headers", {})
    origin = headers.get("origin", "")

    if origin != "https://janmatzek.github.io":
        response = {
            "statusCode": 403,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "https://janmatzek.github.io",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Methods": "OPTIONS,POST",
            },
            "body": json.dumps({"message": "Not allowed"}),
        }

        return response

    # parse payload
    event_body = event["body"]
    incoming = json.loads(event_body)

    contact_info, incoming_message = "", ""

    if incoming.get("contact_info", {}):
        contact_info = incoming.get("contact_info", {})
    if incoming.get("message", ""):
        incoming_message = incoming.get("message", "")

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
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Methods": "OPTIONS,POST",
        },
        "body": json.dumps({"message": f"{message}"}),
    }

    return response
