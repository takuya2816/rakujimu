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

def get_service_term(reserved_service):
    table = dynamodb.Table('ServiceMst')
    response = table.scan()

    service_list = response['Item']
    for service in service_list:
        if service['name'] ==  reserved_service:
            service_term = service['term']
            break
    return service_term

def get_reserved_list(display_days, time_iter):  # ->{"20240130": ["11:00","12:00"],...}
    reserved_dict = {}
    table = dynamodb.Table('ReservationList')
    response = table.scan()
    
    # 対象の範囲の予約済データを15分毎の単位で取得
    reserved_datetime_list = response['Item']
    times_list = []
    for display_day in display_days:  # Mon~Sunで繰り返し
        target_dayofweek:str = datetime.datetime.strptime(display_day, '%Y%m%d').strftime('%A')
        for reserved_datetime_row in reserved_datetime_list:
            if reserved_datetime_row['supply_date'] == target_dayofweek:
                sttime = reserved_datetime_row["supply_sttime"]
                endtime = reserved_datetime_row["supply_endtime"]
                times_list = get_time_intervals(sttime, endtime, time_iter)
        reserved_dict[display_day] = times_list
    return reserved_dict

# 予約可能な時間でサービス提供時間分の時間が空いている箇所を計算
def get_available_slots(reservable_dict, service_term): # {"20240130": ["11:00","11:15"],...}, "00:30" ->{"20240130": ["11:00",],...}
    available_slots = {}
    service_minutes = int(service_term.split(':')[0]) * 60 + int(service_term.split(':')[1])
    for date, slots in reservable_dict.items():
        available_slots[date] = []
        for i, slot in enumerate(slots): 
            slot_time = datetime.datetime.strptime(date + " " + slot, "%Y%m%d %H:%M")  # 日付と時間を合わせる
            
            # slot_timeに15分ずつ足していき、slotsに該当する時間があるか判定、service_term%15-1回の判定が完了したらavailable_slotsへappend
            is_available = True
            for j in range(1, service_minutes // 15):
                check_time = slot_time + timedelta(minutes=15 * j)
                check_time_str = check_time.strftime("%H:%M")
                if check_time_str not in slots:
                    is_available = False
                    break

            # 利用可能な場合、スロットを追加
            if is_available:
                available_slots[date].append(slot)

    return available_slots
    
def lambda_handler(event, context):
    try:
        time_iter = 15  # NEXT:どこから持ってくるか
        
        # 表示させる週初日(月曜日)と予約するサービス名の情報を取得
        data = event.get('queryStringParameters')  # ["20240130", "20240131", "20240201"...]
        parsed_data = json.loads(data['data'])
        display_days = parsed_data['display_days']
        reserved_service = parsed_data['reserved_service']
        print(display_days)
        print(reserved_service)        
        
        # 各テーブルから全データを参照する。
        opening_hour_dict = get_opening_hour(display_days, time_iter)
        reserved_dict = get_reserved_list(display_days, time_iter)
        
        # 営業時間から指定週のデータのみを取ってくる
        reservable_dict = {}
        for (open_day, open_times), (reserved_day, reserved_times) in zip(opening_hour_dict.items(), reserved_dict.items()):
            reservable_dict[open_day] = [item for item in open_times if item not in reserved_times]  # {"20240130": ["11:00","12:00"],...}
        
        # サービス提供が可能な時間のみを計算する。
        service_term = get_service_term(reserved_service)
        serviceable_dict = get_available_slots(reservable_dict, service_term)

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
            "body": json.dumps({"reservable_dict":serviceable_dict}, cls=DecimalEncoder)
        }
        
    except:
        import traceback
        traceback.print_exc()
        return {
            'statusCode' : 500
        }
    