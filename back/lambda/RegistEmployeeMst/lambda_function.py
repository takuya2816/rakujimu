import boto3
import json
import time
import datetime

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
        # シーケンスデータを得る
        seqtable = dynamodb.Table('sequence')
        nextseq = get_next_seq(seqtable, 'EmployeeMst')
        
        ## フォームに入力されたデータを得る
        param = json.loads(event['body'])
        employeeid = param['id']
        lineid = param['lineid']
        name = param['name']
        gender = param['gender']
        mailaddress = param['mailaddress']
        date = param['date']
        
        # 現在の時刻を取得
        nowtime = time.time()
        timestamp = datetime.datetime.fromtimestamp(nowtime)
        # EmployeeMst テーブルに登録する
        table = dynamodb.Table('EmployeeMst')
        table.put_item(
            Item = {
                'id' : nextseq,
                'employee_id' : employeeid,
                'line_id' : lineid,
                'name' : name,
                'gender' : gender,
                'mailaddress' : mailaddress,
                'date' : date,
                'update_datetime' : str(timestamp)
            }
        )
        
        # 結果を返す
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
        
    except:
        import traceback
        traceback.print_exc()
        return {
            'statusCode' : 500
        }
