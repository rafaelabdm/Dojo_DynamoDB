import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


AWS_REGION = 'us-east-1'
AWS_PROFILE = 'localstack'

boto3.setup_default_session(profile_name=AWS_PROFILE)

def read_dynamodb_table_item_by_accountid(table_name, accountID):
    try:
        dynamodb_client = boto3.client("dynamodb", region_name=AWS_REGION, endpoint_url='http://localhost:4566')
        response = dynamodb_client.query(
        ExpressionAttributeValues={
            ':v1': {
                'S': accountID,
            },
        },
        KeyConditionExpression='AccountID = :v1',
        TableName=table_name,
        )
    except ClientError:
        raise
    else:
        return response

def read_dynamodb_table_item_case2(table_name, schedualedDate, status):
    try:
        dynamodb_client = boto3.resource("dynamodb", region_name=AWS_REGION, endpoint_url='http://localhost:4566')
        table = dynamodb_client.Table(table_name)
        response = table.query(
            # Add the name of the index you want to use in your query.
            IndexName="date_by_status-index",
            KeyConditionExpression=Key('SchedualedDate').eq(schedualedDate) & Key('PaymentStatus').eq(status),
        )
    except ClientError:
        raise
    else:
        return response
    
def read_dynamodb_table_item_case1(table_name, statusAccountID, currentDay, ninetyDaysLater):
    try:
        dynamodb_client = boto3.resource("dynamodb", region_name=AWS_REGION, endpoint_url='http://localhost:4566')
        table = dynamodb_client.Table(table_name)
        response = table.query(
            # Add the name of the index you want to use in your query.
            IndexName="schedualed_user_by_date-index",
            # KeyConditionExpression=Key('StatusAccountID').eq(statusAccountID) & Key('SchedualedDate').between('20230912', '20231212'),
            KeyConditionExpression=Key('StatusAccountID').eq(statusAccountID) & Key('SchedualedDate').between(currentDay, ninetyDaysLater),
        )
    except ClientError:
        raise
    else:
        return response
    
def main():
    table_name = 'BankPayments'
    accountID = '00000'
    paymentID = '00000000'
    schedualedDate = '20230602' #aaaammdd
    status = 'schedualed'
    dataBlob = 'some data'
    statusAccountID = f'{status}#{accountID}'
    # EXEMPLOS DE FILTRO
    currentDay = '20230529'
    ninetyDaysLater = '20230827'

    response = read_dynamodb_table_item_by_accountid(table_name, accountID)
    # response = read_dynamodb_table_item_case2(table_name, schedualedDate, status)
    # response = read_dynamodb_table_item_case1(table_name, statusAccountID, currentDay, ninetyDaysLater)
    print(response['Items'])

if __name__ == '__main__':
    main()