# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spider_demo.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(865, 436)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setObjectName("listWidget_2")
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_2.addItem(item)
        self.verticalLayout.addWidget(self.listWidget_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 275, 308))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setMaximumSize(QtCore.QSize(60, 23))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setMaximumSize(QtCore.QSize(60, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setMaximumSize(QtCore.QSize(133, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_2.addWidget(self.lineEdit_3, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setMaximumSize(QtCore.QSize(75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignLeft)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label, 0, QtCore.Qt.AlignLeft)
        self.verticalLayout_3.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 865, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName("action1")
        self.action22 = QtWidgets.QAction(MainWindow)
        self.action22.setObjectName("action22")
        self.menu.addAction(self.action1)
        self.menu.addSeparator()
        self.menu.addAction(self.action22)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "搜索分类"))
        __sortingEnabled = self.listWidget_2.isSortingEnabled()
        self.listWidget_2.setSortingEnabled(False)
        item = self.listWidget_2.item(0)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(1)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(2)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(3)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(4)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(5)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(6)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(7)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(8)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(9)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(10)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(11)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(12)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(13)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(14)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(15)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(16)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(17)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(18)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(19)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(20)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(21)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(22)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(23)
        item.setText(_translate("MainWindow", "新建项目"))
        item = self.listWidget_2.item(24)
        item.setText(_translate("MainWindow", "新建项目"))
        self.listWidget_2.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("MainWindow", "上一张<<"))
        self.pushButton_2.setText(_translate("MainWindow", "下一张>>"))
        self.pushButton_3.setText(_translate("MainWindow", "搜索"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action1.setText(_translate("MainWindow", "保存"))
        self.action22.setText(_translate("MainWindow", "退出"))

