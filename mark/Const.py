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
const.ROTATE_ANGLE=1
# 服务器地址
# const.SERVER_ADDR="http://ubuntu.zhixiang.co:8889"
#const.SERVER_ADDR="http://annotation.lingmou.ai:8000"
const.SERVER_ADDR="http://192.168.3.4:8000"
# 数据接口
const.SERVER_LOGIN=const.SERVER_ADDR+"/index.php/user/login"
const.SKUS=const.SERVER_ADDR+"/index.php/skus/list?"
const.SKUS_LIB_LIST=const.SERVER_ADDR+"/index.php/skus/type-list"
const.IMAGES=const.SERVER_ADDR+"/index.phpimage/list"
const.IMAGE=const.SERVER_ADDR+"/index.php/image/view"
const.ANNOTATION=const.SERVER_ADDR+"/index.php/annotation/view"
const.ANNOTATION_UPSERT=const.SERVER_ADDR+"/index.php/annotation/upsert"
# 数据接口-mars
const.SKUS_MARS=const.SERVER_ADDR+"/index-ms.php?r=/skus/list&type=2&modifiedSince=0"
const.IMAGES_MARS=const.SERVER_ADDR+"/index-ms.php?r=image/list"
const.IMAGE_MARS=const.SERVER_ADDR+"/index-ms.php?r=/image/view&file=100001.jpg"
const.ANNOTATION_MARS=const.SERVER_ADDR+"/index-ms.php?r=annotation/view&image=100001"
const.ANNOTATION_UPSERT_MARS=const.SERVER_ADDR+'/index-ms.php?r=annotation/upsert'

