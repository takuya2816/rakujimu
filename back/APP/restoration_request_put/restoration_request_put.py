import logging
import json
import os
import sys
from datetime import (datetime, timedelta)
from common import (common_const, utils, line)
# from validation import params_check as validation
# DynamoDB操作クラスのインポート
from common.channel_access_token import ChannelAccessToken
from db_controll import utils
from db_controll.RestorationRequestDB_ctr import RestorationRequestDB_ctr
# from db_controll.RestorationBidDB_ctr import RestorationBidDB_ctr


# 環境変数
LOGGER_LEVEL = os.environ.get("LOGGER_LEVEL")
CHANNEL_TYPE = os.environ.get("CHANNEL_TYPE")
CHANNEL_ID = os.getenv('OA_CHANNEL_ID', None)
LIFF_CHANNEL_ID = os.getenv('LIFF_CHANNEL_ID', None)

# テーブル操作クラスの初期化
RestorationRequest_table_controller = RestorationRequestDB_ctr()
# RestorationBid_table_controller = RestorationBidDB_ctr()
channel_access_token_table_controller = ChannelAccessToken()

# ログ出力の設定
logger = logging.getLogger()
if LOGGER_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
# LINEチャンネルチェック
if CHANNEL_ID is None:
    logger.error('Specify CHANNEL_ID as environment variable.')
    sys.exit(1)



def put_restraction_request(body:dict) ->str:
    """
    DyanmoDBに原状回復案件を登録する

    Params
    -------
    body:dict
        フロントから送信されたパラメータ

    Returns:bool
    -------
    restoration_request_id:str
        登録時に採番されたID
    """
    # 予約情報の登録
    restoration_request_id = RestorationRequest_table_controller.put_item(
        body['LINEID'], body['LINEName'], body['propertyName'], body['propertyAddress'],
        body['stDate'], body['dueDate'], body['hasParking'], body['hasElevator'],
        body['hasEstimate']
    )

    return restoration_request_id  # 予約番号

def lambda_handler(event:dict, context:dict):
    """ 
    予約情報とメッセージ情報をDynamoDBに登録
    Params
    ----------
    event : dict
            フロントより渡されたパラメータ
    context : dict
        コンテキスト内容。
    Returns
    -------
    body : dict
        予約IDとクーポン情報
    """
    # パラメータログ、チェック
    logger.info(event)
    body = json.loads(event['body'])
    if body is None:
        error_msg_display = common_const.const.MSG_ERROR_NOPARAM
        return utils.create_error_response(error_msg_display, 400)
    #ユーザーID取得
    try:
        user_profile = line.get_profile(
            body['idToken'], LIFF_CHANNEL_ID)  # lineライブラリ?
        if 'error' in user_profile and 'expired' in user_profile['error_description']:  # noqa 501
            return utils.create_error_response('Forbidden', 403)
        else:
            body['userId'] = user_profile['sub']
    except Exception:
        logger.exception('不正なIDトークンが使用されています')
        return utils.create_error_response('Error')

    # param_checker = validation.HairSalonParamCheck(body)  # TODO
    # if error_msg := param_checker.check_api_reservation_put():  # TODO
    #     error_msg_display = ('\n').join(error_msg)
    #     logger.error(error_msg_display)
    #     return utils.create_error_response(error_msg_display, 400)

    try:
        # 予約データ登録
        restoration_request_id  = put_restraction_request(body)
    except Exception as e:
        logger.exception('Occur Exception: %s', e)
        return utils.create_error_response('Error')

    body = json.dumps({'restorationRequestId': restoration_request_id })
    return utils.create_success_response(body)

