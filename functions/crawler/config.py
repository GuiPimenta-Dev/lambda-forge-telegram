from infra.services import Services

class CrawlerConfig:
    def __init__(self, services: Services) -> None:

        function = services.aws_lambda.create_function(
            name="Crawler",
            path="./functions/crawler",
            description="a url scraper",
            
        )
