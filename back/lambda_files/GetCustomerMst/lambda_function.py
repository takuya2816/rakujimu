import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import json
import decimal
import requests
# import pytz

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
    
def getReseavationList(customerIds):
    api_url = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetReservationList'
    
    data = json.dumps({'customer_id': customerIds})
    api_params = {'data': data}
    
    api_response = requests.get(api_url, params=api_params)
    api_response.raise_for_status()  # HTTPエラーが発生した場合に例外をスロー
    return api_response.json().get('Items', [])


def lambda_handler(event, context):
    try:
        # CustomerMst テーブルから全データを参照する。
        table = dynamodb.Table('CustomerMst')

        # パラメータを定義しておく
        customerIds = False
        withReserveInfo = False
        
        # レスポンスデータの内、customerIdに値がある場合絞り込みを行う
        data = event.get('queryStringParameters')
        if data:
            customerId = data.get('customer_id', False)
            withReserveInfo = data.get('withReserveInfo', False)
    
         # フィルター条件の初期化
        filterExpression = None
    
        # フィルター条件の組み立て
        print(customerId)
        if customerId is not False:
            customer_condition = Attr('id').eq(int(customerId))
            filterExpression = filterExpression & customer_condition if filterExpression else customer_condition
    
        # スキャンを実行
        if filterExpression is not None:
            response = table.scan(
                FilterExpression=filterExpression
            )
            customerList = response['Items']
        else:
            response = table.scan()
            customerList = response['Items']
    
    
        # withReserveInfoがTrueなら、最終来店日と来店予定日を計算
        if withReserveInfo:
            # jst = pytz.timezone('Asia/Tokyo')
            # date_now = datetime.now(jst)
            date_now = datetime.now()
            
            customerIds = [int(item['id']) for item in customerList]
            reservationList = getReseavationList(customerIds)
            
            # 最終来店日と来店予定日を計算して追加
            for customer in customerList:
                customer_id = customer['id']
        
                # 最終来店日
                past_visits = [(datetime.fromisoformat(item['reserve_date']), item['reserve_sttime']) for item in reservationList if int(item['customer_id']) == int(customer_id) and datetime.fromisoformat(item['reserve_date']) < date_now]
                print(past_visits)
                if past_visits:
                    # 最大の日付を持つ予約日時と開始時間を取得
                    last_reservation = max(past_visits, key=lambda x: x[0])
                    customer['last_reserved_date'] = last_reservation[0].isoformat()
                    customer['last_reserved_sttime'] = last_reservation[1]
                else:
                    customer['last_reserved_date'] = None
                    customer['last_reserved_sttime'] = None

                # 来店予定日
                future_visits = [(datetime.fromisoformat(item['reserve_date']), item['reserve_sttime']) for item in reservationList if int(item['customer_id']) == int(customer_id) and datetime.fromisoformat(item['reserve_date']) >= date_now]
                if future_visits:
                    print(future_visits)
                    next_reservation = min(future_visits, key=lambda x: x[0])
                    customer['next_reserved_date'] = next_reservation[0].isoformat()
                    customer['next_reserved_sttime'] = next_reservation[1]
                else:
                    customer['next_reserved_date'] = None
                    customer['next_reserved_sttime'] = None
        print(customerList)
    
        # 結果を返す
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET',
                'Access-Control-Allow-Origin': '*'
            },
            "body": json.dumps(customerList, cls=DecimalEncoder)
        }
    except:
        import traceback
        traceback.print_exc()
        return {
            'statusCode' : 500
        }
    
