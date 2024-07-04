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
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('ReservationList')
        
        reservation_ids = False
        customer_ids = False
        reserved_flg = False
        reserving_flg = False
        data = event.get('queryStringParameters', False)
        if data:  # リクエストパラメータがある場合はレコードを絞り込む
            parsed_data = event.get('queryStringParameters', {})
            reservation_ids = parsed_data.get('reservationId', False)
            customer_ids = parsed_data.get('customerId', False)
            reserved_flg = parsed_data.get('reservedFlg', False)
            reserving_flg = parsed_data.get('reservingFlg', False)

        # フィルター条件の初期化
        filter_expression = None
        current_datetime = datetime.now().isoformat()
        
        print(f"customer_ids:{customer_ids}")
        print(f"reserved_flg:{reserved_flg}")
        print(f"reserving_flg:{reserving_flg}")

        # フィルター条件の組み立て
        if reservation_ids:
            filter_expression &= Attr('id').is_in([int(res_id) for res_id in reservation_ids])
        if customer_ids:
            filter_expression &= Attr('customer_id').is_in([int(cust_id) for cust_id in customer_ids])
        if reserved_flg:
            filter_expression &= Attr('reserved_flg').eq(reserved_flg) & Attr('supply_date').lt(current_datetime)
        if reserving_flg:
            filter_expression &= Attr('reserving_flg').eq(reserving_flg) & Attr('supply_date').gte(current_datetime)

        # フィルター条件がある場合はスキャンを実行
        if filter_expression:
            reservationList = table.scan(
                FilterExpression=filter_expression
            )
        else:
            # フィルター条件がない場合は全てのレコードを取得
            reservationList = table.scan()

        # CustomerMst, ServiceMst テーブルからデータを参照する
        table = dynamodb.Table('CustomerMst')
        customerMst = table.scan()
        table = dynamodb.Table('ServiceMst')
        serviceMst = table.scan()

        # CustomerMst, ServiceMst テーブルの情報を付与
        for reservation in reservationList['Items']:
            for customer in customerMst['Items']:
                if reservation['customer_id'] == customer['id']:
                    reservation['customer_name'] = customer['name']
                    break
            for service in serviceMst['Items']:
                if reservation['service_id'] == service['id']:
                    reservation['service_name'] = service['name']
                    break
            
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
            "body": json.dumps(reservationList, cls=DecimalEncoder)
        }
    except:
        import traceback
        traceback.print_exc()
        return {
            'statusCode' : 500
        }
    
