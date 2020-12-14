"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-08 16:05:59
@description: None
"""
import base64
import hashlib
import json
import os
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from io import BytesIO

import numpy as np
from PIL import Image
from loguru import logger

from api_ocr.baidu import baidu_ocr
from config import max_ocr_workers, use_baidu_ocr
from local_ocr import local_ocr

from progress import SocketQueue, ProgressBar


def ocr_processor(file, remote_addr, has_pic_detail=False):
    """

    :return:
    """
    filename = re.sub('[（(）) ]', '', file.filename)
    file.save('./font_collection/' + filename)

    file_suffix = hashlib.md5((filename + time.strftime('%Y%m%d%H%M%S')).encode()).hexdigest()

    if file_suffix in os.listdir('./fontforge_output'):
        os.rmdir('./fontforge_output/' + file_suffix)
    os.mkdir(f'./fontforge_output/{file_suffix}')

    os.system(
        'fontforge -script font2png.py --file_path {} --file_name {}'.format('./font_collection/' + filename,
                                                                             file_suffix))

    img_list = []

    for png in os.listdir(f'./fontforge_output/{file_suffix}/'):
        png_path = f'./fontforge_output/{file_suffix}/{png}'
        strength_pic(png_path)
        with open(png_path, 'rb') as f:
            img_list.append({'img': base64.b64encode(f.read()), 'name': png.replace('.png', '')})
            # res_dic = ocr_func(img, remote_addr, is_encode=False, has_pic_detail=True)
            # res_dic.update({'name': re.sub('.png|.jpg', '', png)})
            # res.append(res_dic)

    ProgressBar.max_length = len(img_list)
    tasks = []
    with ThreadPoolExecutor(max_workers=len(img_list) if len(img_list) <= max_ocr_workers else max_ocr_workers) as pool:
        for img_dict in img_list:
            task = pool.submit(ocr_func, img_dict['img'], img_dict['name'], remote_addr, has_pic_detail)
            tasks.append(task)

    results = [getattr(foo, '_result') for foo in tasks]
    time.sleep(4)
    return results


def ocr_func(img_b64, picname, remote_addr, has_pic_detail=False) -> dict:
    """

    :param picname:
    :param has_pic_detail:
    :param img_b64:
    :param remote_addr:
    :return:
    """
    t_start = time.perf_counter()

    if is_null_pic(img_b64):
        logger.info(f'{picname} is white image. skip')
        res = [{'simPred': ''}]

    else:
        res = local_ocr(img_b64)

        if not res:
            if use_baidu_ocr:
                logger.info('local cracker failed,now start to use baidu api')
                res.append({'simPred': baidu_ocr(img_b64)})

        log_info = {
            'ip': remote_addr,
            'return': res,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
        }
        logger.info(json.dumps(log_info, ensure_ascii=False))

    SocketQueue.res_queue.put(picname)

    if has_pic_detail:
        return {'img_detected_b64': 'data:image/png;base64,' + img_b64.decode(), 'ocr_result': res,
                'espionage': float(time.perf_counter() - t_start), 'name': picname}
    else:
        return {'ocr_result': res, 'espionage': float(time.perf_counter() - t_start), 'name': picname}


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


def is_null_pic(img_b64):
    """
    判断是否是空白图片
    :param img_b64:
    :return:
    """
    if img_b64 is not None:
        raw_image = base64.b64decode(img_b64)
        image = Image.open(BytesIO(raw_image))
        return not np.max(255 - np.array(image))
