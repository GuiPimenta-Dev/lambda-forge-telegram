from functions.crawler.config import CrawlerConfig
from functions.test.config import TestConfig
from functions.start.config import StartConfig
from functions.bot.config import BotConfig
from aws_cdk import Stack
from constructs import Construct
from infra.services import Services
from lambda_forge import release


@release
class LambdaStack(Stack):
    def __init__(self, scope: Construct, context, **kwargs) -> None:

        super().__init__(scope, f"{context.stage}-{context.name}-Lambda-Stack", **kwargs)

        self.services = Services(self, context)

        # Bot
        BotConfig(self.services)

        # Crawler
        CrawlerConfig(self.services)
