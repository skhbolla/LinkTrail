import os

class Settings:
    # DynamoDB tables
    DYNAMO_TABLE_LINKS = os.getenv("DYNAMO_TABLE_LINKS")
    DYNAMO_TABLE_CLICKS = os.getenv("DYNAMO_TABLE_CLICKS")

    # AWS configuration
    AWS_REGION = os.getenv("AWS_REGION")
    DYNAMO_ENDPOINT = os.getenv("DYNAMO_ENDPOINT")

    # Base URL for generating full URLs
    BASE_URL = os.getenv("BASE_URL")

settings = Settings()
