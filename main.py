import sys
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import simulate        # module của bạn chứa show_polygons_and_lines, animate_squares_along_paths
from mainwindow_ui import Ui_MainWindow  # file pyuic5 sinh ra
from matplotlib.animation import FuncAnimation
from process import handle_open_file, handle_close_file, handle_save_file

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # self.ani = None  # Thêm dòng này để giữ animation

        # Thiết lập UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.ramTable.itemChanged.connect(self.handle_ram_item_changed)
        self.ui.ramTable.cellClicked.connect(self.save_old_value)
        self._old_ram_value = ""
        # Tạo figure và canvas
        self.fig, self.ax = simulate.plt.subplots(figsize=(30, 18))
        simulate.show_polygons(self.ax, simulate.polygons)
        simulate.show_lines(self.ax, simulate.lines)        
        self.ax.set_aspect('equal')
        self.ax.autoscale(enable=True)
        self.ax.invert_yaxis()
        self.ax.axis('off')
        self.canvas = FigureCanvas(self.fig)

        # Đặt canvas vào sim_frame
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.ui.sim_frame.setLayout(layout)
        layout.addWidget(self.canvas)

        self.ui.open_bottom.clicked.connect(lambda: handle_open_file(self.ui))
        self.ui.close_bottom.clicked.connect(lambda: handle_close_file(self.ui))
        self.ui.save_bottom.clicked.connect(lambda: handle_save_file(self.ui))
        self.ui.run_all_bottom.clicked.connect(self.simulate_add)  # Thêm dòng này
        self.ui.run_step_bottom.clicked.connect(self.simulate_add_step)  # Kết nối nút step

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

    def simulate_add(self):
        # Lấy lệnh từ code frame
        code = self.ui.textEdit.toPlainText().strip()
        if not code:
            return

        # Giả sử chỉ xử lý dòng đầu tiên, dạng: ADD Xd, Xn, Xm
        line = code.splitlines()[0]
        parts = line.replace(',', '').split()
        if len(parts) != 4 or parts[0].upper() != "ADD":
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Chỉ hỗ trợ lệnh: ADD Xd, Xn, Xm")
            return

        _, dst, src1, src2 = parts
        # Lấy chỉ số thanh ghi
        dst_idx = int(dst[1:])
        src1_idx = int(src1[1:])
        src2_idx = int(src2[1:])

        # Lấy giá trị hiện tại của các thanh ghi (nếu chưa có thì là 0)
        def get_reg(idx):
            item = self.ui.registerShow.item(idx, 0)
            return int(item.text()) if item and item.text().isdigit() else 0

        val1 = get_reg(src1_idx)
        val2 = get_reg(src2_idx)
        result = val1 + val2

        # Cập nhật kết quả lên thanh ghi đích
        self.ui.registerShow.setItem(dst_idx, 0, QtWidgets.QTableWidgetItem(str(result)))

        # Sau khi xử lý xong, gọi animation (ví dụ animate từ 'Control')
        if self.ani:
            self.ani.event_source.stop()
        self.ani = simulate.animate_square_from_block(
            self.ax, 'Control', simulate.lines, simulate.line_next, square_size=18, interval=20, speed=2
        )
        self.canvas.draw_idle()

    def simulate_add_step(self):
        # Danh sách các block theo thứ tự animation
        order = [
            'PC', 'P1', 'IM', 'P2', 'Control', 'ALUControl', 'P3', 'M1', 'Reg', 'P5',
            'P4', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem', 'M3', 'AND1', 'AND2', 'XOR',
            'SL2', 'P8', 'A1', 'A2', 'M4'
        ]

        # Khởi tạo biến đếm bước nếu chưa có
        if not hasattr(self, 'current_step'):
            self.current_step = 0
        
        # Nếu đã hết order thì quay lại đầu
        if self.current_step >= len(order):
            self.current_step = 0

        block = order[self.current_step]

        # Animate block/line hiện tại
        self.ani = simulate.animate_square_from_block(
            self.ax, block, simulate.lines, simulate.line_next, interval=20, speed=5
        )
        self.canvas.draw_idle()
        self.current_step += 1

    def get_rn_rm_from_code(self):
        """
        Lấy chỉ số Rn, Rm từ dòng đầu tiên của code frame (giả sử dạng: ADD Xd, Xn, Xm)
        Trả về (rn_idx, rm_idx)
        """
        code = self.ui.textEdit.toPlainText().strip()
        if not code:
            return None, None
        line = code.splitlines()[0]
        parts = line.replace(',', '').split()
        if len(parts) != 4 or parts[0].upper() != "ADD":
            return None, None
        # _, dst, rn, rm
        _, _, rn, rm = parts
        try:
            rn_idx = int(rn[1:])
            rm_idx = int(rm[1:])
            return rn_idx, rm_idx
        except Exception:
            return None, None

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()

    w.showMaximized()

    sys.exit(app.exec_())