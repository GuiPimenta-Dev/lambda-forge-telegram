from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as tasks
from constructs import Construct

class StateMachine:
    def __init__(self, scope: Construct, context) -> None:
        self.scope = scope
        self.context = context
        self.tasks = []
        self.choice_states = []
        self.success_states = []
        self.fail_states = []

    def create_task(self, task_name, function):
        task_name = f"{self.context.stage}-{self.context.name}-{task_name}"
        task = tasks.LambdaInvoke(
            self.scope, 
            task_name, 
            lambda_function=function, 
            output_path="$.Payload",
            retry_on_service_exceptions=False,
            
        )
        self.tasks.append(task)
        return task

    def add_choice(self, name, choices):
        choice_state = sfn.Choice(self.scope, name)
        for condition, next_state in choices:
            choice_state.when(condition, next_state)
        self.choice_states.append(choice_state)
        return choice_state

    def add_success(self, name="Success"):
        success_state = sfn.Succeed(self.scope, name)
        self.success_states.append(success_state)
        return success_state

    def add_fail(self, name="Fail", cause="Unknown Error"):
        fail_state = sfn.Fail(self.scope, name, cause=cause)
        self.fail_states.append(fail_state)
        return fail_state

    def finalize_and_build(self, name, starting_state):
        name = f"{self.context.stage}-{self.context.name}-{name}"
        return sfn.StateMachine(
            self.scope,
            name,
            state_machine_name=name,
            definition=starting_state,
                        
        )

    @staticmethod
    def string_equals(variable, value):
        return sfn.Condition.string_equals(variable, value)
