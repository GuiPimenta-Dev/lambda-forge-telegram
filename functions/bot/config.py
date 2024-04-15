from infra.services import Services
from aws_cdk import aws_iam
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as task


class BotConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Bot",
            path="./functions/bot",
            description="Telegram webhook",
        )

        services.api_gateway.create_endpoint("POST", "/bot", function, public=True)
        
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
        start_task = stm.create_task("StartCommandTask", start_function)
        test_task = stm.create_task("TestCommandTask", test_function)
        
        choice_state = sfn.Choice(self.scope, "CommandChoice")

        # Adding conditions based on the command received
        choice_state.when(sfn.Condition.string_equals("$.text", "/start"), start_task)
        choice_state.when(sfn.Condition.string_equals("$.text", "/test"), test_task)

        # Default to a fail state if an unknown command is received
        fail_state = sfn.Fail(self.scope, "Fail", cause="Invalid Command")
        choice_state.otherwise(fail_state)

        # Your initial task should lead to the choice state
        definition = task.next(choice_state)
        
        bot_stm = stm.create_state_machine("Bot-STM", definition)
        
        bot_stm.grant_start_execution(function)
        
        function.add_environment("STATE_MACHINE_ARN", bot_stm.state_machine_arn)

        