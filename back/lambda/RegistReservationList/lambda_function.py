import boto3
import json
import time
import os
#from common import (common_const, utils, line)
import logging
import datetime
import requests

# 環境変数
#REMIND_DATE_DIFFERENCE = int(os.getenv(
#    'REMIND_DATE_DIFFERENCE'))
#LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
#CHANNEL_TYPE = os.environ.get("CHANNEL_TYPE")
#CHANNEL_ID = os.getenv('OA_CHANNEL_ID', None)
LIFF_CHANNEL_ID = 2000948278-yXl6L5MR #os.getenv('LIFF_CHANNEL_ID', None)

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

# ログ出力の設定
logger = logging.getLogger()

# 共通変数
API_USER_ID_URL = 'https://api.line.me/oauth2/v2.1/verify'

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

# 共通関数
def get_profile(id_token, channel_id):
    """
    プッシュメッセージ送信処理
    Parameters
    id_token:str
        IDトークン
    channel_id:dict
        使用アプリのLIFFチャネルID
    Returns
    -------
    res_body:dict
        レスポンス情報
    """
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'id_token': id_token,
        'client_id': channel_id
    }

    response = requests.post(
        API_USER_ID_URL,
        headers=headers,
        data=body
    )
    
    res_body = json.loads(response.text)
    return res_body

def lambda_handler(event, context):
    try:
        # パラメータログ、チェック
        logger.info(event)
        #body = json.loads(event['body'])
        #if body is None:
        #    error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        #    return utils.create_error_response(error_msg_display, 400)
    
        # シーケンスデータを得る
        seqtable = dynamodb.Table('sequence')
        nextseq = get_next_seq(seqtable, 'ReservationList')
        
        ## フォームに入力されたデータを得る
        param = json.loads(event['body'])
        
        #ユーザーID取得
        try:
            user_profile = get_profile(
                param['idToken'], LIFF_CHANNEL_ID)
            if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
                return {
                    'statusCode' : 403
                }
            else:
                lineid = user_profile['sub']
        except Exception:
            logger.exception('不正なIDトークンが使用されています')
            return {
                'statusCode' : 403
            }

        datetime = param['datetime']
        resist_reserve_date = param['resist_datetime']
        employee = "" # param['employee']
        serviceid = param['serviceid']
        memo = param['memo']
        
        # 現在の時刻を取得
        nowtime = time.time()
        timestamp = datetime.datetime.fromtimestamp(nowtime)
        # CustomerMst テーブルに登録する
        table = dynamodb.Table('ReservationList')
        table.put_item(
            Item = {
                'id' : nextseq,
                'resist_reserve_date' : resist_reserve_date,
                'reserve_date' : datetime,
                'line_id' : lineid,
                'employee_id' : employee,
                'service_id' : serviceid,
                'approval_flag' : 'false',
                'memo' : memo,
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
