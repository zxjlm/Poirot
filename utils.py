"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-08 16:05:59
@description: None
"""
import base64
import json
import time
from io import BytesIO
from PIL import Image
from loguru import logger
from local_ocr.model import OcrHandle


def ocr_func(img_b64, remote_addr, is_encode=True, has_pic_detail=False) -> dict:
    """

    :param has_pic_detail:
    :param is_encode:
    :param img_b64:
    :param remote_addr:
    :return:
    """
    t_start = time.perf_counter()
    short_size = 960

    if img_b64 is not None:
        if is_encode:
            raw_image = base64.b64decode(img_b64.encode('utf-8'))
        else:
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
    img = img.convert("RGB")

    # img.save("../web_imgs/{}.jpg".format(time_now))

    res = []
    do_det = True

    if do_det:
        ocrhandle = OcrHandle()
        res = ocrhandle.text_predict(img, short_size)

        img_detected = img.copy()

        output_buffer = BytesIO()
        img_detected.save(output_buffer, format='PNG')
        byte_data = output_buffer.getvalue()
        img_detected_b64 = base64.b64encode(byte_data).decode('utf8')

    else:
        output_buffer = BytesIO()
        img.save(output_buffer, format='JPEG')
        byte_data = output_buffer.getvalue()
        img_detected_b64 = base64.b64encode(byte_data).decode('utf8')

    log_info = {
        'ip': remote_addr,
        'return': res,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
    }
    logger.info(json.dumps(log_info, ensure_ascii=False))
    if has_pic_detail:
        return {'img_detected_b64': img_detected_b64, 'ocr_result': res, 'espionage': float(time.perf_counter() - t_start)}
    else:
        return {'ocr_result': res, 'espionage': float(time.perf_counter() - t_start)}


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
    new_im = Image.new("RGB", new_size, color='white')  ## luckily, this is already black!
    new_im.paste(old_im, (int((new_size[0] - old_size[0]) / 2),
                          int((new_size[1] - old_size[1]) / 2)))

    new_im.save(pic_path)
