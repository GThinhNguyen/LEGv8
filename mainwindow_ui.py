# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

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
        
        self.stop_bottom = QtWidgets.QPushButton(self.setting_frame)
        self.stop_bottom.setObjectName("stop_bottom")
        self.setting_layout.addWidget(self.stop_bottom)
        
        self.top_layout.addWidget(self.setting_frame)
        
        # Code frame
        self.code_frame = QtWidgets.QFrame(self.centralwidget)
        self.code_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.code_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.code_frame.setObjectName("code_frame")
        
        self.code_layout = QtWidgets.QVBoxLayout(self.code_frame)
        self.textEdit = QtWidgets.QTextEdit(self.code_frame)
        self.textEdit.setObjectName("textEdit")
        self.code_layout.addWidget(self.textEdit)
        
        self.top_layout.addWidget(self.code_frame, stretch=2)  # Cho code_frame chiếm nhiều không gian hơn
        
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
        
        self.n_flag = QtWidgets.QLabel(self.reg_frame)
        self.n_flag.setStyleSheet("background-color: lightgray;\n"
                                 "border: 2px solid black;\n"
                                 "border-radius: 6px;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 16px;\n"
                                 "qproperty-alignment: AlignCenter;\n")
        self.n_flag.setObjectName("n_flag")
        self.reg_layout.addWidget(self.n_flag, 0, 1, 1, 1)
        
        self.z_flag = QtWidgets.QLabel(self.reg_frame)
        self.z_flag.setStyleSheet("background-color: lightgray;\n"
                                 "border: 2px solid black;\n"
                                 "border-radius: 6px;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 16px;\n"
                                 "qproperty-alignment: AlignCenter;\n")
        self.z_flag.setObjectName("z_flag")
        self.reg_layout.addWidget(self.z_flag, 1, 1, 1, 1)
        
        self.c_flag = QtWidgets.QLabel(self.reg_frame)
        self.c_flag.setStyleSheet("background-color: lightgray;\n"
                                 "border: 2px solid black;\n"
                                 "border-radius: 6px;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 16px;\n"
                                 "qproperty-alignment: AlignCenter;\n")
        self.c_flag.setObjectName("c_flag")
        self.reg_layout.addWidget(self.c_flag, 2, 1, 1, 1)
        
        self.v_flag = QtWidgets.QLabel(self.reg_frame)
        self.v_flag.setStyleSheet("background-color: lightgray;\n"
                                 "border: 2px solid black;\n"
                                 "border-radius: 6px;\n"
                                 "font-weight: bold;\n"
                                 "font-size: 16px;\n"
                                 "qproperty-alignment: AlignCenter;\n")
        self.v_flag.setObjectName("v_flag")
        self.reg_layout.addWidget(self.v_flag, 3, 1, 1, 1)
        
        self.top_layout.addWidget(self.reg_frame)
        
        # Thêm top_layout vào main_layout
        self.main_layout.addLayout(self.top_layout)
        
        # Simulation frame
        self.sim_frame = QtWidgets.QFrame(self.centralwidget)
        self.sim_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.sim_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sim_frame.setLineWidth(2)
        self.sim_frame.setObjectName("sim_frame")
        
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_bottom.setText(_translate("MainWindow", "Open file"))
        self.close_bottom.setText(_translate("MainWindow", "Close file"))
        self.save_bottom.setText(_translate("MainWindow", "Save"))
        self.run_all_bottom.setText(_translate("MainWindow", "Run all"))
        self.run_step_bottom.setText(_translate("MainWindow", "Run by step"))
        self.stop_bottom.setText(_translate("MainWindow", "Stop"))
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