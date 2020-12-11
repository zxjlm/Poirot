"""
@project : Poirot
@author  : harumonia
@mail   : zxjlm233@163.com
@ide    : PyCharm
@time   : 2020-12-11 09:34:28
@description: None
"""

import multiprocessing

# debug = True
# threads = 2
worker_connections = 200
loglevel = 'info'
bind = "0.0.0.0:5000"
pidfile = '/logs/gunicorn/gunicorn.pid'
accesslog = '/logs/gunicorn/gunicorn_acess.log'
errorlog = '/logs/gunicorn/gunicorn_error.log'
daemon = True

# 启动的进程数
workers = multiprocessing.cpu_count()
worker_class = 'sync'
x_forwarded_for_header = 'X-FORWARDED-FOR'
