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
        # CustomerMst テーブルから全データを参照する。
        table = dynamodb.Table('CustomerMst')
        customerList = table.scan()

        # レスポンスデータの内、customerIdに値がある場合絞り込みを行う
        data = event.get('queryStringParameters')
        if data:
            parsed_data = json.loads(data['data'])
            customerId = parsed_data.get('customerId', False)
            customerList = get_record_by_id(customerList, customerId)
        
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
    
