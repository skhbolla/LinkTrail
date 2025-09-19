import os

class Settings:
    #Dynamo Endpoint (Loads only on local runs)
    DYNAMO_ENDPOINT = os.getenv("DYNAMO_ENDPOINT")

    # DynamoDB tables
    DYNAMO_TABLE_LINKS = os.getenv("DYNAMO_TABLE_LINKS")
    DYNAMO_TABLE_CLICKS = os.getenv("DYNAMO_TABLE_CLICKS")

    # AWS configuration
    AWS_REGION = os.getenv("AWS_REGION")

settings = Settings()
