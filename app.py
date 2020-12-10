"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-02 15:50:07
@description: None
"""
import time
import shutil

from flask import Flask, request, jsonify, render_template

from utils import ocr_func, ocr_processor

app = Flask(__name__)


@app.route('/')
def index():
    """
    返回主页
    :return:
    """
    return render_template('index.html')


@app.route('/page_pic')
def page_pic():
    """
    返回解析图片页面
    :return:
    """
    return render_template('pic.html')


@app.route('/page_font')
def page_font():
    """
    返回解析字体文件页面
    :return:
    """
    return render_template('font.html')


@app.route('/font_file_cracker', methods=['POST'])
def font_file_cracker_2_html():
    """

    :return:
    """
    file_suffix = None
    try:
        file = request.files.get('font_file')

        res = ocr_processor(file, request.remote_addr, is_encode=False, has_pic_detail=True)
        for idx, foo in enumerate(res):
            if foo['ocr_result']:
                res[idx]['ocr_result'] = foo['ocr_result'][0]['simPred']
            else:
                res[idx]['ocr_result'] = 'undefined'

        return render_template('images.html', result=res)
    except Exception as _e:
        if file_suffix:
            shutil.rmtree('./fontforge_output/' + file_suffix)
        return jsonify({'code': 400, 'msg': f'{_e}', 'res': {}})


@app.route('/api/font_file_cracker', methods=['POST'])
def font_file_cracker():
    """
    接受字体文件，返回破解结果
    :return:
    """
    file_suffix = None
    try:
        file = request.files.get('font_file')
        type_ = request.form.get('type')
    except Exception as _e:
        return jsonify({'code': 400, 'msg': f'lose args,{_e}', 'res': {}})

    try:
        res = ocr_processor(file, request.remote_addr, is_encode=False, has_pic_detail=True)

        if type_ == 'html':
            font_dict = {}
            for idx, foo in enumerate(res):
                if foo['ocr_result']:
                    res[idx]['ocr_result'] = foo['ocr_result'][0]['simPred']
                    font_dict[foo['name']] = foo['ocr_result']
                else:
                    res[idx]['ocr_result'] = 'undefined'
                    font_dict[foo['name']] = 'undefined'

            return jsonify({'code': 200, 'html': render_template('images.html', result=res), 'font_dict': font_dict})
        else:
            return jsonify({'code': 200, 'msg': 'success', 'res': res})

    except Exception as _e:
        if file_suffix:
            shutil.rmtree('./fontforge_output/' + file_suffix)
        return jsonify({'code': 400, 'msg': f'{_e}', 'res': {}})


@app.route('/api/img_cracker_via_local_ocr/', methods=['POST'])
def local_cracker():
    """
    接受图片，进行本地的ocr，返回图片破解结果
    :return:
    """
    img_b64 = request.form['img'].replace('data:image/png;base64,', '')

    start_time = time.time()
    res = ocr_func(img_b64, 'single_image', request.remote_addr, has_pic_detail=True)
    return jsonify({'code': 200, 'msg': '成功',
                    'data': {'raw_out': res,
                             'speed_time': round(time.time() - start_time, 2)}})


@app.route('/normal_test')
def normal_test():
    print(render_template('demo.html'))
    return render_template('demo.html')
