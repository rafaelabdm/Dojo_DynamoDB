import boto3
from botocore.exceptions import ClientError
AWS_REGION = 'us-east-1'
AWS_PROFILE = 'localstack'

boto3.setup_default_session(profile_name=AWS_PROFILE)
dynamodb_resource = boto3.resource(
    "dynamodb", region_name=AWS_REGION, endpoint_url='http://localhost:4566')

def add_dynamodb_table_item(table_name, accountID, paymentID , schedualDate, status, dataBlob, statusAccountID):
    try:
        table = dynamodb_resource.Table(table_name)
        response = table.put_item(
            Item={
                'AccountID': accountID, #variavel
                'PaymentID': paymentID, #variavel
                'SchedualedDate': schedualDate, #variavel
                'PaymentStatus': status,
                'DataBlob': dataBlob,
                'StatusAccountID': statusAccountID
            }
        )
    except ClientError:
        raise
    else:
        return response

def main():
    table_name = 'BankPayments'
    accountID = '11111'
    paymentID = '00000000'
    schedualDate = '20230602' #aaaammdd
    status = 'schedualed'
    dataBlob = 'some data'
    statusAccountID = f'{status}#{accountID}'
    add_dynamodb_table_item(table_name, accountID, paymentID ,schedualDate, status, dataBlob, statusAccountID)

if __name__ == '__main__':
    main()