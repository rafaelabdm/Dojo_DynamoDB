import boto3
from botocore.exceptions import ClientError

AWS_REGION = 'us-east-1'
AWS_PROFILE = 'localstack'

boto3.setup_default_session(profile_name=AWS_PROFILE)

def delete_dynamodb_table_item(table_name, accoutID, paymentID):
    dynamodb_resource = boto3.resource("dynamodb", region_name=AWS_REGION, endpoint_url='http://localhost:4566')
    try:
        table = dynamodb_resource.Table(table_name)
        response = table.delete_item(
            Key={
                'AccountID': accoutID,
                'PaymentID': paymentID
            }
        )
    except ClientError:
        raise
    else:
        return response

def main():
    table_name = 'BankPayments'
    accoutID = '00000'
    paymentID = '00000001'
    schedualDate = '20230602' #aaaammdd
    status = 'schedualed'
    dataBlob = 'some data'
    statusAccountID = f'{status}#{accoutID}'
    dynamodb = delete_dynamodb_table_item(table_name, accoutID, paymentID)
    print(dynamodb)

if __name__ == '__main__':
    main()