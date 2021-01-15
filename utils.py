"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-08 16:05:59
@description: None
"""
import base64
import hashlib
import json
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from io import BytesIO

import numpy as np
from PIL import Image
from loguru import logger

from api_ocr.baidu import baidu_ocr
from config import max_ocr_workers, use_baidu_ocr
from local_ocr import local_ocr

from progress import SocketQueue, ProgressBar
from fontTools.pens.basePen import BasePen

from reportlab.graphics.shapes import Path

from fontTools.ttLib import TTFont
from reportlab.lib import colors

from reportlab.graphics import renderPM
from reportlab.graphics.shapes import Group, Drawing


class ReportLabPen(BasePen):
    """A pen for drawing onto a reportlab.graphics.shapes.Path object."""

    def __init__(self, glyphSet, path=None):
        BasePen.__init__(self, glyphSet)
        if path is None:
            path = Path()
        self.path = path

    def _moveTo(self, p):
        (x, y) = p
        self.path.moveTo(x, y)

    def _lineTo(self, p):
        (x, y) = p
        self.path.lineTo(x, y)

    def _curveToOne(self, p1, p2, p3):
        (x1, y1) = p1
        (x2, y2) = p2
        (x3, y3) = p3
        self.path.curveTo(x1, y1, x2, y2, x3, y3)

    def _closePath(self):
        self.path.closePath()


def ocr_processor(filename, remote_addr, file_suffix, has_pic_detail=False):
    """

    Args:
        filename:上传的字体文件的文件名
        remote_addr:
        file_suffix:
        has_pic_detail:

    Returns:

    """

    if file_suffix in os.listdir("./fontforge_output"):
        os.rmdir("./fontforge_output/" + file_suffix)
    os.mkdir(f"./fontforge_output/{file_suffix}")

    # os.system(
    #     'fontforge -script font2png.py --file_path {} --file_name {}'.format(
    #         './font_collection/' + filename,
    #         file_suffix))

    font = TTFont("./font_collection/" + filename)

    for glyph in font.getGlyphNames():
        generate_pic(glyph, font, file_suffix)

    img_list = []

    for png in os.listdir(f"./fontforge_output/{file_suffix}/"):
        png_path = f"./fontforge_output/{file_suffix}/{png}"
        strength_pic(png_path)
        with open(png_path, "rb") as f:
            img_list.append(
                {"img": base64.b64encode(f.read()),
                 "name": png.replace(".png", "")}
            )
            # res_dic = ocr_func(img, remote_addr,
            # is_encode=False, has_pic_detail=True)
            # res_dic.update({'name': re.sub('.png|.jpg', '', png)})
            # res.append(res_dic)

    ProgressBar.max_length = len(img_list)
    tasks = []
    with ThreadPoolExecutor(
            max_workers=len(img_list)
            if len(img_list) <= max_ocr_workers
            else max_ocr_workers
    ) as pool:
        for img_dict in img_list:
            task = pool.submit(
                ocr_func, img_dict["img"], img_dict["name"], remote_addr,
                has_pic_detail
            )
            tasks.append(task)

    results = [getattr(foo, "_result") for foo in tasks]
    time.sleep(4)
    return results


def ocr_func(img_b64, picname, remote_addr, has_pic_detail=False) -> dict:
    """

    :param picname:
    :param has_pic_detail:
    :param img_b64:
    :param remote_addr:
    :return:
    """
    t_start = time.perf_counter()

    if is_null_pic(img_b64):
        logger.info(f"{picname} is white image. skip")
        res = [{"simPred": ""}]

    else:
        res = local_ocr(img_b64)

        if not res:
            if use_baidu_ocr:
                logger.info("local cracker failed,now start to use baidu api")
                res.append({"simPred": baidu_ocr(img_b64)})

        log_info = {
            "ip": remote_addr,
            "return": res,
            "time": time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime(time.time())),
        }
        logger.info(json.dumps(log_info, ensure_ascii=False))

    SocketQueue.res_queue.put(picname)

    if has_pic_detail:
        return {
            "img_detected_b64": "data:image/png;base64," + img_b64.decode(),
            "ocr_result": res,
            "espionage": float(time.perf_counter() - t_start),
            "name": picname,
        }
    else:
        return {
            "ocr_result": res,
            "espionage": float(time.perf_counter() - t_start),
            "name": picname,
        }


def strength_pic(pic_path):
    """
    扩张图片边缘
    :param pic_path:
    :return:
    """
    from PIL import Image

    old_im = Image.open(pic_path)
    old_size = old_im.size

    new_size = (300, 300)
    new_im = Image.new("RGB", new_size, color="white")
    new_im.paste(
        old_im,
        (int((new_size[0] - old_size[0]) / 2),
         int((new_size[1] - old_size[1]) / 2)),
    )

    new_im.save(pic_path)


def is_null_pic(img_b64):
    """
    判断是否是空白图片
    :param img_b64:
    :return:
    """
    if img_b64 is not None:
        raw_image = base64.b64decode(img_b64)
        image = Image.open(BytesIO(raw_image))
        return not np.max(255 - np.array(image))


def check_file(filepath):
    """
    校验文件
    :param filepath:
    :return:
    """
    with open(filepath, "rb") as f:
        return hashlib.md5(
            f.read()).hexdigest() == "4f1f3231cc1fcc198dbe1536f8da751a"


def generate_pic(glyphname, font: TTFont, file_suffix: str):
    image_file = f"./fontforge_output/{file_suffix}/{glyphname}.png"

    gs = font.getGlyphSet()
    pen = ReportLabPen(gs, Path(fillColor=colors.black, strokeWidth=1))
    g = gs[glyphname]
    g.draw(pen)

    w, h = 120, 120

    # Everything is wrapped in a group to allow transformations.
    g = Group(pen.path)
    g.translate(10, 20)
    g.scale(0.1, 0.1)

    d = Drawing(w, h)
    d.add(g)

    renderPM.drawToFile(d, image_file, fmt="PNG")
