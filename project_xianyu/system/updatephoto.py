#!/usr/bin/env python3
# encoding: utf-8
'''
1、读取指定目录下的所有文件
2、读取文件，正则匹配出需要的内容，获取文件名
3、打开此文件(可以选择打开可以选择复制到别的地方去)
'''
import os.path
import re


# # 遍历指定目录，显示目录下的所有文件名
# def eachFile(filepath):
#     pathDir = os.listdir(filepath)
#     for allDir in pathDir:
#         child = os.path.join('%s\%s' % (filepath, allDir))
#         if os.path.isfile(child):
#             readFile(child)
#             # print (child.decode('gbk')) # .decode('gbk')是解决中文显示乱码问题
#             continue
#         eachFile(child)
#
#
# # 遍历出结果 返回文件的名字
# def readFile(filenames):
#     fopen = open(filenames, 'rb')  # r 代表read
#     try:
#         fileread = fopen.read()
#     except:
#         print("error")
#     else:
#
#         fopen.close()
#         t = re.search(r'request - 请求对象', fileread)
#         if t:
#             #             print "匹配到的文件是:"+filenames
#             arr.append(filenames)

class pppp():
    def __init__(self,filenames):
        self.filenames = filenames

    def get_photo0000(self):
        list_photo = []
        # filenames = '/home/tarena/xianyu_tupian' # 文件的绝对路径
        pathDir = os.listdir(self.filenames)  #os.listdir: 读取该文件夹下的文件名称或目录名称，形成列表
        for allDir in pathDir:
            child = os.path.join('%s/%s' % (self.filenames, allDir))  # os.path.join：将前面的绝对路径与得到的文件名 连接起来
            for dir in os.listdir(child):
                # grandson = os.path.join('%s/%s' % (child, dir))
                # for dd in os.listdir(grandson):
                dict_photo = {}
                dict_photo["commodity_id"] = int(allDir)
                dict_photo["file_name"] = dir
                path = os.path.join('%s/%s' % (child, dir))
                dict_photo["full_path"]=path
                list_photo.append(dict_photo)
        for i in list_photo:
            print(i)
        return list_photo

if __name__ =="__main__":
    asda = pppp('/home/tarena/xianyu_tupian/运动')
    asda.get_photo0000()

    # arr = []
    # eachFile(filenames)
    # for i in arr:
    #     print(i)