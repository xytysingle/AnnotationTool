#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/10/3 17:20
#!@Author :SINGLE
#!@File   :BaseApp.py
import ctypes
from tkinter import messagebox

from configobj import ConfigObj
import os

from Const import const


class BaseApp:
    #common-var
    user_info=None
    appdata_dir=os.path.join(os.getenv('localappdata'), 'ZeroEye', 'PolygonAnnotationTool')
    config_path=os.path.join(appdata_dir, 'conifg.ini')
    config=None
    #common-function
    def is_exit(master,config=None,cur_sku_lib=None,cur_img_index=None,is_cur_img_change=False,str=''):
        if is_cur_img_change:
            str='未保存,'
        if messagebox.askokcancel("提示", str+"是否要退出?"):
            try:
                # master.destroy()
                os._exit(0)
            except:
                pass

    def is_save(master,info='离开前是否保存?'):
        # return messagebox.askyesnocancel("提示", info)
        return  ctypes.windll.user32.MessageBoxA(0, info.encode('gb2312'), u' 提示'.encode('gb2312'), 3)

    def msgBox(self, info='敬请期待!'):
        # messagebox.showinfo(title='提示', message=info)
        ctypes.windll.user32.MessageBoxA(0, info.encode('gb2312'),u' 提示'.encode('gb2312'), 0)

    def get_conifgObj(filename='config.ini'):
        # 生成配置文件
        # conf_ini = "./test.ini"
        # config = ConfigObj(conf_ini, encoding='UTF8')
        file_path = os.path.join(BaseApp.appdata_dir, filename)
        # config = BaseApp.config if  BaseApp.config  else ConfigObj(file_path,encoding='utf-8')
        if   BaseApp.config :
            config=BaseApp.config
        else:
            BaseApp.config=config=ConfigObj(file_path,encoding='utf-8')
            # print(BaseApp.config)
        if not os.path.exists(file_path):
            # 先新建目录
            os.makedirs(os.path.join(os.getenv('localappdata'), 'ZeroEye', 'PolygonAnnotationTool', 'Logs'),exist_ok=1)
            # 初始化配置文件
            if filename == 'config.ini':
                config[const.LOGIN]={}
                config[const.LOGIN][const.ISREMEMBERPWD] = '0'
                config[const.LOGIN][const.ISAUTOLOGIN] = '0'
                config[const.LOGIN][const.ISWELCOMEMSG] = '1'
                config[const.LOGIN][const.ISPOWERON] = '0'
                config[const.LOGIN][const.LANGUAGE] = 'en'
                config[const.LOGIN][const.USER] = ''
                config[const.LOGIN][const.PSWD] = ''
                config[const.LOGIN][const.ISPOLL] = '0'
                config[const.LOGIN][const.SKU_LIB] = 'SKU'
                config[const.LOGIN][const.ISLINKAGE] = '1'
                if list(const.DATA_ADDR.keys()):
                    for sku_lib in list(const.DATA_ADDR.keys()):
                        config[const.LOGIN][sku_lib+'_IMAGE_INDEX']='0'
            elif filename == '':
                pass

            config.write()
        return config