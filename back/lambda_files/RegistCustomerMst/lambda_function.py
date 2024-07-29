import boto3
import json
import time
import datetime
from boto3.dynamodb.conditions import Attr
import pytz

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

# 連番を採番して返す関数
def get_next_seq(table, tablename):
    response = table.update_item(
        Key = {
            'tablename' : tablename
        },
        UpdateExpression='set seq = seq + :val',
        ExpressionAttributeValues = {
            ':val' : 1
        },
        ReturnValues='UPDATED_NEW'
    )
    return response['Attributes']['seq']

def lambda_handler(event, context):
    try:
        param = json.loads(event['body'])
        print(param)
        table = dynamodb.Table('CustomerMst')
        
        name = param['name']
        gender = param['gender']
        tel = str(param['tel'])
        birthday = param['birthday']
        lineId = param['line_id']
        customerId = param.get('id', None)
        
        jst = pytz.timezone('Asia/Tokyo')
        now = datetime.datetime.now(jst)
        timestamp = now.isoformat()
        
        if customerId!=None:
            # 既存のデータを更新
            response = table.update_item(
                Key={
                    'id': customerId  # プライマリキー 'id' を使用
                },
                UpdateExpression="set #n = :n, gender = :g, tel = :t, birthday = :b, update_datetime = :u",
                ExpressionAttributeNames={
                    '#n': 'name'  # 'name' は予約語なので、プレースホルダーを使用
                },
                ExpressionAttributeValues={
                    ':n': name,
                    ':g': gender,
                    ':t': tel,
                    ':b': birthday,
                    ':u': timestamp
                },
                ReturnValues="UPDATED_NEW"
            )
        else:
            # 新しいデータを作成
            seqtable = dynamodb.Table('sequence')
            customerId = int(get_next_seq(seqtable, 'CustomerMst'))
            print(customerId)
            
            table.put_item(
                Item = {
                    'id' : customerId,
                    'line_id' : lineId,
                    'name' : name,
                    'gender' : gender,
                    'tel' : tel,
                    'birthday' : birthday,
                    'regist_datetime' : timestamp,
                    'update_datetime' : timestamp
                }
            )
        
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,GET',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps({"customerId":customerId, "result":"ok"})  # 2024/07/29 岸変更
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'statusCode' : 500,
            'body': json.dumps({"error": str(e)})
        }