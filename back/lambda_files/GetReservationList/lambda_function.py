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
        
        reservation_id = False
        customer_id = False
        reserved_flag = False
        reserving_flag = False
        
        data = event.get('queryStringParameters', False)
        print(data)
        if data:  # リクエストパラメータがある場合はレコードを絞り込む
            reservation_id = data.get('reservation_id', False)
            customer_id = data.get('customer_id', False)
            # reserved_flag = data.get('reserved_flag', False)
            # reserving_flag = data.get('reserving_flag', False)

        # フィルター条件の初期化
        filter_expression = Attr('delete_flag').eq("false")  # stringでの
        current_datetime = datetime.now().isoformat()
        
        # print(f"reserved_flg:{reserved_flg}")  # テスト
        # print(f"reserving_flg:{reserving_flg}")  # テスト

        # フィルター条件の組み立て  TODO:list処理からの
        if reservation_id is not False:
            reservation_condition = Attr('id').eq(int(reservation_id))
            filter_expression = filter_expression & reservation_condition if filter_expression else reservation_condition
        if customer_id is not False:
            customer_condition = Attr('customer_id').eq(int(customer_id))
            filter_expression = filter_expression & customer_condition if filter_expression else customer_condition
        # if reserved_flg:
        #     reserved_condition = Attr('reserved_flg').eq(reserved_flg) & Attr('reserve_date').lt(current_datetime)
        #     filter_expression = filter_expression & reserved_condition if filter_expression else reserved_condition
        # if reserving_flg:
        #     reserving_condition = Attr('reserving_flg').eq(reserving_flg) & Attr('reserve_date').gte(current_datetime)
        #     filter_expression = filter_expression & reserving_condition if filter_expression else reserving_condition
        print(filter_expression)

        # フィルター条件がある場合はスキャンを実行
        if filter_expression:
            reservationList = table.scan(
                FilterExpression=filter_expression
            )
        else:
            # フィルター条件がない場合は全てのレコードを取得
            reservationList = table.scan()
        print(reservationList)

        # CustomerMst, ServiceMst テーブルからデータを参照する
        table = dynamodb.Table('CustomerMst')
        customerMst = table.scan()
        table = dynamodb.Table('ServiceMst')
        serviceMst = table.scan()
        print(serviceMst)

        # CustomerMst, ServiceMst テーブルの情報を付与
        for reservation in reservationList['Items']:
            for customer in customerMst['Items']:
                if int(reservation['customer_id']) == int(customer['id']):
                    reservation['customer_name'] = customer['name']
                    break
            for service in serviceMst['Items']:
                if int(reservation['service_id']) == int(service['id']):
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
    
