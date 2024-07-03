import boto3
import json
import time
import datetime
from boto3.dynamodb.conditions import Attr

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
        lineid = param['lineid']
        
        table = dynamodb.Table('CustomerMst')
        
        # line_idでスキャンして既存のデータを確認. 1000項目以上になったときはパフォーマンスチューニング必須
        response = table.scan(
            FilterExpression=Attr('line_id').eq(lineid)
        )
        items = response.get('Items', [])
        existing_item = items[0] if items else None
        
        name = param['name']
        address = param.get('address', 'None')
        gender = param['gender']
        phonenumber = str(param['phonenumber'])
        date = param['date']
        
        nowtime = time.time()
        timestamp = str(datetime.datetime.fromtimestamp(nowtime))
        
        if existing_item:
            # 既存のデータを更新
            response = table.update_item(
                Key={
                    'id': existing_item['id']  # プライマリキー 'id' を使用
                },
                UpdateExpression="set line_id = :l, #n = :n, gender = :g, tel = :t, birthday = :b, update_datetime = :u",
                ExpressionAttributeNames={
                    '#n': 'name'  # 'name' は予約語なので、プレースホルダーを使用
                },
                ExpressionAttributeValues={
                    ':l': lineid,
                    ':n': name,
                    ':g': gender,
                    ':t': phonenumber,
                    ':b': date,
                    ':u': timestamp
                },
                ReturnValues="UPDATED_NEW"
            )
        else:
            # 新しいデータを作成
            seqtable = dynamodb.Table('sequence')
            nextseq = get_next_seq(seqtable, 'CustomerMst')
            
            table.put_item(
                Item = {
                    'id' : nextseq,
                    'line_id' : lineid,
                    'name' : name,
                    'gender' : gender,
                    'tel' : phonenumber,
                    'birthday' : date,
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
            "body": json.dumps({"result":"ok"})
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            'statusCode' : 500,
            'body': json.dumps({"error": str(e)})
        }