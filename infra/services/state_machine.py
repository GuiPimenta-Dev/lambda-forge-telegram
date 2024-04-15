from aws_cdk import aws_secretsmanager as secrets_manager
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as tasks


class StateMachine:
    def __init__(self, scope, context) -> None:
        self.scope = scope
        self.context = context

    def create_task(self, task_name, function):
        task_name = f"{self.context.stage}-{self.context.name}-{task_name.title().replace(' ', '')}"
        return tasks.LambdaInvoke(self.scope, task_name, lambda_function=function, output_path="$.Payload")

    def success(self, task):
        return task.next(sfn.Succeed(self.scope, "Succeed"))

    def create_state_machine(self, name, definition):
        name = f"{self.context.stage}-{self.context.name}-{name}"
        return sfn.StateMachine(
            self.scope,
            name,
            state_machine_name=name,
            definition=definition,
        )
