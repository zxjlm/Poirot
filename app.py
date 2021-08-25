'''
File: app.py
Project: poirot
File Created: Wednesday, 25th August 2021 3:19:54 pm
Author: harumonia (zxjlm233@gmail.com)
-----
Last Modified: Wednesday, 25th August 2021 4:48:51 pm
Modified By: harumonia (zxjlm233@gmail.com>)
-----
Copyright 2020 - 2021 Node Supply Chain Manager Corporation Limited
-----
Description: 
'''

import re

import time
from threading import Lock
import config

from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect

from flask import Flask, request, jsonify, render_template, \
    copy_current_request_context, session
from utils import ocr_processor, check_file, ocr_func
from progress import SocketQueue, ProgressBar

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'Poirot%%harumonia'
socketio = SocketIO(app)
thread = None
thread_lock = Lock()


@socketio.on('disconnect_request')
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


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        # socketio.sleep(2)
        ret = []
        while not SocketQueue.res_queue.empty():
            ProgressBar.now_length += 1
            ret.append(SocketQueue.res_queue.get())
        if ret:
            socketio.emit('my_response',
                          {'data': ret, 'width':str(ProgressBar.calculate()) + '%'})
        socketio.emit('my_response',
                          {'data': ret, 'width':str(ProgressBar.calculate()) + '%'})


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
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
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


@app.route('/api/font_file_cracker', methods=['POST'])
def font_file_cracker():
    try:
        file = request.files.get('font_file')
        type_ = request.form.get('type')
    except Exception as _e:
        return jsonify({'code': 400, 'msg': f'lose args,{_e}', 'res': {}})

    filename = re.sub('[（(）) ]', '', file.filename)
    file.save('./font_collection/' + filename)

    if config.is_online and not check_file('./font_collection/' + filename):
        return jsonify({'code': 300, 'msg': 'Please use example file(*^_^*)'})

    ProgressBar.init()

    res = ocr_processor('./font_collection/' + filename)

    if type_ == 'html':
            font_dict = {}
            for foo in res:
                font_dict[foo['name']] = foo['ocr_result']
            
            return jsonify({'code': 200,
                            'html': render_template('images.html', result=res),
                            'font_dict': font_dict})
    else:
        return jsonify({'code': 200, 'msg': 'success', 'res': res})


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
    res = ocr_func(img_b64.encode(), 'single_image', request.remote_addr)
    return jsonify({'code': 200, 'msg': '成功',
                    'data': {'raw_out': res,
                             'speed_time':
                                 round(time.time() - start_time, 2)}})



@app.route('/api/special_for_printed_digits/', methods=['POST'])
def special_for_printed_digits():
    """
    针对数字进行特化
    Returns:
        如果传入的参数中指定了 has_pic_detail为 '0'，那么就只返回映射表
        默认情况下 has_pic_detail 的值是 '1'。

    """
    return jsonify({'code': 200})