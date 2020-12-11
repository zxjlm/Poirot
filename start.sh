#!/bin/bash

#chmod  777  /etc/apt/sources.list
#
#cat source_files/ubuntu > /etc/apt/sources.list
#apt update
#apt upgrade

#apt-get install -y libjpeg-dev libtiff5-dev libpng-dev libfreetype6-dev libgif-dev libgtk-3-dev libxml2-dev libpango1.0-dev libcairo2-dev libspiro-dev libuninameslist-dev python3-dev ninja-build cmake build-essential gettext
#apt-get install fontforge -y --no-install-recommends
#apt-get install python3-pip -y
apt-get install python3.7 -y
apt install libgl1-mesa-glx -y
#cd ./source_files/fontforge
#mkdir build
#cd build
#cmake -GNinja ..
#ninja
#ninja install

python3.7 -m pip install --upgrade pip -i https://pypi.douban.com/simple
python3.7 -m pip install -r requirements.txt -i https://pypi.douban.com/simple
python3.7 -m pip install gunicorn -i https://pypi.douban.com/simple

mkdir font_collection
mkdir fontforge_output
