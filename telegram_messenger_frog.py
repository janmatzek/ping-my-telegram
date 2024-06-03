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

    # parse payload
    event_body = event["body"]
    incoming = json.loads(event_body)

    sender_name, contact_info, incoming_message = "", "", ""

    if incoming.get("sender_name", {}):
        sender_name = incoming.get("sender_name", {})
    if incoming.get("contact_info", {}):
        contact_info = incoming.get("contact_info", {})
    if incoming.get("message", ""):
        incoming_message = incoming.get("message", "")

    # construc outgoing message
    outgoing_message = f"""*New message from the interwebs!*
    \n_Message from:_ {sender_name}
    \n_Reply to:_ {contact_info}
    \n_Message:_ {incoming_message}"""

    # send the message to telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={outgoing_message}&parse_mode=markdown"

    response = requests.get(url=url, timeout=10).json()

    print(response)

    return response
