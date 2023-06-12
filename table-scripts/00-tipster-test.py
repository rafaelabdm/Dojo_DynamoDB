import boto3
from botocore.exceptions import ClientError
import random

def get_tip_by_id(event, context):
    method = event['HttpMethod']
    tipID = f'{random.randint(1, 3)}'
    # tipID = '1'
    if method != 'GET':
        return {"Error" : "Http Method Not Suported!"}
    try:
		#API dentro da localstack:
        # dynamodb_client = boto3.client("dynamodb", region_name='us-east-1', endpoint_url='http://host.docker.internal:4566/')
		
		#API fora da localstack:
        dynamodb_client = boto3.client("dynamodb", region_name='us-east-1', endpoint_url='http://localhost.localstack.cloud:4566/')
        response = dynamodb_client.query(
        ExpressionAttributeValues={
            ':v1': {
                'N': tipID,
            },
        },
        KeyConditionExpression='TipID = :v1',
        TableName="ProjectsTips",
        )
    except ClientError:
        raise
    else:
        return response['Items'][0]["Project"]["S"] + ": " + response['Items'][0]["Tip"]["S"]


if __name__ == '__main__':
    print(get_tip_by_id(event={"HttpMethod" : "GET"}, context={}))
    