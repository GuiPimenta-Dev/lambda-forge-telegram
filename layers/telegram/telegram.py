import json
import requests
import boto3


def get_secret(secret="telegram"):
    sm_client = boto3.client("secretsmanager")
    response = sm_client.get_secret_value(SecretId=secret)
    try:
        secret = json.loads(response["SecretString"])
    except json.JSONDecodeError:
        secret = response["SecretString"]

    return secret

def send_message(chat_id, message, parse_mode="HTML"):
    secret = get_secret()
    send_text = f"https://api.telegram.org/bot{secret}/sendMessage?chat_id={chat_id}&parse_mode={parse_mode}&text={message}"
    requests.get(send_text)

def get_text(event):
    body = json.loads(event['body'])
    text = body['message']['text']
    return text

def get_chat_id(event):
    body = json.loads(event['body'])
    chat_id = body['message']['chat']['id']
    return chat_id