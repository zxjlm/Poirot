"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-11 16:08:36
@description: None
"""
import base64
import time

import requests
from loguru import logger

from secure import access_token


def baidu_ocr(img: bytes):
    """
    文字识别(百度)
    :param img: base64化的图片
    :return:
    """
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    #     request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage"

    params = {"image": img}
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        time.sleep(1)
        result = response.json()
        if 'error_code' in result.keys():
            logger.warning('baidu return error_code', result)
        elif result['words_result_num'] == 1:
            return result['words_result'][0]['words']
    return ''
