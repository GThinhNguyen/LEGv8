from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit, QApplication, QMainWindow, QVBoxLayout, QFrame, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor, QPainter, QTextFormat, QFont, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import QRect, Qt, QSize, pyqtSlot, QRegExp

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    def lineNumberAreaWidth(self):
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    @pyqtSlot(int)
    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    @pyqtSlot(QRect, int)
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, int(top), self.lineNumberArea.width(),
                                 self.fontMetrics().height(), Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

class CodeHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Định nghĩa format cho các loại token
        self.keywordFormat = QTextCharFormat()
        self.keywordFormat.setForeground(QColor("#aa00a2"))
        self.keywordFormat.setFontWeight(QFont.Bold)

        self.commentFormat = QTextCharFormat()
        self.commentFormat.setForeground(QColor("#228B22"))
        self.commentFormat.setFontItalic(True)

        self.numberFormat = QTextCharFormat()
        self.numberFormat.setForeground(QColor("#006faa"))

        self.registerFormat = QTextCharFormat()
        self.registerFormat.setForeground(QColor("#050099"))
        self.registerFormat.setFontWeight(QFont.Bold)

        # Danh sách từ khóa LEGv8 hoặc Python
        keywords = [
            "ADD", "SUB", "AND", "ORR", "ADDI", "SUBI", "ANDI", "ORRI", "ANDIS",
            "LDUR", "STUR", "CBZ", "B", "ADDS", "SUBS", "ANDS", "ADDIS", "SUBIS" 
        ]
        self.keywordPatterns = [QRegExp(r'\b' + kw + r'\b') for kw in keywords]
        self.registerPattern = QRegExp(r'\bX[0-9]+\b')
        self.numberPattern = QRegExp(r'\b\d+\b')
        self.commentPattern = QRegExp(r'//.*')

    def highlightBlock(self, text):
        # Tô màu từ khóa
        for pattern in self.keywordPatterns:
            index = pattern.indexIn(text)
            while index >= 0:
                length = pattern.matchedLength()
                self.setFormat(index, length, self.keywordFormat)
                index = pattern.indexIn(text, index + length)
        # Tô màu thanh ghi
        index = self.registerPattern.indexIn(text)
        while index >= 0:
            length = self.registerPattern.matchedLength()
            self.setFormat(index, length, self.registerFormat)
            index = self.registerPattern.indexIn(text, index + length)
        # Tô màu số
        index = self.numberPattern.indexIn(text)
        while index >= 0:
            length = self.numberPattern.matchedLength()
            self.setFormat(index, length, self.numberFormat)
            index = self.numberPattern.indexIn(text, index + length)
        # Tô màu comment
        index = self.commentPattern.indexIn(text)
        while index >= 0:
            length = self.commentPattern.matchedLength()
            self.setFormat(index, length, self.commentFormat)
            index = self.commentPattern.indexIn(text, index + length)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1147, 863)
        
        # Tạo central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Sử dụng QVBoxLayout chính cho toàn bộ giao diện
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        
        # Tạo layout ngang cho phần trên (setting_frame, code_frame, reg_frame)
        self.top_layout = QtWidgets.QHBoxLayout()
        
        # Setting frame
        self.setting_frame = QtWidgets.QFrame(self.centralwidget)
        self.setting_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.setting_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setting_frame.setLineWidth(2)
        self.setting_frame.setObjectName("setting_frame")
        
        # Layout cho setting_frame
        self.setting_layout = QtWidgets.QVBoxLayout(self.setting_frame)
        self.open_bottom = QtWidgets.QPushButton(self.setting_frame)
        self.open_bottom.setObjectName("open_bottom")
        self.setting_layout.addWidget(self.open_bottom)
        
        self.close_bottom = QtWidgets.QPushButton(self.setting_frame)
        self.close_bottom.setObjectName("close_bottom")
        self.setting_layout.addWidget(self.close_bottom)
        
        self.save_bottom = QtWidgets.QPushButton(self.setting_frame)
        self.save_bottom.setObjectName("save_bottom")
        self.setting_layout.addWidget(self.save_bottom)
        
        self.run_all_bottom = QtWidgets.QPushButton(self.setting_frame)
        self.run_all_bottom.setObjectName("run_all_bottom")
        self.setting_layout.addWidget(self.run_all_bottom)
        
        self.run_step_bottom = QtWidgets.QPushButton(self.setting_frame)
        self.run_step_bottom.setObjectName("run_step_bottom")
        self.setting_layout.addWidget(self.run_step_bottom)
        
        self.clean_bottom = QtWidgets.QPushButton(self.setting_frame)
        self.clean_bottom.setObjectName("clean_bottom")
        self.setting_layout.addWidget(self.clean_bottom)
        
        self.help_bottom = QtWidgets.QPushButton(self.setting_frame)
        self.help_bottom.setObjectName("help_bottom")
        self.setting_layout.addWidget(self.help_bottom)

        self.top_layout.addWidget(self.setting_frame)
        
        # Code frame
        self.code_frame = QtWidgets.QFrame(self.centralwidget)
        self.code_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.code_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.code_frame.setObjectName("code_frame")
        
        self.code_layout = QtWidgets.QVBoxLayout(self.code_frame)
        self.codeEditor = CodeEditor(self.code_frame)
        self.codeEditor.setObjectName("codeEditor")
        self.code_layout.addWidget(self.codeEditor)
        
        self.top_layout.addWidget(self.code_frame, stretch=2)  # Cho code_frame chiếm nhiều không gian hơn
        self.highlighter = CodeHighlighter(self.codeEditor.document())
        # Register frame
        self.reg_frame = QtWidgets.QFrame(self.centralwidget)
        self.reg_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.reg_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.reg_frame.setLineWidth(2)
        self.reg_frame.setObjectName("reg_frame")
        
        self.reg_layout = QtWidgets.QGridLayout(self.reg_frame)
        self.registerShow = QtWidgets.QTableWidget(self.reg_frame)
        self.registerShow.setObjectName("registerShow")
        self.registerShow.setColumnCount(1)
        self.registerShow.setRowCount(32)
        for i in range(32):
            item = QtWidgets.QTableWidgetItem()
            self.registerShow.setVerticalHeaderItem(i, item)
        item = QtWidgets.QTableWidgetItem()
        self.registerShow.setHorizontalHeaderItem(0, item)
        
        self.reg_layout.addWidget(self.registerShow, 0, 0, 5, 1)
        
        # Bảng hiển thị RAM
        self.ramTable = QTableWidget(self.reg_frame)
        self.ramTable.setObjectName("ramTable")
        self.ramTable.setColumnCount(4)
        self.ramTable.setRowCount(512)
        self.ramTable.setHorizontalHeaderLabels(["ByteAddress", "ByteValue", "WordAddress", "WordValue"])
        for i in range(512):
            # ByteAddress
            item_addr = QTableWidgetItem(str(i))
            item_addr.setFlags(item_addr.flags() & ~Qt.ItemIsEditable)
            self.ramTable.setItem(i, 0, item_addr)
            # ByteValue (editable)
            self.ramTable.setItem(i, 1, QTableWidgetItem(""))
            # WordAddress every 4 bytes
            if i % 4 == 0:
                w_item = QTableWidgetItem(str(i // 4))
                w_item.setFlags(w_item.flags() & ~Qt.ItemIsEditable)
                self.ramTable.setItem(i, 2, w_item)
            else:
                blank = QTableWidgetItem("")
                blank.setFlags(blank.flags() & ~Qt.ItemIsEditable)
                self.ramTable.setItem(i, 2, blank)
            # WordValue editable for each word row (only first of each 4)
            if i % 4 == 0:
                self.ramTable.setItem(i, 3, QTableWidgetItem(""))
            else:
                # merge cells visually unused
                blank2 = QTableWidgetItem("")
                blank2.setFlags(blank2.flags() & ~Qt.ItemIsEditable)
                self.ramTable.setItem(i, 3, blank2)
            
            for col in range(4):
                item = self.ramTable.item(i, col)
                if item is not None:
                    if item.flags() & Qt.ItemIsEditable:
                        # Ô có thể nhập liệu: màu vàng nhạt
                        item.setBackground(QColor(255, 255, 200))
                    else:
                        # Ô không nhập liệu: màu xám nhạt
                        item.setBackground(QColor(240, 240, 240))

        # Đặt kích thước cột hợp lý
        self.ramTable.resizeColumnsToContents()
        self.ramTable.setFixedWidth(450)
        self.ramTable.verticalHeader().setVisible(False)
        self.reg_layout.addWidget(self.ramTable, 0, 2, 5, 1)

        self.n_flag = QtWidgets.QLabel(self.reg_frame)
        self.n_flag.setStyleSheet("background-color: lightgray;\n"
                                 "border: 2px solid black;\n"
                                 "border-radius: 6px;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 16px;\n"
                                 "qproperty-alignment: AlignCenter;\n")
        self.n_flag.setObjectName("n_flag")
        self.reg_layout.addWidget(self.n_flag, 0, 3, 1, 1)
        
        self.z_flag = QtWidgets.QLabel(self.reg_frame)
        self.z_flag.setStyleSheet("background-color: lightgray;\n"
                                 "border: 2px solid black;\n"
                                 "border-radius: 6px;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 16px;\n"
                                 "qproperty-alignment: AlignCenter;\n")
        self.z_flag.setObjectName("z_flag")
        self.reg_layout.addWidget(self.z_flag, 1, 3, 1, 1)
        
        self.c_flag = QtWidgets.QLabel(self.reg_frame)
        self.c_flag.setStyleSheet("background-color: lightgray;\n"
                                 "border: 2px solid black;\n"
                                 "border-radius: 6px;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 16px;\n"
                                 "qproperty-alignment: AlignCenter;\n")
        self.c_flag.setObjectName("c_flag")
        self.reg_layout.addWidget(self.c_flag, 2, 3, 1, 1)
        
        self.v_flag = QtWidgets.QLabel(self.reg_frame)
        self.v_flag.setStyleSheet("background-color: lightgray;\n"
                                 "border: 2px solid black;\n"
                                 "border-radius: 6px;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 16px;\n"
                                 "qproperty-alignment: AlignCenter;\n")
        self.v_flag.setObjectName("v_flag")
        self.reg_layout.addWidget(self.v_flag, 3, 3, 1, 1)
        
        self.top_layout.addWidget(self.reg_frame)
        
        # Thêm top_layout vào main_layout
        self.main_layout.addLayout(self.top_layout)
        
        # Simulation frame
        self.sim_frame = QtWidgets.QFrame(self.centralwidget)
        self.sim_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.sim_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sim_frame.setLineWidth(2)
        self.sim_frame.setObjectName("sim_frame")
        self.sim_frame.setMinimumSize(1000, 1000)  # Thêm dòng này để đổi kích thước
        
        
        self.main_layout.addWidget(self.sim_frame, stretch=1)
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LEGv8 Simulator"))
        self.open_bottom.setText(_translate("MainWindow", "Open file"))
        self.close_bottom.setText(_translate("MainWindow", "Close file"))
        self.save_bottom.setText(_translate("MainWindow", "Save"))
        self.run_all_bottom.setText(_translate("MainWindow", "Run all"))
        self.run_step_bottom.setText(_translate("MainWindow", "Run by step"))
        self.clean_bottom.setText(_translate("MainWindow", "Clean"))
        self.help_bottom.setText(_translate("MainWindow", "Instructions"))
        self.registerShow.verticalHeaderItem(0).setText(_translate("MainWindow", "X0"))
        self.registerShow.verticalHeaderItem(1).setText(_translate("MainWindow", "X1"))
        self.registerShow.verticalHeaderItem(2).setText(_translate("MainWindow", "X2"))
        self.registerShow.verticalHeaderItem(3).setText(_translate("MainWindow", "X3"))
        self.registerShow.verticalHeaderItem(4).setText(_translate("MainWindow", "X4"))
        self.registerShow.verticalHeaderItem(5).setText(_translate("MainWindow", "X5"))
        self.registerShow.verticalHeaderItem(6).setText(_translate("MainWindow", "X6"))
        self.registerShow.verticalHeaderItem(7).setText(_translate("MainWindow", "X7"))
        self.registerShow.verticalHeaderItem(8).setText(_translate("MainWindow", "X8"))
        self.registerShow.verticalHeaderItem(9).setText(_translate("MainWindow", "X9"))
        self.registerShow.verticalHeaderItem(10).setText(_translate("MainWindow", "X10"))
        self.registerShow.verticalHeaderItem(11).setText(_translate("MainWindow", "X11"))
        self.registerShow.verticalHeaderItem(12).setText(_translate("MainWindow", "X12"))
        self.registerShow.verticalHeaderItem(13).setText(_translate("MainWindow", "X13"))
        self.registerShow.verticalHeaderItem(14).setText(_translate("MainWindow", "X14"))
        self.registerShow.verticalHeaderItem(15).setText(_translate("MainWindow", "X15"))
        self.registerShow.verticalHeaderItem(16).setText(_translate("MainWindow", "X16"))
        self.registerShow.verticalHeaderItem(17).setText(_translate("MainWindow", "X17"))
        self.registerShow.verticalHeaderItem(18).setText(_translate("MainWindow", "X18"))
        self.registerShow.verticalHeaderItem(19).setText(_translate("MainWindow", "X19"))
        self.registerShow.verticalHeaderItem(20).setText(_translate("MainWindow", "X20"))
        self.registerShow.verticalHeaderItem(21).setText(_translate("MainWindow", "X21"))
        self.registerShow.verticalHeaderItem(22).setText(_translate("MainWindow", "X22"))
        self.registerShow.verticalHeaderItem(23).setText(_translate("MainWindow", "X23"))
        self.registerShow.verticalHeaderItem(24).setText(_translate("MainWindow", "X24"))
        self.registerShow.verticalHeaderItem(25).setText(_translate("MainWindow", "X25"))
        self.registerShow.verticalHeaderItem(26).setText(_translate("MainWindow", "X26"))
        self.registerShow.verticalHeaderItem(27).setText(_translate("MainWindow", "X27"))
        self.registerShow.verticalHeaderItem(28).setText(_translate("MainWindow", "X28 (SP)"))
        self.registerShow.verticalHeaderItem(29).setText(_translate("MainWindow", "X29 (FP)"))
        self.registerShow.verticalHeaderItem(30).setText(_translate("MainWindow", "X30 (LR)"))
        self.registerShow.verticalHeaderItem(31).setText(_translate("MainWindow", "X31 (XZR)"))
        self.registerShow.horizontalHeaderItem(0).setText(_translate("MainWindow", "value"))
        self.c_flag.setText(_translate("MainWindow", "C"))
        self.n_flag.setText(_translate("MainWindow", "N"))
        self.z_flag.setText(_translate("MainWindow", "Z"))
        self.v_flag.setText(_translate("MainWindow", "V"))