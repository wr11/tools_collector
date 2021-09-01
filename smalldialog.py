'''这里是一些小窗口'''

import os

from PyQt5 import QtWidgets, QtCore


class SmallThemeAddEditWid(QtWidgets.QDialog):
    def __init__(self):
        super(SmallThemeAddEditWid, self).__init__()
        hLayout_1 = QtWidgets.QHBoxLayout()
        themeName_lbl = QtWidgets.QLabel("类名:")
        self.themeName_lineedit = QtWidgets.QLineEdit()
        hLayout_1.addWidget(themeName_lbl)
        hLayout_1.addWidget(self.themeName_lineedit)

        hLayout_2 = QtWidgets.QHBoxLayout()
        self.ButtonBox = QtWidgets.QDialogButtonBox(self)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.ButtonBox.accepted.connect(self.accept)
        self.ButtonBox.rejected.connect(self.reject)
        hLayout_2.addWidget(self.ButtonBox)

        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addLayout(hLayout_1)
        vLayout.addLayout(hLayout_2)
        self.setLayout(vLayout)

        self.setWindowTitle("新增分类")

    def GetThemeName(self):
        return self.themeName_lineedit.text()

class SmallThemeNameEditWid(QtWidgets.QDialog):
    def __init__(self, oldName):
        super(SmallThemeNameEditWid, self).__init__()

        hLayout_1 = QtWidgets.QHBoxLayout()
        themeName_lbl = QtWidgets.QLabel("新类名")
        self.themeName_lineedit = QtWidgets.QLineEdit()
        self.themeName_lineedit.setText(oldName)
        hLayout_1.addWidget(themeName_lbl)
        hLayout_1.addWidget(self.themeName_lineedit)

        hLayout_2 = QtWidgets.QHBoxLayout()
        self.ButtonBox = QtWidgets.QDialogButtonBox(self)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.ButtonBox.accepted.connect(self.accept)
        self.ButtonBox.rejected.connect(self.reject)
        hLayout_2.addWidget(self.ButtonBox)

        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addLayout(hLayout_1)
        vLayout.addLayout(hLayout_2)
        self.setLayout(vLayout)
        self.setWindowTitle("修改分类名")

    def GetThemeName(self):
        return self.themeName_lineedit.text()

class SmallItemAddEditWid(QtWidgets.QDialog):
    def __init__(self, name=None, path=None):
        super(SmallItemAddEditWid, self).__init__()

        hLayout_1 = QtWidgets.QHBoxLayout()
        itemName_lbl = QtWidgets.QLabel("名称:")
        self.itemName_lineedit = QtWidgets.QLineEdit()
        if name:
            self.itemName_lineedit.setText(name)
        else:
            self.itemName_lineedit.setPlaceholderText("默认为工具名~")
        hLayout_1.addWidget(itemName_lbl)
        hLayout_1.addWidget(self.itemName_lineedit)

        hLayout_2 = QtWidgets.QHBoxLayout()
        itemPath_lbl = QtWidgets.QLabel("路径:")
        self.itemPath_lineedit = QtWidgets.QLineEdit()
        if path:
            self.itemPath_lineedit.setText(path)
        self.itemPath_lineedit.textChanged.connect(self.ItemPathChange)
        self.item_select_btn = QtWidgets.QPushButton("浏览")
        self.item_select_btn.clicked.connect(self.SelectItem)
        hLayout_2.addWidget(itemPath_lbl)
        hLayout_2.addWidget(self.itemPath_lineedit)
        hLayout_2.addWidget(self.item_select_btn)

        hLayout_3 = QtWidgets.QHBoxLayout()
        self.ButtonBox = QtWidgets.QDialogButtonBox(self)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.ButtonBox.accepted.connect(self.accept)
        self.ButtonBox.rejected.connect(self.reject)
        hLayout_3.addWidget(self.ButtonBox)

        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addLayout(hLayout_2)
        vLayout.addLayout(hLayout_1)
        vLayout.addLayout(hLayout_3)
        self.setLayout(vLayout)

        self.setWindowTitle("添加工具")
        self.setFixedWidth(300)

    def SelectItem(self):
        itemPath, _ = QtWidgets.QFileDialog.getOpenFileName(None, "选择exe", "", ".exe")
        if not itemPath:
            return
        self.itemPath_lineedit.setText(itemPath)

    def ItemPathChange(self):
        if not self.itemName_lineedit and self.itemPath_lineedit.text():
            self.itemName_lineedit.setPlaceholderText(str(os.path.basename(self.itemPath_lineedit.text())).strip('.')[0])

    def GetItemName(self):
        itemName = self.itemName_lineedit.text()
        if not itemName and self.itemPath_lineedit.text():
            itemName = str(os.path.basename(self.itemPath_lineedit.text())).strip('.')[0]
        return itemName

    def GetItemPath(self):
        return self.itemPath_lineedit.text()