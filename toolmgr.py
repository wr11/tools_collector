'''工具管理'''

import os
from pathlib import Path
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import define
from mysignal import GetSignalMgr
import shareinterface


class ConstantItem(object):

    DataDict = {
        "ScreenToGif" : "tools/ScreenToGif/ScreenToGif.exe"
    }

class ItemNode(object):
    def __init__(self, name, path):
        self.m_ItemName = name
        self.m_ItemPath = path

    def GetName(self):
        return self.m_ItemName

    def GetPath(self):
        return self.m_ItemPath

class ToolMgr(object):
    '''工具管理：工具所有操作在这管理'''
    def __init__(self):
        self.m_DataDict = {}   # {themeName : [nodeObj, ]}
        self.InitData()
        self.InitConnect()

    def InitData(self):
        '''初始化存盘数据'''
        toolData = self.LoadToolData()
        for themeName, itemlist in toolData.items():
            if itemlist:
                for itemData in itemlist:
                    itemName = itemData.get(define.USERDATAATTR.tool_item_name)
                    itemPath = itemData.get(define.USERDATAATTR.tool_item_path)
                    self.AddItem(themeName, itemName, itemPath)
            else:
                self.AddTheme(themeName)

    def InitConnect(self):
        GetSignalMgr().TURN_TO_EXE.connect(self.TurnToExe)
        GetSignalMgr().OPEN_EXE_PATH.connect(self.OpenExePath)
        GetSignalMgr().DUMP_TOOL_DATA.connect(self.DumpToolData)

    # ----------------------------item-----------------------------
    def AddItem(self, themeName, itemName=None, itemPath=None):
        nodeObj = ItemNode(itemName, itemPath)
        if themeName in self.m_DataDict:
            for tempNodeObj in self.m_DataDict[themeName]:
                nodeName = tempNodeObj.GetName()
                nodePath = tempNodeObj.GetPath()
                if nodePath == itemPath:
                    QtWidgets.QMessageBox.information(None, "提示", f"该工具已存在，其名称为{nodeName}")
                    return
            self.m_DataDict[themeName].append(nodeObj)
        else:
            self.m_DataDict[themeName] = []
            self.m_DataDict[themeName].append(nodeObj)

    def DeleteItem(self, themeName, itemName):
        '''删除item'''
        for nodeObj in self.m_DataDict[themeName]:  # type:ItemNode
            nodeName = nodeObj.GetName()
            if nodeName == itemName:
                self.m_DataDict[themeName].remove(nodeObj)
                break

    def GetItemsByTheme(self, themeName):
        if self.m_DataDict.get(themeName):
            return list(self.m_DataDict.get(themeName))
        else:
            return []

    # ----------------------------item-----------------------------
    def AddTheme(self, themeName):
        '''添加分类'''
        if themeName in self.m_DataDict:
            QtWidgets.QMessageBox.information(None, "提示", f"该分类已存在，勿重复命名")
            return
        self.m_DataDict.update({themeName : []})

    def DeleteTheme(self, themeName):
        '''删除分类'''
        if themeName in self.m_DataDict:
            del self.m_DataDict[themeName]

    def ChangeThemeName(self, oldThemeName, newThemeName):
        '''更改分类名'''
        if oldThemeName not in self.m_DataDict:
            return
        # 为了保持原来的顺序
        Data = {}
        for themeName, itemObjLst in self.m_DataDict.items():
            if themeName != oldThemeName:
                Data.update({themeName : itemObjLst})
            else:
                Data.update({newThemeName : itemObjLst})
        self.m_DataDict = Data

    def GetThemeByItemName(self, itemName):
        for themeName, itemObjLst in self.m_DataDict.items():
            for nodeObj in itemObjLst:
                nodeName = nodeObj.GetName()
                if nodeName == itemName:
                    return themeName
        return None

    def GetTheme(self):
        return list(self.m_DataDict.keys())

    # ----------------------------执行-----------------------------
    def TurnToExe(self, exeName, exePath):
        if self.GetThemeByItemName(exeName) == define.CONSTANTTHEME:
            exePath = os.path.join(os.getcwd(), exePath)
        if not os.path.exists(exePath):
            QtWidgets.QMessageBox.information(None, "提示", f"路径不存在")
            return
        cmd = (str(exePath).replace('/', '\\')).split('\\')[0]
        cmd += f" && cd {str(os.path.dirname(Path(exePath)))}"
        cmd += f" && start {str(os.path.basename(Path(exePath)))}"
        os.popen(cmd)
        # QDesktopServices.openUrl(QUrl.fromLocalFile(exePath))

    def OpenExePath(self, exeName, exePath):
        if self.GetThemeByItemName(exeName) == define.CONSTANTTHEME:
            exePath = os.path.join(os.getcwd(), exePath)
        if not os.path.exists(exePath):
            QtWidgets.QMessageBox.information(None, "提示", f"路径不存在")
            return
        exeParentPath = os.path.dirname(Path(exePath))
        QDesktopServices.openUrl(QUrl.fromLocalFile(exeParentPath + "/"))

    # ----------------------------用户数据-----------------------------
    def GetToolSavaData(self):
        '''要存盘的数据: data={themeName : [{tool_item_name: itemName, tool_item_path: itemPath}, ……]}'''
        userData = {}
        for themeName, itemObjList in self.m_DataDict.items():
            itemList = []
            for itemObj in itemObjList:  # type: ItemNode
                itemData = {}
                itemName = itemObj.GetName()
                itemPath = itemObj.GetPath()
                itemData.update({
                    define.USERDATAATTR.tool_item_name: itemName,
                    define.USERDATAATTR.tool_item_path: itemPath})
                itemList.append(itemData)
            userData.update({themeName: itemList})
        return userData

    @classmethod
    def GetToolDataFilePath(cls):
        '''数据储存路径'''
        path = os.path.join(os.getcwd(), 'Data', define.USER_TOOL_DATA_PATH)  # 工具用户数据文件路径
        return path

    def DumpToolData(self):
        '''工具数据写入'''
        data = self.GetToolSavaData()
        shareinterface.ShareJson.dumps(data, self.GetToolDataFilePath())

    def LoadToolData(self):
        '''工具数据读取'''
        data = shareinterface.ShareJson.loads(self.GetToolDataFilePath())
        return data


g_toolMgr = None

def GetToolMgr():
    global g_toolMgr
    if not g_toolMgr:
        g_toolMgr = ToolMgr()
    return g_toolMgr