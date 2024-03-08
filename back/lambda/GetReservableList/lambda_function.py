import boto3
import json
import decimal
import datetime
from datetime import timedelta

# DynamoDBオブジェクト
dynamodb = boto3.resource('dynamodb')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)
        
def get_time_intervals(start_time, end_time, time_iter):
    start = datetime.datetime.strptime(start_time, "%H:%M")
    end = datetime.datetime.strptime(end_time, "%H:%M")
    
    # 結果を格納するリスト
    time_intervals = []
    current = start
    while current < end:
        # 時刻を "HH:MM" 形式でリストに追加
        time_intervals.append(current.strftime("%H:%M"))
        current += timedelta(minutes=time_iter)
    return time_intervals


def get_opening_hour(display_days, time_iter):  # ->{"20240130": ["11:00","12:00"],...}
    opening_hour_dict = {}
    # match_dict = {1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 0:'Sunday'}  # 表示日の曜日と営業日DBの曜日が一致したら
    
    table = dynamodb.Table('OpeningHourMst')
    response = table.scan()
    
    dayofweek_list = response['Items']  # {"id", "dayofweek", "BusinessStartTime", "BusinessEndTime"}のリスト
    times_list = []
    for display_day in display_days:  # Mon~Sunで繰り返し
        target_dayofweek:str = datetime.datetime.strptime(display_day, '%Y%m%d').strftime('%A')
        for dayofweek_row in dayofweek_list:
            if dayofweek_row["dayofweek"] == target_dayofweek:  # Mondayなどの文字列で一致したら
                sttime = dayofweek_row["BusinessStartTime"]
                endtime = dayofweek_row["BusinessEndTime"]
                times_list = get_time_intervals(sttime, endtime, time_iter)
        opening_hour_dict[display_day] = times_list
    return opening_hour_dict


def get_reserved_list(display_days, time_iter):  # ->{"20240130": ["11:00","12:00"],...}
    reserved_dict = {}
    table = dynamodb.Table('ReservationList')
    response = table.scan()
    
    # TODO:対象の範囲の予約済データを15分毎の単位で取得
    for display_day in display_days:
        reserved_dict[display_day] = ["11:00","12:00"]  # test
    return reserved_dict

    
def lambda_handler(event, context):
    try:
        time_iter = 15  # NEXT:どこから持ってくるか
        
        # 表示させる週初日の情報を取得
        data = event.get('queryStringParameters')  # ["20240130", "20240131", "20240201"...]
        json_str = data['data']
        parsed_data = json.loads(json_str)
        display_days = parsed_data['display_days']
        print(display_days)
        
        # 各テーブルから全データを参照する。
        opening_hour_dict = get_opening_hour(display_days, time_iter)
        reserved_dict = get_reserved_list(display_days, time_iter)
        
        # 営業時間から指定週のデータのみを取ってくる
        reservable_dict = {}
        for (open_day, open_times), (reserved_day, reserved_times) in zip(opening_hour_dict.items(), reserved_dict.items()):
            reservable_dict[open_day] = [item for item in open_times if item not in reserved_times]  # {"20240130": ["11:00","12:00"],...}
        
        
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
            "body": json.dumps({"reservable_dict":reservable_dict}, cls=DecimalEncoder)
        }
        
    except:
        import traceback
        traceback.print_exc()
        return {
            'statusCode' : 500
        }
    