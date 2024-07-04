import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime
import json
import decimal

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
    

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
            print(customer_ids)
            customer_condition = Attr('id').is_in([int(cust_id) for cust_id in customer_ids])
            filter_expression = customer_condition if filter_expression is None else filter_expression & customer_condition
    
        # スキャンを実行
        if filter_expression is not None:
            customerList = table.scan(
                FilterExpression=filter_expression
            )
        else:
            customerList = table.scan()
        print(customerList)
    
    
        # with_reserve_infoがTrueなら、最終来店日と来店予定日を計算
        if with_reserve_info:
            for record in records:
                # 最終来店日
                past_visits = [datetime.fromisoformat(item['supply_date']) for item in records if item['customer_id'] == record['customer_id'] and datetime.fromisoformat(item['supply_date']) < datetime.now()]
                if past_visits:
                    record['last_visit_date'] = max(past_visits).isoformat()
                else:
                    record['last_visit_date'] = None
    
                # 来店予定日
                future_visits = [datetime.fromisoformat(item['supply_date']) for item in records if item['customer_id'] == record['customer_id'] and datetime.fromisoformat(item['supply_date']) >= datetime.now()]
                if future_visits:
                    record['next_visit_date'] = min(future_visits).isoformat()
                else:
                    record['next_visit_date'] = None
    
            customerList = records
    
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
    
