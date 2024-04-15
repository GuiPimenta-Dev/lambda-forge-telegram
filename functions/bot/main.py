from dataclasses import dataclass
import telegram

@dataclass
class Input:
    pass


@dataclass
class Output:
    message: str


def lambda_handler(event, context):
    chat_id, text = telegram.get_chat_id(event), telegram.get_text(event)
    telegram.send_message(chat_id, text)
