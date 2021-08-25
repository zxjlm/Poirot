
import hashlib
import re
import time

from flask import Flask, request, jsonify
from utils import ocr_processor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Poirot%%harumonia'

@app.route('/font_file_test', methods=['POST'])
def font_file_test():
    try:
        file = request.files.get('font_file')
    except Exception as _e:
        return jsonify({'code': 400, 'msg': f'lose args,{_e}', 'res': {}})

    filename = re.sub('[（(）) ]', '', file.filename)
    file.save('./font_collection/' + filename)

    # file_suffix = hashlib.md5(
    #     (filename + time.strftime('%Y%m%d%H%M%S')).encode()).hexdigest()

    # if config.is_online and not check_file('./font_collection/' + filename):
    #     return jsonify({'code': 300, 'msg': 'Please use example file(*^_^*)'})

    res = ocr_processor('./font_collection/' + filename)

    return jsonify({'code': 200, 'msg': 'success', 'res': res})
