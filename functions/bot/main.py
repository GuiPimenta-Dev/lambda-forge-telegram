import telegram


def lambda_handler(event, context):
    chat_id, text = telegram.get_chat_id_and_text(event)  
    return {
        "statusCode": 200,
        "chat_id": chat_id,
        "text": text  
    }
