from botocore.exceptions import ClientError
import boto3

AWS_REGION = 'us-east-1'
AWS_PROFILE = 'localstack'

boto3.setup_default_session(profile_name=AWS_PROFILE)
dynamodb_client = boto3.client("dynamodb", region_name=AWS_REGION, endpoint_url='http://localhost:4566/')

def create_dynamodb_table(table_name):
    try:
        response = dynamodb_client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'AccountID',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'PaymentID',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'AccountID',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'PaymentID',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            },
            Tags=[
                {
                    'Key': 'TableName',
                    'Value': 'BankPayments'
                }
            ])
    except ClientError:
        raise
    else:
        return response

def create_dynamodb_table_GSI_case2(table_name):
    try:
        response = dynamodb_client.update_table(
            TableName=table_name,
            # Any attributes used in your new global secondary index must be declared in AttributeDefinitions
            AttributeDefinitions=[
                {
                    "AttributeName": "SchedualedDate",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "PaymentStatus",
                    "AttributeType": "S"
                },
            ],
            # This is where you add, update, or delete any global secondary indexes on your table.
            GlobalSecondaryIndexUpdates=[
                {
                    "Create": {
                        # You need to name your index and specifically refer to it when using it for queries.
                        "IndexName": "date_by_status-index",
                        # Like the table itself, you need to specify the key schema for an index.
                        # For a global secondary index, you can use a simple or composite key schema.
                        "KeySchema": [
                            {
                                "AttributeName": "SchedualedDate",
                                "KeyType": "HASH"
                            },
                            {
                                "AttributeName": "PaymentStatus",
                                "KeyType": "RANGE"
                            }
                        ],
                        # You can choose to copy only specific attributes from the original item into the index.
                        # You might want to copy only a few attributes to save space.
                        "Projection": {
                            "ProjectionType": "ALL"
                        },
                        # Global secondary indexes have read and write capacity separate from the underlying table.
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 5,
                            "WriteCapacityUnits": 5,
                        }
                    }
                }
            ],
        )
    except ClientError:
        raise
    else:
        return response
    
def create_dynamodb_table_GSI_case1(table_name):
    try:
        response = dynamodb_client.update_table(
            TableName=table_name,
            AttributeDefinitions=[
                {
                    "AttributeName": "StatusAccountID",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "SchedualedDate",
                    "AttributeType": "S"
                },
            ],
            GlobalSecondaryIndexUpdates=[
                {
                    "Create": {
                        "IndexName": "schedualed_user_by_date-index",
                        "KeySchema": [
                            {
                                "AttributeName": "StatusAccountID",
                                "KeyType": "HASH"
                            },
                            {
                                "AttributeName": "SchedualedDate",
                                "KeyType": "RANGE"
                            }
                        ],
                        "Projection": {
                            "ProjectionType": "ALL"
                        },
                        "ProvisionedThroughput": {
                            "ReadCapacityUnits": 5,
                            "WriteCapacityUnits": 5,
                        }
                    }
                }
            ],
        )
    except ClientError:
        raise
    else:
        return response

def main():
    table_name = 'BankPayments'
    # create_dynamodb_table(table_name)
    # create_dynamodb_table_GSI_case2(table_name)
    create_dynamodb_table_GSI_case1(table_name)

if __name__ == '__main__':
    main()