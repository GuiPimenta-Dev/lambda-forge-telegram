from infra.services import Services


class BotConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Bot",
            path="./functions/bot",
            description="Telegram webhook",
        )

        services.api_gateway.create_endpoint("POST", "/bot", function, public=True)

        stm = services.state_machine
        task = stm.create_task("Bot", function)
        definition = stm.success(task)
        stm.create_state_machine("Bot", definition)