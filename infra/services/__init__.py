from infra.services.secrets_manager import SecretsManager
from infra.services.api_gateway import APIGateway
from infra.services.aws_lambda import AWSLambda
from infra.services.layers import Layers
from infra.services.state_machine import StateMachine


class Services:
    def __init__(self, scope, context) -> None:
        self.layers = Layers(scope)
        self.secrets_manager = SecretsManager(scope, context)
        self.api_gateway = APIGateway(scope, context)
        self.aws_lambda = AWSLambda(scope, context, self.layers, self.secrets_manager)
        self.state_machine = StateMachine(scope, context)