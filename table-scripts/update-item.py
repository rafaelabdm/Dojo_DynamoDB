import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'
AWS_PROFILE = 'localstack'

boto3.setup_default_session(profile_name=AWS_PROFILE)
dynamodb_resource = boto3.client(
    "dynamodb", region_name=AWS_REGION, endpoint_url='http://localhost:4566')

def update_dynamodb_table_item(table_name, accountId, paymentID, newStatus, newStatusAccountID):
    try:
        # table = dynamodb_resource.Table(table_name)
        response = dynamodb_resource.update_item(
            TableName = table_name,
            ExpressionAttributeNames={
            '#S': 'PaymentStatus',
            '#SA': 'StatusAccountID'
            },
            ExpressionAttributeValues={
                ':s': {
                    'S': newStatus
                },
                ':sa': {
                    'S': newStatusAccountID
                },
            },
            Key={
                'AccountID': {
                    'S': accountId,
                },
                'PaymentID': {
                    'S': paymentID,
                },
            },
            ReturnValues='ALL_NEW',
            UpdateExpression='SET #S = :s, #SA = :sa'
        )
    except ClientError:
        raise
    else:
        return response

def main():
    table_name = 'BankPayments'
    accoutID = '00000'
    paymentID = '00000000'
    schedualDate = '20230602' #aaaammdd
    status = 'schedualed'
    dataBlob = 'some data'
    statusAccountID = f'{status}#{accoutID}'

    newStatus = 'pending'
    newStatusAccountID =  f'{newStatus}#{accoutID}'
    dynamodb = update_dynamodb_table_item(table_name, accoutID, paymentID, newStatus, newStatusAccountID)
    print(dynamodb)

if __name__ == '__main__':
    main()
