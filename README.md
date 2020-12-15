# Poirot(开发中)
自动将字体文件(woff\woff2\ttf)映射为结果字典,主要用于中文字体反爬虫的破解,报错css字体映射和图片文字反爬虫.

![poirot.gif](https://i.loli.net/2020/12/15/sNuACxmwVZL9Phb.gif)

具体的思路见 [字体反爬虫解决方案-自动化通过字体文件生成映射字典](https://blog.harumonia.moe/font-antispider-cracker/)

## TODO

- [x] 升级为多线程
- [x] 添加本地的文字识别
- [x] 使用socketio优化使用体验
- [x] 添加进度条优化使用体验
- [ ] 扩展文字识别途径(腾讯)
- [x] 扩展文字识别途径(百度)
- [x] 对空白图片添加过滤

### 部署指定

- [ ] 部署样例网站
- [ ] Docker
- [x] 使用Redis管理api访问次数
- [ ] 解决socket通信混乱的问题

## 启动

### 普通启动
```shell
pip install requirements.txt

flask run
```
访问 http://127.0.0.1:5000 即可使用


### docker 启动

1. 可以直接使用docker启动
```shell script
docker build . -t poirot
docker run -d poirot
```

2. 如果按照 **docker-compose.yml** 启动，需要创建在宿主机对应的文件夹
- /logs/gunicorn/poirot 存放日志
- /root/data/poirot/font_collection 存放分析文件
```shell script
mkdir -p /logs/gunicorn/poirot && mkdir -p /root/data/poirot/font_collection
docker up
```

### 测试用的文件
测试用的文件见 ./static/test_files





## 说明

提供web和api两类服务


