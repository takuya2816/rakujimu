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
    """
    営業開始時間から営業終了時間までの時間間隔リストを生成する関数

    Args:
        start_time (str): 開始時間
            形式: "HH:MM"
            例: "10:00"
        end_time (str): 終了時間
            形式: "HH:MM"
            例: "20:00"
        time_iter (int): 時間間隔（分）
            例: 15

    Returns:
        list: 時間間隔のリスト
            形式: ["HH:MM", ...]
            例: ["11:00", "11:15", "11:30", ..., "19:45"]

    Examples:
        >>> get_time_intervals("09:00", "10:30", 30)
        ["09:00", "09:30", "10:00"]
    """
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
    """
    指定された日付(1week)に対する営業時間を取得する関数

    Args:
        display_days (list): 表示する日付のリスト
            形式: ["YYYYMMDD", ...]
            例: ["20240130", "20240131", "20240201"]
        time_iter (int): 時間間隔（分）
            例: 15

    Returns:
        dict: 日付ごとの営業時間のリストを含む辞書
            形式: {"YYYYMMDD": ["HH:MM", ...], ...}
            例: {
                "20240130": ["09:00", "09:15", "09:30", ..., "17:45"],
                "20240131": ["09:00", "09:15", "09:30", ..., "17:45"],
                ...
            }

    Note:
        - この関数はDynamoDBの'OpeningHourMst'テーブルからデータを取得します。
        - テーブルには各曜日の営業開始時間と終了時間が格納されていることを前提としています。

    Examples:
        >>> get_opening_hour(["20240130", "20240131"], 30)
        {
            "20240130": ["09:00", "09:30", "10:00", ..., "17:30"],
            "20240131": ["09:00", "09:30", "10:00", ..., "17:30"]
        }
    """
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

def get_service_term(serviceId):
    """
    指定されたサービス名に対応するサービス所要時間を取得する関数

    Args:
        serviceId (str): 予約されたサービスの名前
            例: "カット", "カラー", "パーマ"

    Returns:
        str: サービスの所要時間
            形式: "HH:MM"
            例: "00:30", "01:00", "01:30"

    Raises:
        KeyError: 指定されたサービス名が見つからない場合

    Note:
        - この関数はDynamoDBの'ServiceMst'テーブルからデータを取得します。
        - テーブルには各サービスの名前と所要時間が格納されていることを前提としています。

    Examples:
        >>> get_service_term("haircut")
        "00:30"
        >>> get_service_term("full_coloring")
        "02:00"
    """
    table = dynamodb.Table('ServiceMst')
    response = table.scan()

    service_term = None
    service_list = response.get('Items', [])
    for service in service_list:
        if int(service['id']) ==  int(serviceId):
            service_term = service['term']
    if not service_term:
        raise KeyError(f"Service '{serviceId}' not found in the database")
    return service_term

def get_reserved_list(display_days, time_iter):  # ->{"20240130": ["11:00","12:00"],...}
    """
    指定された日付範囲の予約済み時間リストを取得する関数

    Args:
        display_days (list): 表示する日付のリスト
            形式: ["YYYYMMDD", ...]
            例: ["20240130", "20240131", "20240201"]
        time_iter (int): 時間間隔（分）
            例: 15

    Returns:
        dict: 日付ごとの予約済み時間のリストを含む辞書
            形式: {"YYYYMMDD": ["HH:MM", ...], ...}
            例: {
                "20240130": ["11:00", "11:15", "11:30", "11:45"],
                "20240131": ["14:00", "14:15", "14:30", "14:45"],
                ...
            }

    Note:
        - この関数はDynamoDBの'ReservationList'テーブルからデータを取得します。
        - テーブルには予約の日付（曜日）、開始時間、終了時間が格納されていることを前提としています。
        - 返される時間リストは指定された時間間隔(time_iter)に基づいて生成されます。

    Examples:
        >>> get_reserved_list(["20240130", "20240131"], 15)
        {
            "20240130": ["11:00", "11:15", "11:30", "11:45"],
            "20240131": ["14:00", "14:15", "14:30", "14:45"]
        }
    """
    reserved_dict = {}
    
    # 対象の範囲の予約済データを15分毎の単位で取得
    table = dynamodb.Table('ReservationList')  # TODO:期間指定できたらよりよい
    response = table.scan()
    reserved_datetime_list = response.get('Items', [])
    
    for display_day in display_days:  # Mon~Sunで繰り返し
        times_list = []
        target_date = datetime.datetime.strptime(display_day, '%Y%m%d')
        for reserved_datetime_row in reserved_datetime_list:
            reserve_date = datetime.datetime.strptime(reserved_datetime_row['reserve_date'], "%Y-%m-%d")
            reserve_date = reserve_date.strftime("%Y%m%d")
            if reserve_date == display_day:
                sttime = reserved_datetime_row["reserve_sttime"]
                endtime = reserved_datetime_row["reserve_endtime"]
                times_list.extend(get_time_intervals(sttime, endtime, time_iter))
        reserved_dict[display_day] = sorted(list(set(times_list)))
    return reserved_dict

