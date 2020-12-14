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
from threading import Lock

from flask import Flask, request, jsonify, render_template, copy_current_request_context, session
from flask_socketio import SocketIO, emit, disconnect

from progress import SocketQueue, ProgressBar
from utils import ocr_func, ocr_processor

app = Flask(__name__)
socketio = SocketIO(app)
thread = None
thread_lock = Lock()


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(3)
        ret = []
        while not SocketQueue.res_queue.empty():
            ProgressBar.now_length += 1
            ret.append(SocketQueue.res_queue.get())
        socketio.emit('my_response',
                      {'data': ret, 'width': str(ProgressBar.calculate()) + '%'},
                      namespace='/test')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
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

    ProgressBar.init()

    try:
        res = ocr_processor(file, request.remote_addr, has_pic_detail=True)

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
    接受单个图片，进行本地的ocr，返回图片破解结果
    :return:
    """
    img_b64 = request.form['img'].replace('data:image/png;base64,', '')

    start_time = time.time()
    res = ocr_func(img_b64.encode(), 'single_image', request.remote_addr, has_pic_detail=True)
    return jsonify({'code': 200, 'msg': '成功',
                    'data': {'raw_out': res,
                             'speed_time': round(time.time() - start_time, 2)}})


@app.route('/normal_test')
def normal_test():
    return render_template('demo_socket.html', async_mode=socketio.async_mode)
