# -*- coding:utf-8 -*-
import os
# 创建web文件夹
if not os.path.exists('{0}\web'.format(os.getcwd())):
    os.makedirs('{0}\web'.format(os.getcwd()))

for root,dirs,files in os.walk(os.getcwd()):
    for name in files:
        move_list = ['wmv', 'avi', 'dat', 'asf', 'mpeg', 'mpg', 'rm', 'rmvb', 'ram', 'flv', 'mp4', '3gp', 'mov', 'divx', 'dv', 'vob', 'mkv', 'qt', 'cpk', 'fli', 'flc', 'f4v', 'm4v', 'mod', 'm2t', 'swf', 'webm', 'mts', 'm2ts', '3g2', 'mpe', 'ts', 'div', 'lavf', 'dirac']
        # move_list = ['mp4']
        file_name = os.path.join(root,name)
        if file_name[-3:]in move_list:   # 后面可以定义一个列表
            # 创建文件之前，保证文件名的规范性
            name =  os.path.splitext(name)[0].strip()
            # os.mkdir(name)
            print(name)
            with open('index.html','a',encoding="utf-8")as file:
                file.write('<p><a href="{2}\\web\\{0}.html">{1}</a></p>\n'.format(name,name,os.getcwd()))
            with open('web/{}.html'.format(name),'w',encoding="utf-8") as f:
                f.write('<!DOCTYPE html><html><body><video width="640" height="480" controls="controls" autoplay="autoplay"><source src="{}" type="video/mp4" /></video></body></html>'.format(file_name))
