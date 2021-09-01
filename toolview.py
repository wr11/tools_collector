'''工具界面'''

import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import define, smalldialog
from mysignal import GetSignalMgr
from toolmgr import GetToolMgr, ToolMgr, ItemNode
from ui_mytool import Ui_Form


class ThemeButton(QtWidgets.QPushButton):
    def __init__(self, name, parent=None):
        super(ThemeButton, self).__init__(name, parent)
        self.m_name = name
        self.setStyleSheet("QPushButton{background: rgb(0, 160, 0); color: white; border-radius: 5px; font-size: 15px; padding: 6px;}"
                           "QPushButton:hover:!pressed{background: rgb(0, 190, 0)}"
                           "QPushButton::pressed{background: rgb(0, 130, 0); padding-top: 6px}")

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.RightButton:
            GetSignalMgr().DELETE_TEHEME.emit(self.m_name)
        super(ThemeButton, self).mousePressEvent(event)

class ItemView(QtWidgets.QDialog):
    '''工具item展示view'''
    def __init__(self, name, path):
        super(ItemView, self).__init__()
        self.m_Name = name
        self.m_Path = path
        self.InitUI()
        self.InitConnect()

    def InitUI(self):
        self.setMouseTracking(True)
        self.setStyleSheet(
           "QWidget{background: rgb(100, 100, 100); border-radius: 10px;}"
           "QWidget:hover{background: rgb(80, 80, 80);}"
           "QPushButton{background: rgb(100, 100, 100); color: rgb(180, 180, 180); border:0px; padding:5px;  border-radius:3px;}"
           "QPushButton:hover{color: rgb(0, 0, 0)}"
           "QPushButton:hover:!pressed{background: rgb(255, 200, 50)}"
           "QPushButton::pressed{background: rgb(214, 165, 42); padding-top: 6px}"
        )
        hlyt_1 = QtWidgets.QHBoxLayout()
        hlyt_2 = QtWidgets.QHBoxLayout()
        hlyt_3 = QtWidgets.QHBoxLayout()
        vlyt = QtWidgets.QVBoxLayout()

        self.name_label = QtWidgets.QLabel(self.m_Name)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.path_label = QtWidgets.QLabel(str(self.m_Path))
        self.turnTo_btn = QtWidgets.QPushButton("打开")
        self.open_path_btn = QtWidgets.QPushButton("位置")
        self.delete_btn = QtWidgets.QPushButton("移除")

        hlyt_1.addWidget(self.name_label)
        hlyt_1.addStretch(1)
        hlyt_2.addWidget(self.path_label)
        hlyt_2.addStretch(1)
        hlyt_3.addStretch(1)
        hlyt_3.addWidget(self.turnTo_btn)
        hlyt_3.addWidget(self.open_path_btn)
        hlyt_3.addWidget(self.delete_btn)
        vlyt.addLayout(hlyt_1)
        vlyt.addLayout(hlyt_2)
        vlyt.addLayout(hlyt_3)
        self.setLayout(vlyt)

    def enterEvent(self, e: QtCore.QEvent):
        self.setStyleSheet(
            "QWidget{background: rgb(80, 80, 80); border-radius: 10px;}"
            "QPushButton{background: rgb(80, 80, 80); color: rgb(180, 180, 180); border:0px; padding:5px;  border-radius:3px;}"
            "QPushButton:hover{color: rgb(0, 0, 0)}"
            "QPushButton:hover:!pressed{background: rgb(255, 200, 50)}"
            "QPushButton::pressed{background: rgb(214, 165, 42); padding-top: 6px}"
        )
        super(ItemView, self).enterEvent(e)

    def leaveEvent(self, e: QtCore.QEvent):
        self.setStyleSheet(
            "QWidget{background: rgb(100, 100, 100); border-radius: 10px;}"
            "QPushButton{background: rgb(100, 100, 100); color: rgb(180, 180, 180); border:0px; padding:5px;  border-radius:3px;}"
            "QPushButton:hover{color: rgb(0, 0, 0)}"
            "QPushButton:hover:!pressed{background: rgb(255, 200, 50)}"
            "QPushButton::pressed{background: rgb(214, 165, 42); padding-top: 6px}"
        )
        super(ItemView, self).leaveEvent(e)

    def InitConnect(self):
        self.turnTo_btn.clicked.connect(self.TurnToExe)
        self.open_path_btn.clicked.connect(self.OpenPath)
        self.delete_btn.clicked.connect(self.DeleteItem)

    def TurnToExe(self):
        GetSignalMgr().TURN_TO_EXE.emit(self.m_Name, self.m_Path)

    def OpenPath(self):
        GetSignalMgr().OPEN_EXE_PATH.emit(self.m_Name, self.m_Path)

    def DeleteItem(self):
        GetSignalMgr().DELETE_ITEN.emit(self.m_Name)
        GetSignalMgr().DUMP_TOOL_DATA.emit()

