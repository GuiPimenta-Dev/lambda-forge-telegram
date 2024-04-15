from infra.services import Services

class TestConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Test",
            path="./functions/test",
            description="handles the test command",
            
        )
