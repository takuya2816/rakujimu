import boto3
import json
import time
import os
#from common import (common_const, utils, line)
import logging
from datetime import datetime, timedelta
import requests
from boto3.dynamodb.conditions import Attr
from urllib.parse import urlencode

# 環境変数 Todo:リファクタリング
#REMIND_DATE_DIFFERENCE = int(os.getenv(
#    'REMIND_DATE_DIFFERENCE'))
#LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
#CHANNEL_TYPE = os.environ.get("CHANNEL_TYPE")
#CHANNEL_ID = os.getenv('OA_CHANNEL_ID', None)
LIFF_CHANNEL_ID = '2000948278' #os.getenv('LIFF_CHANNEL_ID', None)

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

# ログ出力の設定
logger = logging.getLogger()

# 共通変数 #Todo:リファクタリング

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

# 共通関数 #Todo：エラー発生中。要テスト（20240414）
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
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "id_token": id_token,
        "client_id": channel_id
    }

    response = requests.post(
        API_USER_ID_URL,
        headers=headers,
        data=body
    )
    
    res_body = json.loads(response.text)
    
    print(res_body)
    
    return res_body

# lineIdからcustomer_idを取得
def get_customer_id(lineId, seqtable, birthday, gender, name, tel):
    table = dynamodb.Table('CustomerMst')

    # lineIdが一致するアイテムをスキャン
    response = table.scan(
        FilterExpression=Attr('line_id').eq(lineId)
    )
    existing_item = response.get('Items')

    if existing_item: # 既存顧客の場合ID取得
        customer_id = existing_item[0]['id']
    else:  # 新規の場合、新しい顧客として登録
        nextseq = get_next_seq(seqtable, 'CustomerMst')
        customer_id = nextseq

        # 新しい顧客情報
        customer_data = {
            'id': nextseq,
            'birthday':birthday,
            'gender': gender,
            'lineId': lineId,
            'name': name,
            'regist_datetime': datetime.now().isoformat(),
            'tel':tel,
        }

        # API GatewayのエンドポイントURL
        api_url = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistCustomerMst'

        # APIリクエストを送信して顧客情報を登録
        response = requests.post(api_url, json=customer_data)
        print(response)

        # レスポンスのステータスコードを確認
        if response.status_code != 200:
            print(f"Error registering customer: {response.text}")
            
    return customer_id

def cal_endtime(reserveStDatetime, service_id):
    table = dynamodb.Table('ServiceMst')
    response = table.get_item(
        Key={
            'id': int(service_id)
        }
    )
    item = response.get('Item')

    reserveStDatetime = datetime.strptime(reserveStDatetime, "%Y%m%d %H:%M")
    service_term = datetime.strptime(item['term'], "%H:%M")
    delta = timedelta(hours=service_term.hour, minutes=service_term.minute)
    reserveEndtime = (reserveStDatetime + delta).strftime("%H:%M")    
    
    return reserveEndtime

# 既存の予約とかぶっていないことをチェック
def check_reservable(reserve_id, reserve_date, reserve_sttime, reserve_endtime):
    reserve_sttime = datetime.strptime(reserve_sttime, "%H:%M")
    reserve_endtime = datetime.strptime(reserve_endtime, "%H:%M")
    reservable_flag = True

    table = dynamodb.Table('ReservationList')
    response = table.scan(
        # 提供予定日が同じで、編集対象予約と削除済予約を除外したものを検査
        FilterExpression=Attr('reserve_date').eq(reserve_date) & Attr('id').ne(reserve_id) & Attr('delete_flag').eq('false')
    )
    for item in response.get('Items', []):
        existing_sttime = datetime.strptime(item['reserve_sttime'], "%H:%M")
        existing_endtime = datetime.strptime(item['reserve_endtime'], "%H:%M")

        # 時間の重複をチェック
        if ((reserve_sttime < existing_endtime and reserve_endtime > existing_sttime) or
            (existing_sttime < reserve_endtime and existing_endtime > reserve_sttime)):
            reservable_flag = False
            break

    return reservable_flag

