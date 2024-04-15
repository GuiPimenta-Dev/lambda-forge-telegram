from aws_cdk import Duration
from aws_cdk.aws_lambda import Code, Function, Runtime
from lambda_forge import Path, track
from lambda_forge.interfaces import IAWSLambda


class AWSLambda(IAWSLambda):
    def __init__(self, scope, context, layers, secrets_manager) -> None:
        self.scope = scope
        self.context = context
        self.layers = layers
        self.secrets_manager = secrets_manager

    @track
    def create_function(
        self,
        name,
        path,
        description,
        directory=None,
        timeout=1,
        layers=[],
        environment={},
    ):

        function = Function(
            scope=self.scope,
            id=name,
            description=description,
            function_name=f"{self.context.stage}-{self.context.name}-{name}",
            runtime=Runtime.PYTHON_3_9,
            handler=Path.handler(directory),
            environment=environment,
            code=Code.from_asset(path=Path.function(path)),
            layers=layers + [self.layers.telegram_layer, self.layers.requests_layer],
            timeout=Duration.minutes(timeout),
        )

        self.secrets_manager.telegram_secret.grant_read(function)

        return function
