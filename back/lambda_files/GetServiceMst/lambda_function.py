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
        # CustomerMst テーブルから全データを参照する。
        table = dynamodb.Table('ServiceMst')
        response = table.scan()

        # パラメータを取得
        data = event.get('queryStringParameters')  # ["20240130", "20240131", "20240201"...]
        parsed_data = json.loads(data['data'])
        customerId = parsed_data.get('customerId', False)

        # レスポンスデータの内、customerIdに値がある場合絞り込みを行う
        if customerId:
            response = table.query(
                KeyConditionExpression = 'customerId = :customerId',
                ExpressionAttributeValues = {
                    ':customerId': customerId
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
    
