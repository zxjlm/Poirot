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

    def __init__(self):
        self.max = 0
        self.count = 0


class SocketQueue:
    """
    as
    """

    res_queue = queue.Queue()
