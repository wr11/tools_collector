'''工具运行入口'''

import os
import sys

# 添加根目录到系统变量
rootPath = os.path.split(os.getcwd())[0]
sys.path.append(rootPath)

import toolview

def start():
    toolview.startToolView()

start()