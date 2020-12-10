"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-10 16:20:50
@description: None
"""
import queue


class ProgressBar:
    """
    进度条
    """

    max_length = 1
    now_length = 0

    @classmethod
    def calculate(cls):
        return int(cls.now_length * 100 / cls.max_length)

    @classmethod
    def init(cls):
        cls.max_length = 1
        cls.now_length = 0


class SocketQueue:
    """
    as
    """

    res_queue = queue.Queue()
