import json
import telegram
import boto3
import os


def lambda_handler(event, context):
    chat_id, text = telegram.get_chat_id(event), telegram.get_text(event)
    
    sfn_client = boto3.client('stepfunctions')

    # Start the state machine execution
    sfn_client.start_execution(
        stateMachineArn=os.environ['STATE_MACHINE_ARN'],  
        input=json.dumps({
            "chat_id": chat_id,
            "command": text
        })
    )
    return {"statusCode": 200, "chat_id": 6180995571, "text": text, "command": text}

