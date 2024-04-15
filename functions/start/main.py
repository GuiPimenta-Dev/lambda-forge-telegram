import telegram


def start_handler(event, context):
    chat_id = event["chat_id"]
    telegram.send_message(chat_id, "Welcome to the bot!")
    return {"statusCode": 200}
