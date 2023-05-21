"""
@author: harumonia
@license: © Copyright 2023, Node Supply Chain Manager Corporation Limited.
@contact: zxjlm233@gmail.com
@software: Pycharm
@homepage: https://harumonia.moe/
@file: ocrs.py
@time: 2023/3/26 21:51
@desc:
"""

import hashlib
from pathlib import Path

from fontTools.pens.reportLabPen import ReportLabPen
from fontTools.ttLib import TTFont
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing, Path
from reportlab.lib import colors

from api_ocr.baidu import baidu_ocr
from config import max_ocr_workers, use_baidu_ocr
from local_ocr.tesseract.tesseract_utils import tesseract_single_character, tesseract_multi_character
import re

from fontTools.ttLib import TTFont
from PIL import ImageFont, Image, ImageDraw
import base64
from io import BytesIO


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

    Returns:

    """
    ocr_results = []

    f = TTFont(filename)

    for i, name in f.getBestCmap().items():
        pil = uni_2_png_stream(i, filename, 100)
        buffered = BytesIO()
        pil.save(buffered, format="PNG")
        ocr_results.append({
            'name': name,
            'img': 'data:image/png;base64,' + base64.b64encode(buffered.getvalue()).decode(),
            'ocr_result': tesseract_single_character(pil)
        })

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
        'img': base64_img,
        'ocr_result': tesseract_multi_character(pil)
    }


def generate_pic(glyphname, font: TTFont, size=120, scale=0.1):
    """
    生成图片 -> 预处理 -> 保存到本地
    Args:
        glyphname:
        font:
        file_suffix:
        size:
        scale:

    Returns:

    """

    gs = font.getGlyphSet()
    pen = ReportLabPen(gs, Path(fillColor=colors.black, strokeWidth=1))
    g = gs[glyphname]
    g.draw(pen)

    w, h = size, size

    # Everything is wrapped in a group to allow transformations.
    g = Group(pen.path)
    # g.translate(10, 20)
    g.scale(scale, scale)

    d = Drawing(w, h)
    d.add(g)

    return renderPM.drawToPIL(d)


def single_font_to_pic(filename, content):
    res_list = []
    pils = []

    with open(filename, 'wb') as f:
        f.write(content)

    font = TTFont('./' + filename)
    for glyph in font.getGlyphNames():
        if glyph.isdigit():
            pils.append(generate_pic(glyph, font, 30, 0.04))

    res = ocr_func_for_digit(pils)

    for idx, foo in enumerate(res):
        res_list.append({
            "ocr_result": foo,
            "name": str(font.getGlyphNames()[idx]).replace('.png', '').replace('_', ''),
        })

    return res_list
