"""
@project : Poirot
@author  : zhang_xinjian
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-02 15:46:55
@description: None
"""
import base64
from io import BytesIO
from PIL import Image
from loguru import logger

from local_ocr.model import OcrHandle


def local_ocr(img_b64):
    """
    调用本地ocr
    :param img_b64:
    :return:
    """

    if img_b64 is not None:
        raw_image = base64.b64decode(img_b64)
        img = Image.open(BytesIO(raw_image))
    else:
        logger.error("{'code': 400, 'msg': '没有传入参数'}")
        return {'code': 400, 'msg': '没有传入参数'}

    try:
        if hasattr(img, '_getexif') and img._getexif() is not None:
            orientation = 274
            exif = dict(img._getexif().items())
            if orientation not in exif:
                exif[orientation] = 0
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
    except Exception as ex:
        logger.error({'code': 400, 'msg': '产生了一点错误，请检查日志', 'err': str(ex)})
        return {'code': 400, 'msg': '产生了一点错误，请检查日志', 'err': str(ex)}
    # img = img.convert("RGB")

    # img.save("../web_imgs/{}.jpg".format(time_now))

    ocrhandle = OcrHandle()
    res = ocrhandle.text_predict(img)

    return res
