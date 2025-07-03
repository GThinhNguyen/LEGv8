import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import simulate        # module của bạn chứa show_polygons_and_lines, animate_squares_along_paths
from mainwindow_ui import Ui_MainWindow  # file pyuic5 sinh ra
from matplotlib.animation import FuncAnimation
import bits  # module của bạn chứa dữ liệu bits
from process import handle_open_file, handle_close_file, handle_save_file

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ani = None  # Thêm dòng này để giữ animation

        # Thiết lập UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.current_line_idx = 0
        self.current_step = 0
        self.ui.registerShow.itemChanged.connect(self.handle_register_item_changed)
        self.ui.registerShow.cellClicked.connect(self.save_old_register_value)
        self.ui.ramTable.itemChanged.connect(self.handle_ram_item_changed)
        self.ui.ramTable.cellClicked.connect(self.save_old_value)
        self._old_ram_value = ""
        # Tạo figure và canvas
        self.fig, self.ax = simulate.plt.subplots(figsize=(30, 18))
        # simulate.show_background(self.ax, 'named.jpg')
        simulate.show_polygons(self.ax, simulate.polygons)
        simulate.show_lines(self.ax, simulate.lines)
        simulate.show_points(self.ax, simulate.points)       
        self.ax.invert_yaxis()
        self.ax.set_aspect('equal')
        # self.ax.autoscale(enable=True)
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.fig)


        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        

        scale = 0.72
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        cx = (xlim[0] + xlim[1]) / 2
        cy = (ylim[0] + ylim[1]) / 2 + 220
        width = (xlim[1] - xlim[0]) / scale
        height = (ylim[1] - ylim[0]) / scale
        self.ax.set_xlim(cx - width/2, cx + width/2)
        self.ax.set_ylim(cy - height/2, cy + height/2)

        # Đặt canvas vào sim_frame
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.ui.sim_frame.setLayout(layout)
        layout.addWidget(self.canvas)

        self.ui.open_bottom.clicked.connect(lambda: handle_open_file(self.ui))
        self.ui.close_bottom.clicked.connect(lambda: handle_close_file(self.ui))
        self.ui.save_bottom.clicked.connect(lambda: handle_save_file(self.ui))
        self.ui.run_all_bottom.clicked.connect(self.simulate_all) 
        self.ui.run_step_bottom.clicked.connect(self.simulate_step) 
        self.ui.clean_bottom.clicked.connect(self.handle_clean)
        self.ui.help_bottom.clicked.connect(self.show_instruction)
       # --- Thêm code mặc định ---
        default_code = "ADD X1, X2, X3\nADDI X4, X5, #10"
        self.ui.codeEditor.setPlainText(default_code)

        # --- Thêm dữ liệu mặc định cho thanh ghi ---
        for i in range(10):  # Chỉ gán giá trị cho 10 thanh ghi đầu
            self.ui.registerShow.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))  # Giá trị từ 1 đến 10

    def save_old_register_value(self, row, col):
        item = self.ui.registerShow.item(row, col)
        self._old_register_value = item.text() if item else "0"
    
    def handle_register_item_changed(self, item):
        row = item.row()
        col = item.column()
        if col == 0 and row != 31:
            try:
                val = int(item.text())
                if not (-2147483648 <= val <= 2147483647):
                    raise ValueError
            except Exception:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Chỉ cho phép nhập số nguyên có dấu 32 bit (-2147483648 đến 2147483647).")
                # Quay lại giá trị trước đó
                item.setText(getattr(self, "_old_register_value", "0"))
                return
    
    def highlight_line(self, line_number):
        """Tô vàng dòng line_number (0-based) trong codeEditor."""
        editor = self.ui.codeEditor
        # Xóa highlight cũ
        editor.setExtraSelections([])

        # Chuẩn bị cursor đến dòng cần highlight
        cursor = editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.movePosition(QTextCursor.Down, QTextCursor.MoveAnchor, line_number)
        cursor.select(QTextCursor.LineUnderCursor)

        # Tạo format (nền vàng)
        fmt = QTextCharFormat()
        fmt.setBackground(QColor('#fff176'))  # màu vàng nhạt

        # Đóng gói thành ExtraSelection
        sel = QtWidgets.QTextEdit.ExtraSelection()
        sel.cursor = cursor
        sel.format = fmt

        # Áp dụng lên editor
        editor.setExtraSelections([sel])

    def save_old_value(self, row, col):
        item = self.ui.ramTable.item(row, col)
        self._old_ram_value = item.text() if item else ""
    # Xử lý sự kiện khi người dùng thay đổi giá trị trong bảng RAM
    def handle_ram_item_changed(self, item):
        row = item.row()
        col = item.column()
        # ByteValue (cột 1): chỉ cho phép nhập 8 bit nhị phân
        if col == 1:
            val = item.text()
            if len(val) != 8 or any(c not in '01' for c in val):
                QtWidgets.QMessageBox.warning(self, "Lỗi", "ByteValue chỉ cho phép nhập 8 ký tự 0 hoặc 1.")
                item.setText(self._old_ram_value)
                return
            # Cập nhật WordValue (cột 3) nếu là dòng đầu của word
            word_row = row - (row % 4)
            word = 0
            for i in range(4):
                byte_item = self.ui.ramTable.item(word_row + i, 1)
                byte_str = byte_item.text() if byte_item else "00000000"
                if len(byte_str) == 8 and all(c in '01' for c in byte_str):
                    byte_val = int(byte_str, 2)
                else:
                    byte_val = 0
                word |= (byte_val << (8 * (3 - i)))
            # Xử lý số âm (signed 32-bit)
            if word & 0x80000000:
                word = word - 0x100000000
            word_item = self.ui.ramTable.item(word_row, 3)
            if word_item:
                word_item.setText(str(word))
        # WordValue (cột 3): chỉ cho phép nhập số nguyên có dấu 32 bit
        elif col == 3:
            val = item.text()
            try:
                num = int(val)
                if not (-2147483648 <= num <= 2147483647):
                    raise ValueError
            except Exception:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "WordValue chỉ cho phép nhập số nguyên có dấu từ -2147483648 đến 2147483647.")
                item.setText(self._old_ram_value)
                return
            # Cập nhật 4 ByteValue (cột 1) tương ứng
            # Nếu là số âm, chuyển về unsigned 32-bit để tách byte
            num_unsigned = num & 0xFFFFFFFF
            for i in range(4):
                byte_val = (num_unsigned >> (8 * (3 - i))) & 0xFF
                byte_str = format(byte_val, '08b')
                byte_item = self.ui.ramTable.item(row + i, 1)
                if byte_item:
                    byte_item.setText(byte_str)

    def simulate_all(self):
        order = [
            'PC', 'P1', 'IM', 'P2', 'Control',
            'P3', 'M1', 'Reg', 'P5',  
            'P4', 'ALUControl', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem', 
            'M3', 'Flags', 'AND1', 'AND2', 'OR',
            'SL2', 'P8', 'ADD1', 'ADD2', 'M4'
        ]
        total_lines = self.ui.codeEditor.document().blockCount()
        if not hasattr(self, 'current_step'):
            self.current_step = 0
        if not hasattr(self, 'current_line_idx'):
            self.current_line_idx = 0

        loop_count = 0
        max_loops = 10000
        while self.current_line_idx < total_lines:
            if loop_count >= max_loops:
                QtWidgets.QMessageBox.critical(self, "Lỗi", "Chương trình vượt quá 10000 vòng lặp! Có thể bị lặp vô hạn.")
                break
            while self.current_step < len(order):
                # Kiểm tra lỗi "Khong co lenh" trước khi xử lý từng block
                if bits.data['P2']['Inp0'] == 'Khong co lenh':
                    QtWidgets.QMessageBox.warning(self, "Lỗi", "Không có lệnh tại địa chỉ này!\nDừng mô phỏng.")
                    self.current_step = 0
                    self.current_line_idx = 0
                    bits.reset_data()
                    self.highlight_line(self.current_line_idx)
                    self.canvas.draw_idle()
                    return
                block = order[self.current_step]
                # Gọi hàm chỉ xử lý logic, không tạo animation
                simulate.logic_step_from_block(block, simulate.lines, simulate.line_next, self.ui)
                # Nếu có logic cập nhật thanh ghi khi M3
                if block == 'M3' and int(bits.data['Reg']['RegWrite'],2) == 1:
                    rd= bits.data['Reg']['WriteRegister']
                    rd_value = bits.data['Reg']['WriteData']
                    if int(rd, 2) != 31:
                        self.ui.registerShow.setItem(int(rd,2), 0, QtWidgets.QTableWidgetItem(str(int(rd_value))))
                self.current_step += 1
            simulate.clear_animated_squares(self.ax)
            self.current_step = 0
            self.current_line_idx = int(bits.data['PC']['Inp0'])//4
            if self.current_line_idx < total_lines:
                self.highlight_line(self.current_line_idx)
            loop_count += 1

        QtWidgets.QMessageBox.information(self, "Kết thúc", "Đã chạy hết chương trình!")
        self.current_line_idx = 0
        self.highlight_line(self.current_line_idx)
        bits.reset_data()
        self.canvas.draw_idle()
        
    def simulate_step(self):
        # Danh sách các block theo thứ tự animation
        order = [
            'PC', 'P1', 'IM', 'P2', 'Control',
            'P3', 'M1', 'Reg', 'P5',  
            'P4', 'ALUControl', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem', 
            'M3', 'Flags', 'AND1', 'AND2', 'OR',
            'SL2', 'P8', 'ADD1', 'ADD2', 'M4'
        ]

        total_lines = self.ui.codeEditor.document().blockCount()
        # Khởi tạo biến đếm bước nếu chưa có
        if not hasattr(self, 'current_step'):
            self.current_step = 0
        # Nếu đã hết order thì quay lại đầu
        if self.current_step >= len(order):
            simulate.clear_animated_squares(self.ax) #chạy hết 1 vòng thì xóa các khối vuông
            self.current_step = 0
            self.current_line_idx = int(bits.data['PC']['Inp0'])//4
        if bits.data['P2']['Inp0'] == 'Khong co lenh':
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không có lệnh tại địa chỉ này!\nDừng mô phỏng.")
            self.current_step = 0
            self.current_line_idx = 0
            bits.reset_data()
            self.highlight_line(self.current_line_idx)
            self.canvas.draw_idle()
            return
        if self.current_line_idx >= total_lines:
            QtWidgets.QMessageBox.information(self, "Kết thúc",
                "Đã chạy hết chương trình!")
            # reset về đầu
            self.current_line_idx = 0
            self.highlight_line(self.current_line_idx)
            bits.reset_data()
            return
        self.highlight_line(self.current_line_idx)
        block = order[self.current_step]
        
        # Animate block/line hiện tại
        if self.ani:
            self.ani.event_source.stop()
        self.ani = simulate.animate_square_from_block(
            self.ax, block, simulate.lines, simulate.line_next, self.ui, interval=100, speed=10
        )

        if order[self.current_step] == 'M3' and int(bits.data['Reg']['RegWrite'],2) == 1:
            rd= bits.data['Reg']['WriteRegister']
            rd_value = bits.data['Reg']['WriteData']
            if int(rd, 2) != 31:  # XZR (X31) luôn bằng 0, không cần cập nhật
                self.ui.registerShow.setItem(int(rd,2), 0, QtWidgets.QTableWidgetItem(str(int(rd_value))))

        self.canvas.draw_idle()
        self.current_step += 1

    def handle_clean(self):
        # Đưa giá trị thanh ghi về mặc định (0)
        for i in range(self.ui.registerShow.rowCount()):
            self.ui.registerShow.setItem(i, 0, QtWidgets.QTableWidgetItem("0"))
            item = self.ui.ramTable.item(i, 1)
            item.setBackground(QColor(255, 255, 200))

        for row in range(self.ui.ramTable.rowCount()):
            # ByteValue
            # WordValue
            word_item = QtWidgets.QTableWidgetItem("0")
            if row % 4 == 0:
                word_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
                self.ui.ramTable.setItem(row, 3, word_item)
                word_item.setBackground(QColor(255, 255, 200))  # Nền trắng cho ô chỉnh sửa

        # Đặt lại bits.data về mặc định
        bits.reset_data()

        # Đặt lại current_line_idx, current_step về 0
        self.current_line_idx = 0
        self.current_step = 0

        # Xóa highlight dòng code nếu có
        self.ui.codeEditor.setExtraSelections([])

        # Đặt lại cờ NZCV về mặc định (nếu có)
        if hasattr(self.ui, "n_flag"):
            self.ui.n_flag.setStyleSheet("background-color: lightgray; border: 2px solid black; border-radius: 6px; font-weight: bold; font-size: 16px; qproperty-alignment: AlignCenter;")
        if hasattr(self.ui, "z_flag"):
            self.ui.z_flag.setStyleSheet("background-color: lightgray; border: 2px solid black; border-radius: 6px; font-weight: bold; font-size: 16px; qproperty-alignment: AlignCenter;")
        if hasattr(self.ui, "c_flag"):
            self.ui.c_flag.setStyleSheet("background-color: lightgray; border: 2px solid black; border-radius: 6px; font-weight: bold; font-size: 16px; qproperty-alignment: AlignCenter;")
        if hasattr(self.ui, "v_flag"):
            self.ui.v_flag.setStyleSheet("background-color: lightgray; border: 2px solid black; border-radius: 6px; font-weight: bold; font-size: 16px; qproperty-alignment: AlignCenter;")
        simulate.clear_animated_squares(self.ax)
        self.canvas.draw_idle()

    def show_instruction(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Hướng dẫn sử dụng")
        dialog.resize(1000, 850)  # Chỉnh size tại đây
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        text = QtWidgets.QTextBrowser(dialog)
        text.setHtml(
            "<style>body {font-size:24px;} code {font-size:17px; color:#1976d2;} h2 {font-size:26px;} li {font-size:16px;margin-bottom:8px;} .note {font-size:16px;}</style>"
            "<h2 style='color:#1976d2;'>LEGv8 Simulator - Hướng dẫn sử dụng</h2>"
            "<ul>"
            "<li><b>Mở file:</b> Nhấn <span style='color:#1976d2;'>Open</span> để chọn file mã lệnh LEGv8.</li>"
            "<li><b>Chạy từng bước:</b> Nhấn <span style='color:#1976d2;'>Run by Step</span> để chạy từng bước.</li>"
            "<li><b>Chạy toàn bộ:</b> Nhấn <span style='color:#1976d2;'>Run All</span> để chạy hết chương trình. Nếu đang chạy <span style='color:#1976d2;'>Run by Step</span> thì chương trình sẽ chạy từ bước hiện tại đến hết.</li>"
            "<li><b>Lưu file:</b> Nhấn <span style='color:#1976d2;'>Save</span> để lưu lại mã lệnh.</li>"
            "<li><b>Đóng file:</b> Nhấn <span style='color:#1976d2;'>Close</span> để đóng file hiện tại.</li>"
            "<li><b>Làm sạch:</b> Nhấn <span style='color:#1976d2;'>Clean</span> để reset RAM, thanh ghi và trạng thái đang chạy của <span style='color:#1976d2;'>Run by Step</span>.</li>"
            "<li><b>Xem hướng dẫn:</b> Nhấn <span style='color:#1976d2;'>Instruction</span> để xem hướng dẫn.</li>"
            "</ul>"
            "<hr>"
            "<span class='note'><b>Lưu ý:</b><br>"
            "- <b>XZR (X31)</b> luôn bằng 0, không thể thay đổi.<br>"
            "- RAM 32 bit, nhập ByteValue là 8 ký tự 0/1.<br>"
            "- Thanh ghi 32 bit, nhập giá trị từ -2147483648 đến 2147483647. Kết quả phép tính cho phép bị tràn số.<br>"
            "- Chỉ WordValue dòng đầu mỗi word mới cho phép chỉnh sửa.<br>"
            "- LDUR và STUR chỉ hỗ trợ địa chỉ chia hết cho 4 từ 0 đến 508 (tương ứng với 128 dòng RAM).<br>"
            "- Mỗi dòng code phải viết liền nhau, không được có dòng trống. Địa chỉ các dòng code bắt đầu từ 0 và cách nhau 4 byte.<br>"
            "- Các lệnh nhánh (B, CBZ, B.cond) trường #imm là số dòng nhảy, chiều dương hướng xuống.<br>"
            "- Có thể dùng dấu <code>//</code> để chú thích trong code, nhưng phải đảm bảo dòng nào cũng có code.</span>"
            "<hr>"
            "<h3 style='color:#1976d2;'>Cú pháp các lệnh cơ bản</h3>"
            "<ul>"
            "<li><b>ADD, SUB, AND, ORR, EOR, ADDS, SUBS, ANDS:</b><br> <code>ADD Xd, Xn, Xm</code></li>"
            "<li><b>ADDI, SUBI, ANDI, ORRI, EORI, ADDIS, SUBIS, ANDIS:</b><br> <code>ADDI Xd, Xn, #imm</code></li>"
            "<li><b>LDUR, STUR:</b><br> <code>LDUR Xd, [Xn, #imm]</code></li>"
            "<li><b>CBZ:</b><br> <code>CBZ Xn, #imm</code></li>"
            "<li><b>B:</b><br> <code>B #imm</code></li>"
            "<li><b>B.cond:</b><br> <code>B.EQ #imm</code> (các điều kiện: EQ, NE, MI, PL, VS, VC, GE, LT, GT, LE)</li>"
            "</ul>"
            "<hr>"
            "<i>Giáo viên hướng dẫn: Phạm Tuấn Sơn </i><br>"
            "<i>Sinh viên thực hiện: Nguyễn Ngọc Tin, Nguyễn Gia Thịnh </i>"
        )
        text.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(text)

        dialog.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()

    w.showMaximized()

    sys.exit(app.exec_())