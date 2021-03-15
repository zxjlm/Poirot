"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-02 15:50:07
@description: None
"""
import hashlib
import re
import time
import shutil
from threading import Lock

from flask import Flask, request, jsonify, render_template, \
    copy_current_request_context, session
from flask_socketio import SocketIO, emit, disconnect

import config
from progress import SocketQueue, ProgressBar
from utils import ocr_func, ocr_processor, check_file, single_font_to_pic

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Poirot%%harumonia'
socketio = SocketIO(app, async_mode=None)
thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(2)
        ret = []
        while not SocketQueue.res_queue.empty():
            ProgressBar.now_length += 1
            ret.append(SocketQueue.res_queue.get())
        if ret:
            socketio.emit('my_response',
                          {'data': ret, 'width':
                              str(ProgressBar.calculate()) + '%'},
                          namespace='/test')


# @socketio.on('connect', namespace='/test')
# """建立websocket连接"""
# def test_connect():
#     global thread
#     with thread_lock:
#         if thread is None:
#             thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    """关闭websocket连接"""

    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    # for this emit we use a callback function
    # when the callback function is invoked we know that the message has been
    # received and it is safe to disconnect
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


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


@app.route('/page_digit')
def page_digit():
    """
    返回解析字体文件页面
    :return:
    """
    return render_template('digit.html')


@app.route('/page_instruction')
def page_instruction():
    """
    返回使用说明页面
    :return:
    """
    return render_template('instruction.html')


# @app.route("/download/<filepath>", methods=['GET'])
# def download_file(filepath):
#     此处的filepath是文件的路径，但是文件必须存储在static文件夹下
#     比如images\test.jpg
#     rel_path = 'test_files\\' + filepath
#     return app.send_static_file(rel_path)


@app.route('/api/font_file_cracker', methods=['POST'])
def font_file_cracker():
    """
    接受字体文件，返回破解结果
    :return:
    """

    try:
        file = request.files.get('font_file')
        type_ = request.form.get('type')
    except Exception as _e:
        return jsonify({'code': 400, 'msg': f'lose args,{_e}', 'res': {}})

    filename = re.sub('[（(）) ]', '', file.filename)
    file.save('./font_collection/' + filename)

    file_suffix = hashlib.md5(
        (filename + time.strftime('%Y%m%d%H%M%S')).encode()).hexdigest()

    if config.is_online and not check_file('./font_collection/' + filename):
        return jsonify({'code': 300, 'msg': 'Please use example file(*^_^*)'})

    ProgressBar.init()

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

    try:
        res = ocr_processor(filename, request.remote_addr, file_suffix,
                            has_pic_detail=True)

        if type_ == 'html':
            font_dict = {}
            for idx, foo in enumerate(res):
                if foo['ocr_result']:
                    res[idx]['ocr_result'] = foo['ocr_result'][0]['simPred']
                    font_dict[foo['name']] = foo['ocr_result']
                else:
                    res[idx]['ocr_result'] = 'undefined'
                    font_dict[foo['name']] = 'undefined'

            return jsonify({'code': 200,
                            'html': render_template('images.html', result=res),
                            'font_dict': font_dict})
        else:
            return jsonify({'code': 200, 'msg': 'success', 'res': res})

    except Exception as _e:
        if file_suffix:
            shutil.rmtree('./fontforge_output/' + file_suffix)
        return jsonify({'code': 400, 'msg': f'{_e}', 'res': {}})


@app.route('/api/img_cracker_via_local_ocr/', methods=['POST'])
def local_cracker():
    """
    接受单个图片，进行本地的ocr，返回图片破解结果
    :return:
    """
    if config.is_online:
        return jsonify(
            {'code': 300, 'msg': 'online mode can`t use image cracker'})
    img_b64 = request.form['img'].replace('data:image/png;base64,', '')

    start_time = time.time()
    res = ocr_func(img_b64.encode(), 'single_image', request.remote_addr,
                   has_pic_detail=True)
    return jsonify({'code': 200, 'msg': '成功',
                    'data': {'raw_out': res,
                             'speed_time':
                                 round(time.time() - start_time, 2)}})


@app.route('/api/special_for_printed_digits/', methods=['POST'])
def special_for_printed_digits():
    """
    针对数字进行特化
    Returns:

    """
    try:
        file = request.files.get('font_file')
        type_ = request.form.get('type')
    except Exception as _e:
        return jsonify({'code': 400, 'msg': f'lose args,{_e}', 'res': {}})

    filename = re.sub('[（(）) ]', '', file.filename)
    file.save('./font_collection/' + filename)

    file_suffix = hashlib.md5(
        (filename + time.strftime('%Y%m%d%H%M%S')).encode()).hexdigest()
    single_font_to_pic(file_suffix, filename, request.remote_addr)
    return jsonify({'code': 200, 'msg': '成功',
                    'data': {'raw_out': 'unnnnn',
                             'speed_time': -1}})
