
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1082, 863)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setGeometry(QtCore.QRect(10, 10, 1061, 841))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.left_widget = QtWidgets.QWidget(self.splitter)
        self.left_widget.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.left_widget.setObjectName("left_widget")
        self.right_scroll_area = QtWidgets.QScrollArea(self.splitter)
        self.right_scroll_area.setStyleSheet("background-color: rgb(186, 186, 186);")
        self.right_scroll_area.setWidgetResizable(True)
        self.right_scroll_area.setObjectName("right_scroll_area")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 872, 839))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.right_scroll_area.setWidget(self.scrollAreaWidgetContents_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))