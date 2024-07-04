import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import json
import decimal
import requests

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
    
def getReseavationList(customer_ids_to_query):
    # TODO:equests.exceptions.HTTPError: 403 Client Error: Forbidden for url: https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetUserReservationList?customerId=47%2C1%2C49%2C0%2C48
    api_url = 'https://hx767oydxg.execute-api.ap-northeast-1.amazonaws.com/rakujimu-app-prod/GetUserReservationList'
    api_params = {
        'customerId': ','.join(map(str, customer_ids_to_query)),
    }
    api_response = requests.get(api_url, params=api_params)
    api_response.raise_for_status()  # HTTPエラーが発生した場合に例外をスロー
    return api_response.json().get('Items', [])


def lambda_handler(event, context):
    try:
        # CustomerMst テーブルから全データを参照する。
        table = dynamodb.Table('CustomerMst')

        # パラメータを定義しておく
        customer_ids = False
        with_reserve_info = False
        current_datetime = datetime.now().isoformat()
        
        # レスポンスデータの内、customerIdに値がある場合絞り込みを行う
        data = event.get('queryStringParameters')
        if data:
            parsed_data = json.loads(data['data'])
            customer_ids = parsed_data.get('customerId', False)
            with_reserve_info = parsed_data.get('with_reserve_info', False)
    
         # フィルター条件の初期化
        filter_expression = None
    
        # フィルター条件の組み立て
        if customer_ids:
            customer_condition = Attr('id').is_in([int(cust_id) for cust_id in customer_ids])
            filter_expression = customer_condition if filter_expression is None else filter_expression & customer_condition
    
        # スキャンを実行
        if filter_expression is not None:
            response = table.scan(
                FilterExpression=filter_expression
            )
            customerList = response['Items']
        else:
            response = table.scan()
            customerList = response['Items']
        print(customerList)
    
    
        # with_reserve_infoがTrueなら、最終来店日と来店予定日を計算
        if with_reserve_info:
            customer_ids_to_query = [item['id'] for item in customerList]
            
            # reservation_records = getReseavationList(customer_ids_to_query)  # TODO
            reservation_records = []
            
            print(reservation_records)

            # 最終来店日と来店予定日を計算して追加
            for customer in customerList:
                customer_id = customer['id']
                # 最終来店日
                past_visits = [datetime.fromisoformat(item['supply_date']) for item in reservation_records if item['id'] == customer_id and datetime.fromisoformat(item['supply_date']) < datetime.now()]
                if past_visits:
                    customer['last_visit_date'] = max(past_visits).isoformat()
                else:
                    customer['last_visit_date'] = None

                # 来店予定日
                future_visits = [datetime.fromisoformat(item['supply_date']) for item in reservation_records if item['id'] == customer_id and datetime.fromisoformat(item['supply_date']) >= datetime.now()]
                if future_visits:
                    customer['next_visit_date'] = min(future_visits).isoformat()
                else:
                    customer['next_visit_date'] = None
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
    
