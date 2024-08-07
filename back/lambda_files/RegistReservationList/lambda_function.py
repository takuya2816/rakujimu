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
import pytz

# 環境変数
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
    response = table.scan(
        FilterExpression=Attr('line_id').eq(lineId)
    )
    existing_item = response.get('Items')

    if existing_item: # 既存顧客の場合はIDを取得
        customer_id = existing_item[0]['id']
    else:  # 新規の場合は新しい顧客として登録
        customer_data = {
            'birthday':birthday,
            'gender': gender,
            'line_id': lineId,
            'name': name,
            'regist_datetime': datetime.now().isoformat(),
            'tel':tel,
        }

        # API GatewayのエンドポイントURL
        api_url = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/RegistCustomerMst'

        # APIリクエストを送信して顧客情報を登録
        response = requests.post(api_url, json=customer_data)
        print(response)
        response_json = response.json()
        customer_id = response_json['customerId']

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

    reserveStDatetime = datetime.strptime(reserveStDatetime, "%Y-%m-%d %H:%M")
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
        
        ### フォームに入力されたデータを得る
        param = json.loads(event['body'])
        print(param)
        serviceId = param['service_id']
        approvalFlag = param['approval_flag']
        deleteFlag = param['delete_flag']
        employeeId = "" # param['employee_id']
        supplierId = "" # param['supplier_id']
        
        # 予約基本情報　新規予約の場合は値が入る
        birthday = param.get('birthday', None)
        gender = param.get("gender", None)
        name = param.get("name", None)
        tel = param.get('tel', None)
        memo = param.get('memo', None)
        
        # 承認・削除の場合
        approvalChangeFlag = param.get('approval_change_flag')
        deleteChangeFlag = param.get('delete_change_flag')

        # 予約日付　予約編集の場合は値が入る
        reservationId = param.get('id',None)
        print(reservationId)
        reserveDate = param.get('reserve_date', None)
        reserveSttime = param.get('reserve_sttime', None)
        
        # 予約日付　新規予約の場合
        if not reserveDate:
            reserveStDatetime = param['reserve_st_datetime']
            datetime_obj = datetime.strptime(reserveStDatetime, "%Y%m%d %H:%M")
            reserveDate = datetime_obj.strftime("%Y-%m-%d")
            reserveSttime = datetime_obj.strftime("%H:%M")
        
        # 現在の時刻を取得
        jst = pytz.timezone('Asia/Tokyo')
        now = datetime.now(jst)
        timestamp = now.isoformat()
        
        # reserveEndtimeを算出
        reserveEndtime = cal_endtime(reserveDate+" "+reserveSttime, serviceId)
        
        ### customer_idを取得
        if reservationId:  # 予約編集の場合
            table = dynamodb.Table('ReservationList')
            response = table.scan(FilterExpression=Attr('id').eq(reservationId))
            reservation = response['Items'][0] if response['Items'] else None
            customerId = int(reservation['customer_id'])
        else:  # 新規の場合
            seqtable = dynamodb.Table('sequence')
            try:
                user_profile = get_profile(param['id_token'], LIFF_CHANNEL_ID)
                if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
                    return {'statusCode' : 403}
                else:
                    lineId = str(user_profile['sub'])
            except Exception:
                logger.exception('不正なIDトークンが使用されています')
                return {'statusCode' : 403}
            customerId = get_customer_id(lineId, seqtable, birthday, gender, name, tel)  # customerMstへの登録も行う        


        ### ReservationListへの登録・更新
        if reservationId:  # 更新の場合
            table = dynamodb.Table('ReservationList')
            if deleteChangeFlag=="true":  # 既存の予約を削除する場合
                print(f"delete:{deleteFlag}")
                response = table.update_item(
                    Key={
                        'id': int(reservationId)
                    },
                    UpdateExpression="set delete_flag = :df, delete_datetime = :ddt",
                    ExpressionAttributeValues={
                        ':df': deleteFlag,
                        ':ddt': timestamp,
                    },
                    ReturnValues="ALL_NEW"
                )
            elif approvalChangeFlag=="true":  # 既存の予約を承認する場合
                print(f"approvalFlag:{approvalFlag}")
                response = table.update_item(
                    Key={
                        'id': reservationId
                    },
                    UpdateExpression="set approval_flag = :af, approval_datetime = :adt",
                    ExpressionAttributeValues={
                        ':af': approvalFlag,
                        ':adt': timestamp
                    },
                    ReturnValues="UPDATED_NEW"
                )
            else:  # 既存の予約を更新する場合
                if not check_reservable(reservationId, reserveDate, reserveSttime, reserveEndtime):
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
                        'id': reservationId
                    },
                    UpdateExpression="set reserve_date = :rd, reserve_sttime = :rst, reserve_endtime = :ret, service_id = :s, memo = :m, update_datetime = :u",
                    ExpressionAttributeValues={
                        ':rd': reserveDate,
                        ':rst': reserveSttime,
                        ':ret': reserveEndtime,
                        ':s': serviceId,
                        ':m': memo,
                        ':u': timestamp
                    },
                    ReturnValues="UPDATED_NEW"
                )
        else:  # 新規の場合
            table = dynamodb.Table('ReservationList')
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
