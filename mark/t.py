# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 't.py'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

# !/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import *
import sys

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class MainWidget(QMainWindow):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.setWindowTitle(self.tr("依靠窗口"))

        te = QTextEdit(self.tr("主窗口"))
        te.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(te)

        # 停靠窗口 1
        dock1 = QDockWidget(self.tr("停靠窗口 1"), self)
        dock1.setFeatures(QDockWidget.DockWidgetMovable)
        dock1.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        te1 = QTextEdit(self.tr("窗口 1,可在 Main Window 的左部和右部停靠,不可浮动,不可关闭"))
        dock1.setWidget(te1)
        self.addDockWidget(Qt.RightDockWidgetArea, dock1)

        # 停靠窗口 2
        dock2 = QDockWidget(self.tr("停靠窗口 2"), self)
        dock2.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetClosable)
        te2 = QTextEdit(self.tr("窗口 2,只可浮动"))
        dock2.setWidget(te2)
        self.addDockWidget(Qt.RightDockWidgetArea, dock2)

        # 停靠窗口 3
        dock3 = QDockWidget(self.tr("停靠窗口 3"), self)
        dock3.setFeatures(QDockWidget.AllDockWidgetFeatures)
        te3 = QTextEdit(self.tr("窗口 3,可在 Main Window 任意位置停靠,可浮动,可关闭"))
        dock3.setWidget(te3)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock3)


def main():
    app = QApplication(sys.argv)
    main = MainWidget()
    main.show()
    app.exec_()


if __name__ == '__main__':
    main()