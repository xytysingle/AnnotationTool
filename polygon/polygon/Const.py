#!/usr/bin/env python
#!-*-coding:utf-8 -*-
#!@time    :2018/6/25 21:34
#!@Author :SINGLE
#!@File   :Const.py


class _const:
  class ConstError(TypeError): pass
  class ConstCaseError(ConstError): pass

  def __setattr__(self, name, value):
      if name in self.__dict__:
          raise self.ConstError("can't change const %s" % name)
      if not name.isupper():
          raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
      self.__dict__[name] = value

const = _const()
const.PI = 3.14

#flag
# const.FLAG = False
# const.MENU_BAR = []
# const.MENU_FILE_ITEMS = []
# const.MENU_EDIT_ITEMS = []
const.LOGO=r'./imgs/main.ico'
const.USERNAME='TanXin'
const.PWD='iisnow'
const.ROTATE_ANGLE=5
# 服务器地址
const.SERVER_ADDR="http://ubuntu.zhixiang.co:8889"
# 数据接口
const.SERVER_LOGIN=const.SERVER_ADDR+"/index.php/user/login"
const.SKUS=const.SERVER_ADDR+"/index.php/skus/list?type=1&modifiedSince=0"
const.IMAGES=const.SERVER_ADDR+"/index.phpimage/list"
const.IMAGE=const.SERVER_ADDR+"/index.php/image/view"
const.ANNOTATION=const.SERVER_ADDR+"/index.php/annotation-n/view"
const.ANNOTATION_UPSERT=const.SERVER_ADDR+"/index.php/annotation-n/upsert"
# 数据接口-mars
const.SKUS_MARS=const.SERVER_ADDR+"/index-ms.php?r=/skus/list&type=2&modifiedSince=0"
const.IMAGES_MARS=const.SERVER_ADDR+"/index-ms.php?r=image/list"
const.IMAGE_MARS=const.SERVER_ADDR+"/index-ms.php?r=/image/view&file=100001.jpg"
const.ANNOTATION_MARS=const.SERVER_ADDR+"/index-ms.php?r=annotation/view&image=100001"
const.ANNOTATION_UPSERT_MARS=const.SERVER_ADDR+'/index-ms.php?r=annotation/upsert'

const.DATA_ADDR={
    'SKU':{
        'SERVER_LOGIN':const.SERVER_LOGIN,
        'SKUS':const.SKUS,
        'IMAGES':const.IMAGES,
        'IMAGE':const.IMAGE,
        'ANNOTATION':const.ANNOTATION,
        'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_MARS':{
        'SERVER_LOGIN':const.SERVER_LOGIN,
        'SKUS':const.SKUS_MARS,
        'IMAGES':const.IMAGES_MARS,
        'IMAGE':const.IMAGE_MARS,
        'ANNOTATION':const.ANNOTATION_MARS,
        'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT_MARS
                }
     }
#菜单条选项
const.CN_MENU_ITEMS = {'file':'文件','edit':'编辑','view':'视图','tools':'工具','language':'语言','help':'帮助'}
const.EN_MENU_ITEMS = {'file':'File','edit':'Edit','view':'View','tools':'Tools','language':'Language','help':'Help'}

#File菜单选项子菜单
const.CN_FILE_MENU_ITEMS ={'open':'打开...','save':'保存','openWindow':'新建窗口','importData':'导入标注数据','exportData':'导出标注数据','autoBackup':'自动备份','openSKULib':'SKU库(带秒级搜索引擎)','exit':'退出'}
const.EN_FILE_MENU_ITEMS ={'open':'Open...','save':'Save','openWindow':'Open Window','importData':'Import Data','exportData':'Export Data','autoBackup':'Auto Backup','openSKULib':'Open SKU Lib','exit':'Exit'}

#Edit菜单选项子菜单
const.CN_EDIT_MENU_ITEMS = {'refresh':'刷新','toggleCursor':'切换鼠标样式','editCategory':'重命名','deleteCategory':'删除','editCoord':'编辑','copyCategory':'复制分类','cutBBOX':'剪切BBOX','copyBBOX':'复制BBOX','pasteBBOX':'粘贴BBOX','toggleStyle':'切换虚实',
                            'showALl':'全部选择','hideALl':'清除选择','invertSelect':'反向选择','undo':'撤销','restore':'恢复','copyFileName':'复制BBOX文件名'}
const.EN_EDIT_MENU_ITEMS = {'refresh':'Refresh','toggleCursor':'Toggle Cursor','editCategory':'Rename','deleteCategory':'Delete Category','editCoord':'Edit Coord','cutBBOX':'Cut BBOX','copyCategory':'Copy Category','copyBBOX':'Copy BBOX','pasteBBOX':'Paste BBOX','toggleStyle':'Toggle Style',
                            'showALl':'Show ALl','hideALl':'Hide ALl','invertSelect':'Invert Select','undo':'Undo','restore':'Restore','copyFileName':'Copy File Name'}

#View菜单选项子菜单
const.CN_VIEW_MENU_ITEMS ={'refresh':'刷新','pollmode':'轮询模式','autoLocation':'BBOX自动定位模式','toggleSKU':'切换SKU库','SKU':'饮料SKU库','SKU_MARS':'玛氏SKU库','linkage':'SKU-BBOX联动'}
const.EN_VIEW_MENU_ITEMS ={'refresh':'Refresh','pollmode':'Poll Mode','autoLocation':'Auto Location','toggleSKU':'Toggle SKU Lib','SKU':'Drink SKU Lib','SKU_MARS':'MARS SKU Lib','linkage':'SKU-BBOX Linkage'}
#Tools菜单选项子菜单
const.CN_TOOLS_MENU_ITEMS ={'options':'选项','semiAuto':'半自动标注模式','close':'关闭主面板时','minimize':'最小化','exit':'退出','poweron':'开机启动','welcome':'登录问候语','autologin':'自动登录'}
const.EN_TOOLS_MENU_ITEMS ={'options':'Options','semiAuto':'Semi Auto','close':'Close','minimize':'Minimize','exit':'Exit','poweron':'Power On','welcome':'Login Greeting','autologin':'AutoLogin'}
#language菜单选项子菜单
const.CN_LANGUAGE_MENU_ITEMS ={'cn':'中文','en':'英文','korean':'韩语','japanese':'日语'}
const.EN_LANGUAGE_MENU_ITEMS ={'cn':'CN','en':'EN','korean':'Korean','japanese':'Japanese'}
#help菜单选项子菜单
const.CN_HELP_MENU_ITEMS ={'about':'关于','help':'帮助'}
const.EN_HELP_MENU_ITEMS ={'about':'About','help':'Help'}


#配置文件常量
const.CONFIGNAME='config.ini'
#登录模块
const.LOGIN='Login'
const.ISREMEMBERPWD='IsRememberPwd'
const.ISAUTOLOGIN='IsAutoLogin'
const.USER='User'
const.PSWD='Pwd'
const.ISWELCOMEMSG='IsWelcomeMsg'
#
const.ANNOTATION_DATA='Annotation'

#选项模块
const.LANGUAGE='Language'
const.ISPOWERON='IsPowerOn'
const.ISPOLL='IsPoll'
const.ISLINKAGE='IsLinkage'
const.SKU_LIB='SKU_Lib'
