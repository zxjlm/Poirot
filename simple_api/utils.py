# -*- coding: utf-8 -*-
"""
    :time: 2021/3/18 15:16
    :author: Harumonia
    :url: http://harumonia.moe
    :project: poirot(light)
    :file: utils.py
    :copyright: © 2021 harumonia<zxjlm233@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import pickle

import numpy as np
from PIL import Image
from fontTools.pens.reportLabPen import ReportLabPen
from fontTools.ttLib import TTFont
from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing, Path
from reportlab.lib import colors


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


def ocr_func_for_digit(pil_pics):
    """

    Args:
        pil_pics:

    Returns:

    """
    datas = []
    for pil in pil_pics:
        datas.append(convert_img(pil))
    datas = np.array(datas)
    n_samples = len(datas)
    data = datas.reshape((n_samples, -1)) / 255
    with open('./models/clf_model.pkl', 'rb') as f:
        clf = pickle.load(f)
    predicted = clf.predict(data)
    return list(predicted)


def convert_img(img):
    nimg = np.array(img)
    ttmp = nimg.tolist()
    for row in range(len(ttmp)):
        for col in range(len(ttmp[0])):
            ttmp[row][col] = np.average(ttmp[row][col])
    return np.array(ttmp)
