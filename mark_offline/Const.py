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

#菜单条选项
const.CN_MENU_ITEMS = {'file':'文件','edit':'编辑','view':'视图','tools':'工具','language':'语言','help':'帮助'}
const.EN_MENU_ITEMS = {'file':'File','edit':'Edit','view':'View','tools':'Tools','language':'Language','help':'Help'}

#File菜单选项子菜单
const.CN_FILE_MENU_ITEMS ={'open':'打开...','save':'保存','exit':'退出'}
const.EN_FILE_MENU_ITEMS ={'open':'Open...','save':'Save','exit':'Exit'}

#Edit菜单选项子菜单
const.CN_EDIT_MENU_ITEMS = {'refresh':'刷新','toggleCursor':'切换鼠标样式','editCategory':'修改分类','deleteCategory':'删除分类','editCoord':'修改大小','toggleStyle':'切换虚实',
                            'showALl':'显示所有','hideALl':'隐藏所有'}
const.EN_EDIT_MENU_ITEMS = {'refresh':'Refresh','toggleCursor':'Toggle Cursor','editCategory':'Edit Category','deleteCategory':'Delete Category','editCoord':'Edit Coord','toggleStyle':'Toggle Style',
                            'showALl':'Show ALl','hideALl':'Hide ALl'}

#View菜单选项子菜单
const.CN_VIEW_MENU_ITEMS ={'refresh':'刷新'}
const.EN_VIEW_MENU_ITEMS ={'refresh':'Refresh'}
#Tools菜单选项子菜单
const.CN_TOOLS_MENU_ITEMS ={'options':'选项'}
const.EN_TOOLS_MENU_ITEMS ={'options':'Options'}
#language菜单选项子菜单
const.CN_LANGUAGE_MENU_ITEMS ={'cn':'中文','en':'英文'}
const.EN_LANGUAGE_MENU_ITEMS ={'cn':'CN','en':'EN'}
#help菜单选项子菜单
const.CN_HELP_MENU_ITEMS ={'about':'关于'}
const.EN_HELP_MENU_ITEMS ={'about':'About'}
