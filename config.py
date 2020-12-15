"""
@project : jzmonitor
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-10-12 17:28:22
@description: None
"""
import os
import multiprocessing

filt_path = os.path.abspath(__file__)
father_path = os.path.abspath(os.path.dirname(filt_path) + os.path.sep + ".")

# dbnet 参数
dbnet_max_size = 6000  # 长边最大长度
pad_size = 0  # 检测是pad尺寸，有些文档文字充满整个屏幕检测有误，需要pad

# crnn参数
crnn_lite = True
model_path = os.path.join(father_path, "local_ocr/models/dbnet.onnx")
is_rgb = True
crnn_model_path = os.path.join(father_path, "local_ocr/models/crnn_lite_lstm.onnx")

# angle
angle_detect = True
angle_detect_num = 30
angle_net_path = os.path.join(father_path, "local_ocr/models/angle_net.onnx")

from local_ocr.crnn.keys import alphabetChinese as alphabet

# 在进行本地ocr时最大线程数
max_ocr_workers = multiprocessing.cpu_count() * 2

# ip 访问最大次数
max_post_time = 3

# 调用百度OCR(需要配置secure.py)
use_baidu_ocr = False

# 调用腾讯OCR(需要配置secure.py)(未完成)
use_tencent_ocr = False

white_ips = []  # 白名单

version = 'api/v1'
