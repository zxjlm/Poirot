"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-02 15:50:07
@description: None
"""
import base64
import os
import re
import time
import hashlib
import shutil

from flask import Flask, request, jsonify

from utils import ocr_func, strength_pic

app = Flask(__name__)


@app.route('/')
def index():
    return 'hello'


@app.route('/api/font_file_cracker', methods=['POST'])
def font_file_cracker():
    """
    接受字体文件，返回破解结果
    :return:
    """
    file_suffix = None
    try:
        file = request.files.get('font_file')
        filename = re.sub('[（(）) ]', '', file.filename)
        file.save('./font_collection/' + filename)
        file_suffix = hashlib.md5((filename + time.strftime('%Y%m%d%H%M%S')).encode()).hexdigest()

        if file_suffix in os.listdir('./fontforge_output'):
            os.rmdir('./fontforge_output/' + file_suffix)
        os.mkdir(f'./fontforge_output/{file_suffix}')

        os.system(
            'fontforge -script font2png.py --file_path {} --file_name {}'.format('./font_collection/' + filename,
                                                                                 file_suffix))

        res = []
        for png in os.listdir(f'./fontforge_output/{file_suffix}/')[:10]:
            png_path = f'./fontforge_output/{file_suffix}/{png}'
            strength_pic(png_path)
            with open(png_path, 'rb') as f:
                img = base64.b64encode(f.read())
                res_dic = ocr_func(img, request.remote_addr, is_encode=False)
                res_dic.update({'name': re.sub('.png|.jpg', '', png)})
                res.append(res_dic)

        return {'code': 200, 'msg': 'success', 'res': res}
    except Exception as _e:
        if file_suffix:
            shutil.rmtree('./fontforge_output/' + file_suffix)
            os.rmdir('./fontforge_output/' + file_suffix)
        return {'code': 400, 'msg': f'{_e}', 'res': {}}


@app.route('/api/img_cracker_via_local_ocr/', methods=['POST'])
def local_cracker():
    """
    接受图片，进行本地的ocr，返回图片破解结果
    :return:
    """
    img_b64 = request.form['img']

    start_time = time.time()
    res = ocr_func(img_b64, request.remote_addr)
    return jsonify({'code': 200, 'msg': '成功',
                    'data': {'img_detected': 'data:image/jpeg;base64,' + res['img_detected_b64'], 'raw_out': res['res'],
                             'speed_time': round(time.time() - start_time, 2)}})