const.DATA_ADDR={
    'SKU':{
        'SERVER_LOGIN':const.SERVER_LOGIN,
        'SKUS':const.SKUS+'type=1',
        'IMAGES':const.IMAGES,
        'IMAGE':const.IMAGE,
        'ANNOTATION':const.ANNOTATION,
        'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_MARS':{
        'SERVER_LOGIN':const.SERVER_LOGIN,
        'SKUS':const.SKUS+'type=2',
        'IMAGES':const.IMAGES_MARS,
        'IMAGE':const.IMAGE_MARS,
        'ANNOTATION':const.ANNOTATION_MARS,
        'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT_MARS
        },
    'SKU_MOUTH':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=6',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_SEASONING':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=7',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_CLEANING':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=8',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_MB_PRODUCTS':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=9',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_LIQUORS':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=10',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_BEER':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=11',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_JTHJQJ':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=12',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_HEALTH_CARE':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=13',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_PAPER':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=14',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_HAIR':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=15',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_CLOTHES_CLEAN':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=16',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_FACIAL_CARE':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=17',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_DRINKS_RICH':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=18',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_SNACK_FOOD':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=19',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_NON-ANNOTATION_PRODUCTS':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=20',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_DRINK_GRUOP':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=22',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_OTHER_WINE':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=23',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_PRICE_TAG':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=24',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_PICKER':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=25',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },	
    'SKU_ALL_CATEGORIES':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=26',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },	
    'SKU_VIVID_MATERIAL':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=27',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },
    'SKU_UNPACK':{
            'SERVER_LOGIN':const.SERVER_LOGIN,
            'SKUS':const.SKUS+'type=28',
            'IMAGES':const.IMAGES,
            'IMAGE':const.IMAGE,
            'ANNOTATION':const.ANNOTATION,
            'ANNOTATION_UPSERT':const.ANNOTATION_UPSERT
        },		
     }
#菜单条选项
const.CN_MENU_ITEMS = {'file':'文件','edit':'编辑','view':'视图','tools':'工具','language':'语言','help':'帮助'}
const.EN_MENU_ITEMS = {'file':'File','edit':'Edit','view':'View','tools':'Tools','language':'Language','help':'Help'}

#File菜单选项子菜单
const.CN_FILE_MENU_ITEMS ={'open':'打开...','save':'保存','openWindow':'新建窗口','importData':'导入标注数据','exportData':'导出标注数据','autoBackup':'自动备份','openSKULib':'SKU库(带秒级搜索引擎)','exit':'退出'}
const.EN_FILE_MENU_ITEMS ={'open':'Open...','save':'Save','openWindow':'Open Window','importData':'Import Data','exportData':'Export Data','autoBackup':'Auto Backup','openSKULib':'Open SKU Lib','exit':'Exit'}

#Edit菜单选项子菜单
const.CN_EDIT_MENU_ITEMS = {'refresh':'刷新','toggleCursor':'切换鼠标样式','editCategory':'重命名','deleteCategory':'删除','editCoord':'编辑','copyCategory':'复制分类','cutBBOX':'剪切BBOX','copyBBOX':'复制BBOX','pasteBBOX':'粘贴BBOX','toggleStyle':'切换虚实',
                            'showALl':'全部选择','hideALl':'清除选择','invertSelect':'反向选择','undo':'撤销','restore':'恢复','copyFileName':'复制BBOX文件名','editProperty':'编辑属性'}
const.EN_EDIT_MENU_ITEMS = {'refresh':'Refresh','toggleCursor':'Toggle Cursor','editCategory':'Rename','deleteCategory':'Delete Category','editCoord':'Edit Coord','cutBBOX':'Cut BBOX','copyCategory':'Copy Category','copyBBOX':'Copy BBOX','pasteBBOX':'Paste BBOX','toggleStyle':'Toggle Style',
                            'showALl':'Show ALl','hideALl':'Hide ALl','invertSelect':'Invert Select','undo':'Undo','restore':'Restore','copyFileName':'Copy File Name','editProperty':'Edit Property'}

#View菜单选项子菜单
const.CN_VIEW_MENU_ITEMS ={'refresh':'刷新','pollmode':'轮询模式','autoLocation':'BBOX自动定位模式','toggleSKU':'切换SKU库',
                           'SKU':'饮料SKU库','SKU_MARS':'玛氏SKU库','SKU_MOUTH':'口腔清洁SKU库','SKU_SEASONING':'粮油调味SKU库',
                           'SKU_CLEANING':'个护清洁','SKU_MB_PRODUCTS':'母婴用品','SKU_LIQUORS':'洋酒','SKU_BEER':'啤酒',
                           'SKU_PAPER':'清洁纸品','SKU_JTHJQJ':'家庭环境清洁','SKU_HEALTH_CARE':'身体护理','SKU_HAIR':'洗发护发',
                           'SKU_CLOTHES_CLEAN':'衣物清洁','SKU_FACIAL_CARE':'面部护理','SKU_DRINKS_RICH':'饮料冲调',
                           'SKU_SNACK_FOOD':'休闲食品','SKU_NON-ANNOTATION_PRODUCTS':'非标品','SKU_DRINK_GRUOP':'饮料组合装',
                           'SKU_PRICE_TAG':'价签','SKU_OTHER_WINE':'其他酒类','SKU_PICKER':'检出器','SKU_ALL_CATEGORIES':'全品类',
						   'SKU_VIVID_MATERIAL':'生动化物料','SKU_UNPACK':'开箱后排',
                           'linkage':'SKU-BBOX联动'}
const.EN_VIEW_MENU_ITEMS ={'refresh':'Refresh','pollmode':'Poll Mode','autoLocation':'Auto Location','toggleSKU':'Toggle SKU Lib',
                           'SKU':'Drink SKU Lib','SKU_MARS':'MARS SKU Lib','SKU_MOUTH':'SKU MOUTH','SKU_SEASONING':'SKU SEASONING',
                           'SKU_CLEANING':'SKU CLEANING','SKU_MB_PRODUCTS':'SKU MB_PRODUCTS','SKU_LIQUORS':'SKU LIQUORS','SKU_BEER':'SKU BEER',
                           'SKU_PAPER':'SKU PAPER','SKU_JTHJQJ':'SKU JTHJQJ','SKU_HEALTH_CARE':'SKU HEALTH CARE','SKU_HAIR':'SKU HAIR',
                            'SKU_CLOTHES_CLEAN':'SKU CLOTHES CLEAN','SKU_FACIAL_CARE':'SKU FACIAL CARE','SKU_DRINKS_RICH':'SKU DRINKS RICH',
                           'SKU_SNACK_FOOD':'SKU SNACK FOOD','SKU_NON-ANNOTATION_PRODUCTS':'SKU ON-ANNOTATION PRODUCTS','SKU_DRINK_GRUOP':'SKU DRINK GRUOP',
                            'SKU_PRICE_TAG':'SKU PRICE TAG','SKU_OTHER_WINE':'SKU OTHER WINE','SKU_PICKER':'SKU PICKER','SKU_ALL_CATEGORIES':'SKU ALL CATEGORIES',
							'SKU_VIVID_MATERIAL':'SKU VIVID MATERIAL','SKU_UNPACK':'SKU UNPACK',
                           'linkage':'SKU-BBOX Linkage'}
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
const.ZOOM_LEVEL='ZOOM_LEVEL'
