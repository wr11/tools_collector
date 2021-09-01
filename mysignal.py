'''信号'''

import types
import weakref
from PyQt5 import QtCore

def IsBoundMethod(func):
    if not isinstance(func, types.MethodType):
        return False
    if not func.__self__:
        return False
    return True

def IsDataMgr(obj):
    from myTools import toolmgr
    if isinstance(obj, toolmgr.ToolMgr):
        return True
    return False

class CSignal:
    '''自定义信号'''

    def __init__(self):
        self.m_FuncList = []

    def connect(self, func):
        if IsBoundMethod(func):  # 实例方法
            _obj = weakref.ref(func.__self__)  # 方法调用对象
            _fn = func.__func__
        else:
            _obj = None
            _fn = func
        if _obj and _obj() and IsDataMgr(_obj()):
            self.m_FuncList.insert(0, (_obj, _fn))
        else:
            self.m_FuncList.append((_obj, _fn))

    def emit(self, *args):
        for (_obj, _fn) in self.m_FuncList:
            if not _obj():
                newArgs = list(args)[:_fn.__code__.co_argcount]
                _fn(*newArgs)
                continue
            try:
                obj = _obj()
            except SystemError:
                print(f"Warning! System error: _obj: {_obj}, _fn: {_fn}, args: {args}")
                continue
            if not obj:
                continue
            newArgs = list(args)[:_fn.__code__.co_argcount - 1]
            _fn(obj, *newArgs)

class CSignalMgr(QtCore.QObject):

    DELETE_ITEN = QtCore.pyqtSignal(str)
    DELETE_TEHEME = QtCore.pyqtSignal(str)
    TURN_TO_EXE = QtCore.pyqtSignal(str, str)
    OPEN_EXE_PATH = QtCore.pyqtSignal(str, str)

    DUMP_TOOL_DATA = QtCore.pyqtSignal()  # 储存工具数据
    LOAD_TOOL_DATA = QtCore.pyqtSignal()  # 读取工具数据

g_SignalMgr = None

def GetSignalMgr():
    global g_SignalMgr
    if not g_SignalMgr:
        g_SignalMgr = CSignalMgr()
    return g_SignalMgr