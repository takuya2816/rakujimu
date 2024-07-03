import boto3
import json
import decimal

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
    
def get_record_by_id(data, record_id):
    # Itemsリストを取得
    items = data.get('Items', [])
    
    # 指定されたIDを持つレコードを検索
    for item in items:
        if int(item.get('id')) == int(record_id):
            return item
    
    # 指定されたIDを持つレコードが見つからない場合、Noneを返す
    return None
    

def lambda_handler(event, context):
    try:
        # ReservationList テーブルから全データを参照する。
        table = dynamodb.Table('ReservationList')
        reservationList = table.scan()

        # CustomerMst, ServiceMst テーブルからデータを参照する
        table = dynamodb.Table('CustomerMst')
        customerMst = table.scan()
        table = dynamodb.Table('ServiceMst')
        serviceMst = table.scan()

        # CustomerMst, ServiceMst テーブルのを付与
        for reservation in reservationList['Items']:
            for customer in customerMst['Items']:
                if reservation['customer_id'] == customer['id']:
                    reservation['customer_name'] = customer['name']
                    break
            for service in serviceMst['Items']:
                if reservation['service_id'] == service['id']:
                    reservation['service_name'] = service['name']
                    break

        # パラメータを取得
        data = event.get('queryStringParameters', False)
        if data:
            # レスポンスデータの内、reservationIdに値がある場合絞り込みを行う
            parsed_data = json.loads(data['data'])
            reservationId = parsed_data.get('reservationId')
            reservationList = get_record_by_id(reservationList, reservationId)
            print(reservationList)

        
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
    
