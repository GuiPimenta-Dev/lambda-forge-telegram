from infra.services import Services
from aws_cdk import aws_iam
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as task


class BotConfig:
    def __init__(self, services: Services) -> None:

        bot_function = services.aws_lambda.create_function(
            name="Bot",
            path="./functions/bot",
            description="Telegram webhook",
        )

        services.api_gateway.create_endpoint("POST", "/mybot", bot_function, public=True)

       