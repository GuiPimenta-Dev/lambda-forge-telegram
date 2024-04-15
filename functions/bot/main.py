import telegram


def lambda_handler(event, context):
    chat_id, text = telegram.get_chat_id(event), telegram.get_text(event)
    
    telegram.send_message(chat_id, f"Received command: {text}")

    return {"statusCode": 200, "text": text, "command": text}
 
