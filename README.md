# Poirot

自动将字体文件(woff\woff2\ttf)映射为结果字典,主要用于中文字体反爬虫的破解,包括css字体映射和图片文字反爬虫.

![poirot.gif](https://i.loli.net/2020/12/15/sNuACxmwVZL9Phb.gif)

具体的思路见 [字体反爬虫解决方案-自动化通过字体文件生成映射字典](https://blog.harumonia.moe/font-antispider-cracker/)

[DEMO](http://39.108.229.166:8000/)
ps. DEMO的版本为 [最初的fontforge版本](https://github.com/zxjlm/Poirot/releases/tag/0.1.0)

## TODO

- [x] 升级为多线程
- [x] 添加本地的文字识别
- [x] 使用socketio优化使用体验
- [x] 添加进度条优化使用体验
- [ ] 扩展文字识别途径(腾讯)
- [x] 扩展文字识别途径(百度)
- [x] 对空白图片添加过滤
- [x] 解除fontforge的依赖

### 部署指定

- [x] 部署样例网站
- [x] Docker
- [x] 使用Redis管理api访问次数
- [x] 解决socket通信混乱的问题

## 启动

~~windows 无法直接使用 `flask run` 启动,这会导致功能的缺失.~~  
~~在mac或者linux下，可以在安装了 requirements.txt 中的依赖和 fontforge 之后使用 `flask run` 启动.~~
~~docker 启动则没有这些烦恼, 真正意义上的傻瓜式使用.~~

在1.x之后的版本中,解除了对fontforge的依赖,所以能够直接在windows上面使用了😀

### 普通启动

#### poetry

```shell
poetry install --no-dev

flask run
```

#### pip

```shell
pip install -r requirements.txt

flask run
```

之后访问 "http://127.0.0.1:5000" 即可使用

### docker 启动

1. 可以直接使用docker启动

```shell script
docker build . -t poirot
docker run -d poirot
```

ps. 国内使用可以先修改 Dockerfile 中的注释加快构建速度

2. 如果按照 **docker-compose.yml** 启动，需要创建在宿主机对应的文件夹

- /logs/gunicorn/poirot 存放日志
- /root/data/poirot/font_collection 存放分析文件

```shell script
mkdir -p /logs/gunicorn/poirot && mkdir -p /root/data/poirot/font_collection
docker up
```

### 测试用的文件

测试用的文件见 ./static/test_files

### 服务

提供web和api两类服务.

web:
如[DEMO](http://39.108.229.166:8000/)所示,发送字体文件到后端,解析完毕之后返回序列化结果到前端,再由前端序列化为json字符串
. 后端识别的结果会有误差，这个误差可以通过前端的人工校验抹除。

api: 出于功能拓展和使用方式多样化的角度考虑,在开发伊始特意将部分功能设计为api的形式. 目前总共有3个. 

- 普通字体文件识别(/api/font_file_cracker):
  并不推荐直接使用api, 中文文字识别的成功率只在 70%~80% , 需要配合人工审核, 所以对于中文, 建议使用web服务
- 数字特化(/api/special_for_printed_digits/):
  与中文识别不同，数字的识别率在使用 自训练的模型(./models/clf_model) 之后能够无限接近100% (至少目前没有遇到识别错误的案例)
- 单张图片识别(/api/img_cracker_via_local_ocr/):
  针对单张图片进行识别, 这是开发过程中的副产物, 可以用于进行一些验证

## 说明

默认情况下，使用本地破解为主，第三方OCR服务为辅的破解方案.

本地OCR基于[chineseocr_lite](https://github.com/ouyanghuiyu/chineseocr_lite).

### 接入百度OCR

1. 将 **config.py** 中 _use_baidu_ocr_ 的值改为 True.

2. 创建 **secure.py** 文件,文件中需要有一个 _access_token_ 变量,其中存放百度OCR的token。

### 接入腾讯OCR

待开发