class ToolView(QtWidgets.QDialog, Ui_Form):

    def __init__(self):
        super(ToolView, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("My Tool")
        self.setAcceptDrops(True)
        self.left_widget.setMinimumWidth(150)
        self.splitter.setStretchFactor(2, 9)
        self.setFixedSize(1082, 863)

        self.InitData()
        self.InitWidget()
        self.InitConnect()

    def InitData(self):
        self.m_ToolMgr = GetToolMgr()
        self.m_CurTheme = define.CONSTANTTHEME  # 当前所选分类
        self.m_TempThemeName = None  # 鼠标右键点击的分类
        self.m_ItemNameToItemViewObj = {}  # 当前分类的item对象 {itemName : itemObj}
        self.m_ThemeNameToThemeBtnObj = {}  # {themeName : themeBtnObj}

    def InitWidget(self):
        self.InitThemeWidget()
        self.InitItemWidget()

    def InitConnect(self):
        GetSignalMgr().DELETE_ITEN.connect(self.DeleteItem)
        GetSignalMgr().DELETE_TEHEME.connect(self.ThemePressByRightBtn)

    @property
    def ToolMgr(self) -> ToolMgr:
        return self.m_ToolMgr

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        '''右键菜单'''
        super(ToolView, self).contextMenuEvent(event)
        if self.GetThemePressByRightBtn():
            menueConfig = [
                {"Menu": "添加分类", "Function": self.AddTheme},
                {"Menu": "删除分类", "Function": self.DeleteTheme},
                {"Menu": "更改分类名", "Function": self.ChangeThemeName},
            ]
        else:
            menueConfig = [ {"Menu": "添加分类", "Function": self.AddTheme}]

        menu = QtWidgets.QMenu()
        for item in menueConfig:
            menu.addAction(item["Menu"], item["Function"])
        menu.exec_(QtGui.QCursor.pos())
        self.m_TempThemeName = None
        event.accept()

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        super(ToolView, self).dragEnterEvent(event)
        event.acceptProposedAction()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        if self.GetCurTheme() == define.CONSTANTTHEME:
            return
        lUrl = event.mimeData().urls()
        if not lUrl or len(lUrl) > 1:
            return
        itemPath = lUrl[0].path().lstrip('/')
        itemName = os.path.splitext(os.path.basename(itemPath))[0]
        itemSuffix = os.path.splitext(itemPath)[1]
        if itemSuffix != ".exe":
            return
        wid = smalldialog.SmallItemAddEditWid(itemName, itemPath)
        if wid.exec_() == QtWidgets.QDialog.rejected:
            return
        itemName = wid.GetItemName()
        itemPath = wid.GetItemPath()
        self.AddItem(itemName, itemPath)
        super(ToolView, self).dropEvent(event)

    def InitThemeWidget(self):
        '''主题view'''
        self.left_widget_layout = QtWidgets.QVBoxLayout()
        self._ShowThemes()
        self.left_widget.setLayout(self.left_widget_layout)

    def _ShowThemes(self):
        self._ClearThemeWidget()
        themeNameList = self.ToolMgr.GetTheme()
        for themeName in themeNameList:
            btn = ThemeButton(themeName)
            btn.clicked.connect(self.CurThemeChange)
            self.left_widget_layout.addWidget(btn)
            self.m_ThemeNameToThemeBtnObj.update({themeName : btn})
        self.left_widget_layout.addStretch(1)

    def _ClearThemeWidget(self):
        for i in reversed(range(self.left_widget_layout.count())):
            themeObj = self.left_widget_layout.itemAt(i)
            if themeObj:
                self.left_widget_layout.removeItem(themeObj)
                themeBtnObj = themeObj.widget()
                if themeBtnObj:
                    self.left_widget_layout.removeWidget(themeBtnObj)
                    themeBtnObj.setParent(None)
                    themeBtnObj.deleteLater()

    def InitItemWidget(self):
        '''item'''
        self.wid = QtWidgets.QWidget()
        self.right_view_layout = QtWidgets.QVBoxLayout()
        self.wid.setLayout(self.right_view_layout)

        hLayout = QtWidgets.QHBoxLayout()
        self.theme_lbl = QtWidgets.QLabel(f'> {self.m_CurTheme}')
        self.add_item_btn = QtWidgets.QPushButton("添加工具")
        self.add_item_btn.clicked.connect(self.SelectItem)
        self.add_item_btn.setStyleSheet("QPushButton{background: rgb(0, 160, 0); color: white; border-radius: 5px; font-size: 15px; padding: 3px;}"
                           "QPushButton:hover:!pressed{background: rgb(0, 190, 0)}"
                           "QPushButton::pressed{background: rgb(0, 130, 0); padding-top: 6px}")
        hLayout.addWidget(self.theme_lbl)
        hLayout.addStretch(1)
        hLayout.addWidget(self.add_item_btn)

        self.search_lineedit = QtWidgets.QLineEdit()
        self.search_lineedit.textChanged.connect(self.OnSearchItem)
        self.search_lineedit.setPlaceholderText("输入工具名搜索")
        self.search_lineedit.setStyleSheet("QLineEdit{background: white; padding: 3px; border-radius: 5px; margin-bottom: 10px;}")

        vLayout = QtWidgets.QVBoxLayout()
        vLayout.addLayout(hLayout)
        vLayout.addWidget(self.search_lineedit)
        self.right_view_layout.addLayout(vLayout)

        # 装item的布局
        self.items_vLayout = QtWidgets.QVBoxLayout()
        self.right_view_layout.addLayout(self.items_vLayout)

        self._ShowItems(self.m_CurTheme)
        self.right_scroll_area.setWidget(self.wid)

    def _ShowItems(self, themeName):
        '''展示item'''
        self.theme_lbl.setText(f'> {themeName}')
        self._ClearItemWidget()

        itemsList = self.ToolMgr.GetItemsByTheme(themeName)
        if not itemsList:
            self.search_lineedit.hide()
            return
        if self.search_lineedit.isHidden():
            self.search_lineedit.show()
        self.m_ItemNameToItemViewObj.clear()
        for itemObj in itemsList:  # type: ItemNode
            itemName = itemObj.GetName()
            itemPath = itemObj.GetPath()
            itemView = ItemView(itemName, itemPath)
            if themeName == define.CONSTANTTHEME:
                itemView.delete_btn.hide()
            self.items_vLayout.addWidget(itemView)
            self.m_ItemNameToItemViewObj.update({itemName : itemView})
        self.right_view_layout.addStretch(4)

    def _ClearItemWidget(self):
        '''清空当前页面的item'''
        for i in reversed(range(self.items_vLayout.count())):
            themeObj = self.items_vLayout.itemAt(i)
            if themeObj:
                self.items_vLayout.removeItem(themeObj)
                themeBtnObj = themeObj.widget()
                if themeBtnObj:
                    self.items_vLayout.removeWidget(themeBtnObj)
                    themeBtnObj.setParent(None)
                    themeBtnObj.deleteLater()

    # --------------------------分类操作--------------------------
    def CurThemeChange(self):
        '''切换分类'''
        themeName = self.sender().text()
        if themeName == self.m_CurTheme:
            return
        self.m_CurTheme = themeName
        self._ShowItems(themeName)

    def GetCurTheme(self):
        return self.m_CurTheme

    def AddTheme(self):
        '''添加分类'''
        wid = smalldialog.SmallThemeAddEditWid()
        if wid.exec_() == QtWidgets.QDialog.rejected:
            return
        themeName = wid.GetThemeName()
        if not themeName:
            QtWidgets.QMessageBox.information(None, "提示", f"请填写分类名")
            return
        self.ToolMgr.AddTheme(themeName)
        self._OnAddTheme(themeName)
        GetSignalMgr().DUMP_TOOL_DATA.emit()

    def _OnAddTheme(self, themeName):
        btn = ThemeButton(themeName)
        btn.clicked.connect(self.CurThemeChange)
        self.left_widget_layout.insertWidget(self.left_widget_layout.count()-1, btn)
        self.m_ThemeNameToThemeBtnObj.update({themeName : btn})

    def ThemePressByRightBtn(self, themeName):
        self.m_TempThemeName = themeName

    def GetThemePressByRightBtn(self):
        return self.m_TempThemeName

    def DeleteTheme(self):
        delThemeName = self.m_TempThemeName
        if delThemeName == define.CONSTANTTHEME:
            return
        self.ToolMgr.DeleteTheme(delThemeName)
        self._ShowThemes()
        if delThemeName == self.GetCurTheme():
            if self.ToolMgr.GetTheme():
                self.m_CurTheme = self.ToolMgr.GetTheme()[0]
            else:
                self.m_CurTheme = None
            self._ShowItems(self.GetCurTheme())
        GetSignalMgr().DUMP_TOOL_DATA.emit()

    def ChangeThemeName(self):
        '''更改分类名称'''
        oldThemeName = self.GetThemePressByRightBtn()
        wid = smalldialog.SmallThemeNameEditWid(oldThemeName)
        if wid.exec_() == QtWidgets.QDialog.rejected:
            return
        newThemeName = wid.GetThemeName()
        if not newThemeName:
            QtWidgets.QMessageBox.information(None, "提示", f"请填写新分类名")
            return
        self.ToolMgr.ChangeThemeName(oldThemeName, newThemeName)
        self._ShowThemes()
        GetSignalMgr().DUMP_TOOL_DATA.emit()

    # --------------------------item操作--------------------------
    def SelectItem(self):
        if self.GetCurTheme() == define.CONSTANTTHEME:
            return
        wid = smalldialog.SmallItemAddEditWid()
        if wid.exec_() == QtWidgets.QDialog.rejected:
            return
        itemName = wid.GetItemName()
        itemPath = wid.GetItemPath()
        if not itemPath:
            QtWidgets.QMessageBox.information(None, "提示", f"未选择工具")
            return
        self.AddItem(itemName, itemPath)

    def AddItem(self, itemName, itemPath):
        '''添加工具'''
        self.ToolMgr.AddItem(self.GetCurTheme(), itemName, itemPath)
        self._ShowItems(self.GetCurTheme())
        GetSignalMgr().DUMP_TOOL_DATA.emit()

    def DeleteItem(self, itemName):
        '''删除工具'''
        self.ToolMgr.DeleteItem(self.GetCurTheme(), itemName)
        self._ShowItems(self.GetCurTheme())

    # --------------------------搜索--------------------------
    def OnSearchItem(self):
        text = self.search_lineedit.text()
        if not text:
            for itemName, itemViewObj in self.m_ItemNameToItemViewObj.items():
                itemViewObj.show()
            return
        for itemName, itemViewObj in self.m_ItemNameToItemViewObj.items():
            if text not in itemName:
                itemViewObj.hide()
            elif itemViewObj.isHidden():
                itemViewObj.show()


def startToolView():
    app = QtWidgets.QApplication(sys.argv)
    tool = ToolView()
    tool.show()
    print("- - - - - - - - Welcome to MyTool, Enjoy Yourself- - - - - - - -")
    sys.exit(app.exec_())