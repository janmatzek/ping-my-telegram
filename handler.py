"""
FastAPI handler for AWS
"""

from mangum import Mangum

from telegram_messenger_frog import app

handler = Mangum(app)

print("running")
