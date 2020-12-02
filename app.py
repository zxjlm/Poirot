"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-02 15:50:07
@description: None
"""
import base64
import json
import time
from io import BytesIO

from PIL import Image
from flask import Flask, render_template, request, jsonify
from loguru import logger

from local_ocr.model import OcrHandle

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'


@app.route('/api/cracker/', methods=['POST'])
def cracker():
    short_size = 960
    start_time = time.time()
    img_b64 = request.form['img']

    if img_b64 is not None:
        raw_image = base64.b64decode(img_b64.encode('utf-8'))
        img = Image.open(BytesIO(raw_image))
    else:
        logger.error("{'code': 400, 'msg': '没有传入参数'}")
        return jsonify({'code': 400, 'msg': '没有传入参数'})

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
        return jsonify({'code': 400, 'msg': '产生了一点错误，请检查日志', 'err': str(ex)})
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
        'ip': request.remote_addr,
        'return': res,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    }
    logger.info(json.dumps(log_info, ensure_ascii=False))
    return jsonify({'code': 200, 'msg': '成功',
                    'data': {'img_detected': 'data:image/jpeg;base64,' + img_detected_b64, 'raw_out': res,
                             'speed_time': round(time.time() - start_time, 2)}})
