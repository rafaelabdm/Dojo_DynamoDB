import boto3
from botocore.exceptions import ClientError
import random

table_name = 'ProjectsTips'

tips = [
    ["Minishell", "Watch the waitpid"],
    ["So Long", "Don't waste so much time"],
    ["Minishell", "Just breath and test"],
    ["Libft", "Don't rush it, you'll regret it"],
    ["Philosofers", "Watch the CodeVault videos :)"],
    ["Cub3d", "There's a playlist on youtube teaching how to do it"],
]

def populate_table():
    for i in range(0, len(tips)):
        put_item(tips[i], i)

def put_item(item, id):
    try:
        dynamodb_resource = boto3.resource("dynamodb", region_name='us-east-1', endpoint_url='http://localhost.localstack.cloud:4566/')
        table = dynamodb_resource.Table(table_name)
        response = table.put_item(
            Item={
                'Id': id + 1,
                'Project': item[0],
                'Tip': item[1],
            }
        )
    except ClientError:
        raise
    else:
        return response

def get_tip_by_id(event, context):
    method = event['HttpMethod']
    tipID = f'{random.randint(1, len(tips))}'
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
        KeyConditionExpression='Id = :v1',
        TableName=table_name,
        )
    except ClientError:
        raise
    else:
        return response['Items'][0]["Project"]["S"] + ": " + response['Items'][0]["Tip"]["S"]


if __name__ == '__main__':
    # populate_table()
    print(get_tip_by_id(event={"HttpMethod" : "GET"}, context={}))
