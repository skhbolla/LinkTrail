import os
import boto3
from dotenv import load_dotenv

#Use the same secrets the docker compose uses
load_dotenv(dotenv_path=".env")

# Load environment variables
DYNAMO_ENDPOINT = f"http://localhost:{os.getenv("DDB_LOCAL_PORT")}/"
AWS_REGION = os.getenv("AWS_REGION")

print(DYNAMO_ENDPOINT)
print(AWS_REGION)

# Initialize DynamoDB client
dynamodb = boto3.client(
    "dynamodb",
    endpoint_url=DYNAMO_ENDPOINT,
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def create_links_table():

    print("Creating links table")
    table_name = "Links"
    existing_tables = dynamodb.list_tables()["TableNames"]
    if table_name in existing_tables:
        print(f"{table_name} already exists.")
        return
    print("Here")
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "short_code", "KeyType": "HASH"},  # Partition key
        ],
        AttributeDefinitions=[
            {"AttributeName": "short_code", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    print(f"Creating table {table_name}...")
    dynamodb.get_waiter("table_exists").wait(TableName=table_name)
    print(f"Table {table_name} created successfully.")


def create_clicklogs_table():
    table_name = "ClickLogs"
    existing_tables = dynamodb.list_tables()["TableNames"]
    if table_name in existing_tables:
        print(f"{table_name} already exists.")
        return

    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {"AttributeName": "short_code", "KeyType": "HASH"},         # Partition key
            {"AttributeName": "click_timestamp", "KeyType": "RANGE"}  # Sort key
        ],
        AttributeDefinitions=[
            {"AttributeName": "short_code", "AttributeType": "S"},
            {"AttributeName": "click_timestamp", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
    )

    print(f"Creating table {table_name}...")
    dynamodb.get_waiter("table_exists").wait(TableName=table_name)
    print(f"Table {table_name} created successfully.")


if __name__ == "__main__":
    create_links_table()
    create_clicklogs_table()
