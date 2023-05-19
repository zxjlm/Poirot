"""
@author: harumonia
@license: © Copyright 2023, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: digit.py
@time: 2023/5/18 21:46
@desc:
"""
from fastapi import APIRouter, UploadFile

digit_api_router = APIRouter()


@digit_api_router.route('/special_for_printed_digits/', methods=['POST'])
def special_for_printed_digits(file: UploadFile, filename: str):
    """
    针对数字进行特化
    Returns:
        如果传入的参数中指定了 has_pic_detail为 '0'，那么就只返回映射表
        默认情况下 has_pic_detail 的值是 '1'。

    """
    res = single_font_to_pic(filename, file.file.read())
    return {'code': 200, 'font_dict': {foo['name']: int(foo['ocr_result']) for foo in res}}
