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
                if reservation['customer_id'] == customer['customerId']:
                    reservation['customer_name'] = customer
                    break
            for service in serviceMst['Items']:
                if reservation['service_id'] == service['serviceId']:
                    reservation['service_name'] = service
                    break

        # パラメータを取得
        data = event.get('queryStringParameters')  # ["20240130", "20240131", "20240201"...]
        parsed_data = json.loads(data['data'])
        reservationId = parsed_data.get('reservationId', False)

        # レスポンスデータの内、reservationIdに値がある場合絞り込みを行う
        if reservationId:
            response = table.query(
                KeyConditionExpression = 'reservationId = :reservationId',
                ExpressionAttributeValues = {
                    ':reservationId': reservationId
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
            "body": json.dumps(response, cls=DecimalEncoder)
        }
        
    except:
        import traceback
        traceback.print_exc()
        return {
            'statusCode' : 500
        }
    
