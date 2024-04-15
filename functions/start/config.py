from infra.services import Services

class StartConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Start",
            path="./functions/start",
            description="handles the start command",
            
        )
