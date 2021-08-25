'''
File: tesseract_utils.py
Project: poirot
File Created: Wednesday, 25th August 2021 2:26:42 pm
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Wednesday, 25th August 2021 2:27:05 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description: 
'''
import pytesseract


def tesseract_single_character(image) -> str:
    """使用tesseract识别单个字符

    Args:
        image ([type]): [description]

    Returns:
        str: [description]
    """
    text = pytesseract.image_to_string(image, lang='chi_sim', config='--psm 10')
    return text.strip()

