#!/usr/bin/env bash

# 切换到工作目录
cd /root/111

# 运行Python脚本
python3 main.py > main.log 2>&1 &
sleep 39
python3 script.py > script.log 2>&1 &



# 等待用户按下Enter键
read -p "Press [Enter] to continue..."
