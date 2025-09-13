import boto3
from app.core.settings import settings

# You only need endpoint_url when connecting to a non-standard DynamoDB endpoint

# Connect to DynamoDB
if settings.DYNAMO_ENDPOINT:
    # Local DynamoDB (Docker Compose)
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=settings.DYNAMO_ENDPOINT,
        region_name=settings.AWS_REGION
    )
else:
    # Production AWS DynamoDB
    # boto3 automatically connects to AWS DynamoDB in the cloud without needing an endpoint
    # It uses IAM credentials provided by the environment (lambda)
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION
    )

# Reference tables
links_table = dynamodb.Table(settings.DYNAMO_TABLE_LINKS)
clicks_table = dynamodb.Table(settings.DYNAMO_TABLE_CLICKS)