def get_available_slots(reservable_dict, service_term, time_tier):
    """
    予約可能な時間スロットからサービス提供時間分の空きがある時間を計算する関数

    Args:
        reservable_dict (dict): 日付ごとの予約可能な時間スロットの辞書
            形式: {"YYYYMMDD": ["HH:MM", ...], ...}
            例: {
                "20240130": ["11:00", "11:15", "11:30", "11:45", "12:00"],
                "20240131": ["10:00", "10:15", "10:30", "10:45", "11:00"]
            }
        service_term (str): サービスの所要時間
            形式: "HH:MM"
            例: "00:30"
        time_tier (int): 時間の刻み幅（分）
            例: 15

    Returns:
        dict: 日付ごとのサービス提供可能な開始時間のリストを含む辞書
            形式: {"YYYYMMDD": ["HH:MM", ...], ...}
            例: {
                "20240130": ["11:00", "11:15"],
                "20240131": ["10:00", "10:15"]
            }

    Note:
        - この関数は指定された time_tier 分単位の時間スロットを前提としています。
        - サービス時間が time_tier の倍数でない場合、切り上げて計算されます。
        - 返される時間は、そこからサービス時間分の連続した空きがある開始時間のみです。

    Examples:
        >>> reservable_dict = {
        ...     "20240130": ["11:00", "11:15", "11:30", "11:45", "12:00"],
        ...     "20240131": ["10:00", "10:15", "10:30", "10:45", "11:00"]
        ... }
        >>> get_available_slots(reservable_dict, "00:45", 15)
        {
            "20240130": ["11:00", "11:15"],
            "20240131": ["10:00", "10:15"]
        }
    """
    available_slots = {}
    service_minutes = int(service_term.split(':')[0]) * 60 + int(service_term.split(':')[1])
    for date, slots in reservable_dict.items():
        available_slots[date] = []
        for i, slot in enumerate(slots): 
            slot_time = datetime.datetime.strptime(date + " " + slot, "%Y%m%d %H:%M")  # 日付と時間を合わせる
            
            # slot_timeにtime_tier分ずつ足していき、slotsに該当する時間があるか判定、service_term%15-1回の判定が完了したらavailable_slotsへappend
            is_available = True
            for j in range(1, service_minutes // time_tier):
                check_time = slot_time + timedelta(minutes = time_tier * j)
                check_time_str = check_time.strftime("%H:%M")
                if check_time_str not in slots:
                    is_available = False
                    break

            # 利用可能な場合、スロットを追加
            if is_available:
                available_slots[date].append(slot)
    
    return available_slots
    
def lambda_handler(event, context):
    """
    Lambda関数: 指定された日付範囲とサービスに基づいて予約可能な時間スロットを計算し返す

    Args:
        event (dict): Lambda関数のトリガーイベント
            期待される形式:
            {
                "queryStringParameters": {
                    "data": '{"display_days": ["20240130", "20240131", ...], "serviceId": "1"}'
                }
            }
        context (LambdaContext): Lambda実行コンテキスト（この関数では未使用）

    Returns:
        dict: API Gatewayのレスポンス形式
            成功時:
            {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "POST,GET",
                    "Access-Control-Allow-Origin": "*"
                },
                "body": '{"reservable_dict": {"20240130": ["11:00", "11:30"], ...}}'
            }
            失敗時:
            {
                "statusCode": 500
            }

    Note:
        - この関数は、営業時間、予約済み時間、サービス所要時間を考慮して予約可能な時間を計算します。
        - 時間間隔(time_iter)は現在15分で固定されていますが、将来的に可変にする可能性があります。
        - エラーが発生した場合、詳細なトレースバックがログに出力されます。

    Examples:
        >>> event = {
        ...     "queryStringParameters": {
        ...         "data": '{"display_days": ["20240130", "20240131"], "serviceId": "1"}'
        ...     }
        ... }
        >>> lambda_handler(event, None)
        {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": {...},
            "body": '{"reservable_dict": {"20240130": ["11:00", "11:30"], "20240131": ["10:00", "10:30"]}}'
        }
    """
    try:
        time_iter = 15  # NEXT:どこから持ってくるか
        
        # 表示させる週初日(月曜日)と予約するサービス名の情報を取得
        data = event.get('queryStringParameters')  # ["20240130", "20240131", "20240201"...]
        parsed_data = json.loads(data['data'])
        display_days = parsed_data['display_days']
        serviceId = parsed_data['serviceId']
        
        # 各テーブルから全データを参照する。
        opening_hour_dict = get_opening_hour(display_days, time_iter)
        reserved_dict = get_reserved_list(display_days, time_iter)
        
        # 営業時間から指定週のデータのみを取ってくる
        reservable_dict = {}
        for (open_day, open_times), (reserved_day, reserved_times) in zip(opening_hour_dict.items(), reserved_dict.items()):
            reservable_dict[open_day] = [item for item in open_times if item not in reserved_times]  # {"20240130": ["11:00","12:00"],...}
        
        # サービス提供が可能な時間のみを計算する。
        service_term = get_service_term(serviceId)
        serviceable_dict = get_available_slots(reservable_dict, service_term, time_iter)

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
    