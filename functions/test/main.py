import telegram


def lambda_handler(event, context):
    chat_id = event["chat_id"]
    telegram.send_message(chat_id, "This is a test.")
    return {"statusCode": 200}
