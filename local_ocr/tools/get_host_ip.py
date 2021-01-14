import logging
import socket


def host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except OSError as _e:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        logging.warning(_e)
    finally:
        s.close()

    return ip