def lambda_handler(event, context):
    try:
        # パラメータログ、チェック
        logger.info(event)
        
        # フォームに入力されたデータを得る
        param = json.loads(event['body'])
        param = param['params']['data']
        reserveStDatetime = param['reserveStDatetime']

        datetime_obj = datetime.strptime(reserveStDatetime, "%Y%m%d %H:%M")
        reserveDate = datetime_obj.strftime("%Y-%m-%d")
        reserveSttime = datetime_obj.strftime("%H:%M")
        serviceId = param['serviceId']
        approvalFlag = param['approvalFlag']
        deleteFlag = param['deleteFlag']
        employeeId = "" # param['employeeId']
        supplierId = "" # param['supplierId']
        
        birthday = param['birthday']
        gender = param["gender"]
        name = param["name"]
        tel = param['tel']
        memo = param['memo']

        
        # 現在の時刻を取得
        nowtime = time.time()
        timestamp = str(datetime.fromtimestamp(nowtime))
        
        # reserveEndtimeを算出
        reserveEndtime = cal_endtime(reserveStDatetime, serviceId)

        seqtable = dynamodb.Table('sequence')
        if 'customer_id' in param:
            customerId = param['customer_id']
        else:
            # customer_id が含まれていない場合は、lineId から取得
            try:
                user_profile = get_profile(param['idToken'], LIFF_CHANNEL_ID)
                if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
                    return {'statusCode' : 403}
                else:
                    lineId = str(user_profile['sub'])
            except Exception:
                logger.exception('不正なIDトークンが使用されています')
                return {'statusCode' : 403}
            customerId = get_customer_id(lineId, seqtable, birthday, gender, name, tel)            

        table = dynamodb.Table('ReservationList')

        # lineIdとdatetimeで既存の予約を検索
        response = table.scan(
            FilterExpression=Attr('customer_id').eq(customerId) & Attr('reserve_date').eq(reserveDate)
        )
        existing_item = response['Items'][0] if response['Items'] else None
        
        if existing_item:
            if deleteFlag:  # 既存の予約を削除の場合
                response = table.update_item(
                    Key={
                        'id': existing_item['id']
                    },
                    UpdateExpression="set delete_flag = :df, delete_datetime = :ddt",
                    ExpressionAttributeValues={
                        ':df': deleteFlag,
                        ':ddt': timestamp,
                    },
                    ReturnValues="DELETE_ITEM"
                )
            elif approvalFlag:  # 既存の予約を承認する場合
                response = table.update_item(
                    Key={
                        'id': existing_item['id']
                    },
                    UpdateExpression="set approval_flag = :af, approval_datetime = :adt",
                    ExpressionAttributeValues={
                        ':af': approvalFlag,
                        ':adt': timestamp
                    },
                    ReturnValues="UPDATED_NEW"
                )
            else:
                # 既存の予約を更新
                # 既存の予約とかぶっていないことを確認
                if not check_reservable(existing_item['id'], reserveDate, reserveSttime, reserveEndtime):
                    return {
                        "isBase64Encoded": False,
                        "statusCode": 200,
                        "headers": {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Methods': 'POST,GET',
                            'Access-Control-Allow-Origin': '*'
                        },
                        "body": json.dumps({"result": "ng"})
                    }
                
                response = table.update_item(
                    Key={
                        'id': existing_item['id']
                    },
                    UpdateExpression="set reserve_date = :rd, reserve_sttime = :rst, reserve_endtime = :ret, service_id = :s, memo = :m, update_datetime = :u",
                    ExpressionAttributeValues={
                        ':rd': reserveDate,
                        ':rst': reserveSttime,
                        ':ret': reserveEndtime,
                        ':e': "",
                        ':s': serviceId,
                        ':m': memo,
                        ':u': timestamp
                    },
                    ReturnValues="UPDATED_NEW"
                )
        else:            
            # 新しい予約を作成
            nextseq = get_next_seq(seqtable, 'ReservationList')
            table.put_item(
                Item = {
                    'id' : nextseq,
                    'regist_datetime' : timestamp,
                    'reserve_date' : reserveDate,
                    'reserve_sttime' : reserveSttime,
                    'reserve_endtime' : reserveEndtime,
                    'customer_id' : customerId,
                    'delete_flag' : 'false',
                    'service_id' : serviceId,
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
