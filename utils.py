'''
File: utils.py
Project: poirot
File Created: Wednesday, 25th August 2021 2:23:27 pm
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Wednesday, 25th August 2021 2:23:51 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description: 
'''
import hashlib
from api_ocr.baidu import baidu_ocr
from config import max_ocr_workers, use_baidu_ocr
from local_ocr.tesseract.tesseract_utils import tesseract_single_character
import re

from fontTools.ttLib import TTFont
from PIL import ImageFont, Image, ImageDraw
import base64
from io import BytesIO

from progress import SocketQueue, ProgressBar


def uni_2_png_stream(txt, font, img_size=512):
    """将字形转化为图片流

    Args:
        txt ([type]): [description]
        font ([type]): [description]
        img_size (int, optional): [description]. Defaults to 512.

    Returns:
        [type]: [description]
    """
    img = Image.new('1', (img_size, img_size), 255)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, int(img_size * 0.7))

    txt = chr(txt)
    x, y = draw.textsize(txt, font=font)
    draw.text(((img_size - x) // 2, (img_size - y) // 2), txt, font=font, fill=0)
    # draw.text((0,0), txt, font=font, fill=0)
    return img

def ocr_processor(filename):
    """

    Args:
        filename:上传的字体文件的文件名
        remote_addr:
        file_suffix:
        has_pic_detail:

    Returns:

    """
    ocr_results = []

    f = TTFont(filename)
    ProgressBar.max_length = len(f.getGlyphNames())

    for i,name in f.getBestCmap().items():
        pil = uni_2_png_stream(i, filename, 100)
        buffered = BytesIO()
        pil.save(buffered, format="PNG")
        ocr_results.append({
            'name': name,
            'img':  'data:image/png;base64,' + base64.b64encode(buffered.getvalue()).decode(),
            'ocr_result': tesseract_single_character(pil)
        })
        SocketQueue.res_queue.put(name)
        

    return ocr_results

def check_file(filepath):
    """
    校验文件
    :param filepath:
    :return:
    """
    with open(filepath, "rb") as f:
        return hashlib.md5(
            f.read()).hexdigest() == "4f1f3231cc1fcc198dbe1536f8da751a"

def ocr_func(base64_img, filename, ip):
    """[summary]

    Args:
        base64_img ([type]): [description]
        filename ([type]): [description]
        ip ([type]): [description]
    """
    base64_data = re.sub('^data:image/.+;base64,', '', base64_img)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    pil = Image.open(image_data)
    return {
            'name': filename,
            'img':  base64_img,
            'ocr_result': tesseract_single_character(pil)
        }