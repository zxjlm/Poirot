# Poirot(开发中)
自动将字体文件(woff\woff2\ttf)映射为结果字典,主要用于中文字体反爬虫的破解,包括css字体映射和图片文字反爬虫.

![poirot.gif](https://i.loli.net/2020/12/15/sNuACxmwVZL9Phb.gif)

具体的思路见 [字体反爬虫解决方案-自动化通过字体文件生成映射字典](https://blog.harumonia.moe/font-antispider-cracker/)

[DEMO](http://39.108.229.166:8000/)

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
- [x] Docker
- [x] 使用Redis管理api访问次数
- [x] 解决socket通信混乱的问题

## 启动

windows 无法直接使用 `flask run` 启动,这会导致功能的缺失. 
在mac或者linux下，可以在安装了 requirements.txt 中的依赖和 fontforge 之后使用 `flask run` 启动.

docker 启动则没有这些烦恼, 真正意义上的傻瓜式使用.

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

提供web和api两类服务.




