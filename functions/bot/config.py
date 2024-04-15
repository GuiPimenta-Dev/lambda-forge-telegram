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

        services.api_gateway.create_endpoint("POST", "/bot", bot_function, public=True)

        start_function = services.aws_lambda.create_function(
            name="StartCommand",
            path="./functions/start",
            description="Handle /start command",
        )

        test_function = services.aws_lambda.create_function(
            name="TestCommand",
            path="./functions/test",
            description="Handle /test command",
        )
        
        stm = services.state_machine

        # Create tasks (Lambda functions already defined)
        task1 = stm.create_task("HandleStart", start_function)
        task2 = stm.create_task("HandleTest", test_function)

        # Define choice state
        choice = stm.add_choice(
            "CommandChoice", [
                (stm.string_equals("$.command", "/start"), task1),
                (stm.string_equals("$.command", "/test"), task2)
            ],
        )
        
        # Finalize and build the state machine
        state_machine = stm.finalize_and_build("MyStateMachine", choice)

        state_machine.grant_start_execution(bot_function)
        
        bot_function.add_environment("STATE_MACHINE_ARN", state_machine.state_machine_arn)