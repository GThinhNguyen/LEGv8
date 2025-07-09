import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import simulate        # module của bạn chứa show_polygons_and_lines, animate_squares_along_paths
from mainwindow_ui import Ui_MainWindow  # file pyuic5 sinh ra
from matplotlib.animation import FuncAnimation
import bits  # module của bạn chứa dữ liệu bits


import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

# Biến toàn cục lưu đường dẫn file hiện tại
current_file_path = None


class StateManager:
    """Quản lý trạng thái UI (registers, RAM, flags)"""
    
    def __init__(self, ui):
        self.ui = ui
        self.register_backup = []
        self.ram_backup = []
        self.flags_backup = []
        self.line_backup = []
        self.step_backup = []
        self.MAX_BACKUP = 30
    
    def backup_ui_state_for_step(self, current_line_idx, current_step):
        """Backup trạng thái UI cho step"""
        state = {
            'registers': self._get_register_state(),
            'ram': self._get_ram_state(),
            'line_idx': current_line_idx,
            'step': current_step
        }
        self.step_backup.append(state)
        if len(self.step_backup) > self.MAX_BACKUP:
            self.step_backup.pop(0)
    
    def backup_ui_state_for_line(self, current_line_idx, current_step):
        """Backup trạng thái UI cho line"""
        state = {
            'registers': self._get_register_state(),
            'ram': self._get_ram_state(),
            'line_idx': current_line_idx,
            'step': current_step
        }
        self.line_backup.append(state)
        if len(self.line_backup) > self.MAX_BACKUP:
            self.line_backup.pop(0)
    
    def restore_ui_state_from_step(self):
        """Khôi phục trạng thái UI từ step backup"""
        if not self.step_backup:
            return None
        
        state = self.step_backup.pop()
        self._restore_register_state(state['registers'])
        self._restore_ram_state(state['ram'])
        return state['line_idx'], state['step']
    
    def restore_ui_state_from_line(self):
        """Khôi phục trạng thái UI từ line backup"""
        if not self.line_backup:
            return None
        
        state = self.line_backup.pop()
        self._restore_register_state(state['registers'])
        self._restore_ram_state(state['ram'])
        return state['line_idx'], state['step']

    def _get_ram_state(self):
        """Lấy trạng thái hiện tại của RAM"""
        ram = {}
        
        # Kiểm tra UI objects có tồn tại không
        if not hasattr(self, 'ui') or not hasattr(self.ui, 'ramTable'):
            return ram
        
        for i in range(512):
            # ByteValue
            byte_item = self.ui.ramTable.item(i, 1)
            if byte_item and byte_item.text() != "":
                ram[f"byte_{i}"] = byte_item.text()
            else:
                ram[f"byte_{i}"] = "00000000"
            # WordValue (chỉ lưu cho dòng đầu mỗi word)
            if i % 8 == 0:
                word_item = self.ui.ramTable.item(i, 3)
            if word_item and word_item.text() != "":
                ram[f"word_{i}"] = word_item.text()
            else:
                ram[f"word_{i}"] = "0"

        return ram
    
    def _get_register_state(self):
        """Lấy trạng thái hiện tại của registers"""
        registers = {}

        # Kiểm tra UI objects có tồn tại không
        if not hasattr(self, 'ui') or not hasattr(self.ui, 'registerShow'):
            return registers

        try:
            for i in range(32):
                item = self.ui.registerShow.item(i, 0)
                # Nếu chưa có giá trị hoặc giá trị rỗng, mặc định là "0"
                if item is None or item.text() is None or item.text().strip() == "":
                    registers[i] = "0"
                else:
                    registers[i] = item.text()
        except (RuntimeError, AttributeError):
            # UI object đã bị xóa hoặc không tồn tại
            pass

        return registers

    def _restore_register_state(self, registers):
        """Khôi phục trạng thái registers"""
        for i, value in registers.items():
            if i != 31:  # Không restore XZR
                self.ui.registerShow.setItem(i, 0, QtWidgets.QTableWidgetItem(value))
    
    def _restore_ram_state(self, ram):
        """Khôi phục trạng thái RAM"""
        for key, value in ram.items():
            if key.startswith("byte_"):
                row = int(key.split("_")[1])
                self.ui.ramTable.setItem(row, 1, QtWidgets.QTableWidgetItem(value))
            elif key.startswith("word_"):
                row = int(key.split("_")[1])
                if row % 8 == 0:
                    self.ui.ramTable.setItem(row, 3, QtWidgets.QTableWidgetItem(value))
    
    def can_undo_step(self):
        """Kiểm tra có thể undo step không"""
        return len(self.step_backup) > 0
    
    def can_undo_line(self):
        """Kiểm tra có thể undo line không"""
        return len(self.line_backup) > 0
    


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ani = None
        
        # Khởi tạo UI (chỉ một lần)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Khởi tạo các biến trạng thái
        self.current_line_idx = 0
        self.current_step = 0
        self.check_in_checkpoint = 0

        # Khởi tạo StateManager SAU khi UI đã sẵn sàng
        self.state_manager = StateManager(self.ui)

        # Thiết lập kết nối signals
        self.ui.registerShow.itemChanged.connect(self.handle_register_item_changed)
        self.ui.registerShow.cellClicked.connect(self.save_old_register_value)
        self.ui.ramTable.itemChanged.connect(self.handle_ram_item_changed)
        self.ui.ramTable.cellClicked.connect(self.save_old_value)
        self._old_ram_value = ""

        # Tạo figure và canvas
        self.fig, self.ax = simulate.setup_simulation_plot(figsize=(30, 18))
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

        # Kết nối các nút
        self.ui.open_button.clicked.connect(self.handle_open_file)
        self.ui.close_button.clicked.connect(self.handle_close_file)
        self.ui.save_button.clicked.connect(self.handle_save_file)
        self.ui.run_all_button.clicked.connect(self.run_all)
        self.ui.run_by_step_button.clicked.connect(self.handle_run_by_step_click)
        self.ui.clean_button.clicked.connect(self.handle_clean)
        self.ui.instruction_button.clicked.connect(self.show_instruction)
        self.ui.animate_button.clicked.connect(self.handle_animate_button)
        self.ui.speed_slider.valueChanged.connect(self.update_animation_speed)
        self.ui.run_by_line_button.clicked.connect(self.run_by_line)
        self.ui.run_to_checkpoint_button.clicked.connect(self.run_to_checkpoint)
        # Kết nối các nút undo
        self.ui.last_step_button.clicked.connect(self.handle_last_step)
        self.ui.last_line_button.clicked.connect(self.handle_last_line)
        
       # --- Thêm code mặc định ---
        default_code = (
            "ADD X1,X2,X3\n"
            "SUB X4,X1,X3"
        )
        self.ui.codeEditor.setPlainText(default_code)
        # Đặt giá trị mặc định cho các thanh ghi: X0-X9 = 1..10, X10-X30 = 0, X31 (XZR) = 0
        for i in range(self.ui.registerShow.rowCount()-1):
            if i < 10:
                value = str(i + 1)
            else:
                value = "0"
            self.ui.registerShow.setItem(i, 0, QtWidgets.QTableWidgetItem(value))

        # Đặt giá trị mặc định cho RAM: tất cả byte = "00000000", word đầu mỗi 8 dòng = "0"
        for i in range(self.ui.ramTable.rowCount()):
            self.ui.ramTable.setItem(i, 1, QtWidgets.QTableWidgetItem("00000000"))
            if i % 8 == 0:
                self.ui.ramTable.setItem(i, 3, QtWidgets.QTableWidgetItem("0"))

        # Khôi phục trạng thái UI về mặc định
        self.state_manager._restore_register_state(self.state_manager._get_register_state())
        self.state_manager._restore_ram_state(self.state_manager._get_ram_state())
        # Backup trạng thái ban đầu cho undo_line
        self.state_manager.backup_ui_state_for_line(self.current_line_idx, self.current_step)
        if hasattr(bits, "backup_line_state"):
            bits.backup_line_state()


            
    def handle_open_file(self):
        """
        Hiển thị hộp thoại mở file, đọc nội dung và hiển thị vào codeEditor.
        Cập nhật thanh trạng thái với tên file.
        """
        global current_file_path
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self,  # Sử dụng self làm parent
            "Chọn file LEGv8 (.txt, .s, .asm)",
            os.getcwd(),
            "LEGv8 Files (*.txt *.s *.asm);;All Files (*)",
            options=options
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.ui.codeEditor.setPlainText(content)
                current_file_path = file_path
                self.setWindowTitle(f"LEGv8 Simulator - {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi mở file", str(e))

            simulate.clear_animated_squares(self.ax)
            self.handle_clean()

    def handle_close_file(self):
        """
        Đóng file hiện tại: xóa nội dung codeEditor và thiết lập lại tiêu đề.
        """
        global current_file_path
        if current_file_path is None:
            QMessageBox.information(self, "Thông báo", "Chưa có file nào được mở.")
            return
        reply = QMessageBox.question(
            self,
            "Xác nhận",
            f"Bạn có muốn đóng file {os.path.basename(current_file_path)} không?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.ui.codeEditor.clear()
            current_file_path = None
            self.setWindowTitle("LEGv8 Simulator")
            self.handle_clean()

    def handle_save_file(self):
        """
        Hiển thị hộp thoại lưu file, lưu nội dung codeEditor vào file.
        Nếu chưa có file nào được mở, sử dụng Save As.
        """
        global current_file_path
        if current_file_path is None:
            options = QFileDialog.Options()
            options |= QFileDialog.ShowDirsOnly
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Lưu file LEGv8",
                os.getcwd(),
                "LEGv8 Files (*.txt *.s *.asm);;All Files (*)",
                options=options
            )
            if not file_path:
                return
            current_file_path = file_path

        try:
            with open(current_file_path, 'w', encoding='utf-8') as f:
                f.write(self.ui.codeEditor.toPlainText())
            QMessageBox.information(self, "Thông báo", "Đã lưu thành công.")
            self.setWindowTitle(f"LEGv8 Simulator - {os.path.basename(current_file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi lưu file", str(e))


    def closeEvent(self, event):
        """Override closeEvent để dọn dẹp properly"""
        # Dọn dẹp state manager backups để tránh truy cập vào deleted objects
        if hasattr(self, 'state_manager'):
            self.state_manager.step_backup.clear()
            self.state_manager.line_backup.clear()
        
        # Dừng animations nếu có
        if hasattr(self, 'ani') and self.ani:
            self.ani.event_source.stop()
        
        # Chấp nhận close event
        event.accept()

    def save_old_register_value(self, row, col):
        item = self.ui.registerShow.item(row, col)
        self._old_register_value = item.text() if item else "0"
    
    def handle_register_item_changed(self, item):
        row = item.row()
        col = item.column()
        if col == 0 and row != 31:
            try:
                val = int(item.text())
                if not (-9223372036854775808 <= val <= 9223372036854775807):
                    raise ValueError
            except Exception:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Chỉ cho phép nhập số nguyên có dấu 64 bit (-9223372036854775808 đến 9223372036854775807).")
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
            word_row = row - (row % 8)
            word = 0
            for i in range(8):
                byte_item = self.ui.ramTable.item(word_row + i, 1)
                byte_str = byte_item.text() if byte_item else "00000000"
                if len(byte_str) == 8 and all(c in '01' for c in byte_str):
                    byte_val = int(byte_str, 2)
                else:
                    byte_val = 0
                word |= (byte_val << (8 * (7 - i)))
            # Xử lý số âm (signed 64-bit)
            if word & 0x8000000000000000:
                word = word - 0x10000000000000000
            word_item = self.ui.ramTable.item(word_row, 3)
            if word_item:
                word_item.setText(str(word))
        # WordValue (cột 3): chỉ cho phép nhập số nguyên có dấu 64 bit
        elif col == 3:
            val = item.text()
            try:
                num = int(val)
                if not (-9223372036854775808 <= num <= 9223372036854775807):
                    raise ValueError
            except Exception:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "DoubleWordValue chỉ cho phép nhập số nguyên có dấu từ -9223372036854775808 đến 9223372036854775807.")
                item.setText(self._old_ram_value)
                return
            num_unsigned = num & 0xFFFFFFFFFFFFFFFF
            for i in range(8):
                byte_val = (num_unsigned >> (8 * (7 - i))) & 0xFF
                byte_str = format(byte_val, '08b')
                byte_item = self.ui.ramTable.item(row + i, 1)
                if byte_item:
                    byte_item.setText(byte_str)

    def run_all(self):
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
        max_loops = 1000
        while self.current_line_idx < total_lines:
            if loop_count >= max_loops:
                QtWidgets.QMessageBox.critical(self, "Lỗi", "Chương trình vượt quá 1000 vòng lặp! Có thể bị lặp vô hạn.")
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

    def handle_animate_button(self):
        """
        Nếu đang chạy animation thì dừng lại, nếu không thì bắt đầu chạy animation toàn bộ.
        """
        if hasattr(self, 'animation_running') and self.animation_running:
            # Đang chạy animation, dừng lại
            self.animation_running = False
            if self.ani:
                self.ani.event_source.stop()
                self.ani = None
            self.ui.animate_button.setText("Animate")
            self.ui.animate_button.setStyleSheet("")  # Reset style nếu muốn
        else:
            # Bắt đầu chạy animation toàn bộ
            self.animation_running = True
            self.ui.animate_button.setText("Pause")
            self.ui.animate_button.setStyleSheet("background-color: #f44336")
            self.run_all_with_simulate()

    def update_animation_speed(self, value):
        """Cập nhật tốc độ animation khi thanh trượt thay đổi"""
        import simulate_animation  # Import ở đây để tránh import vòng
        simulate_animation.set_animation_speed(value)

    def run_all_with_simulate(self):
        """
        Chạy toàn bộ chương trình từng bước với hiệu ứng animate (dùng run_by_step_with_simulate).
        """

        total_lines = self.ui.codeEditor.document().blockCount()
        # Reset về đầu nếu đang ở cuối
        if not hasattr(self, 'current_step'):
            self.current_step = 0
        if not hasattr(self, 'current_line_idx'):
            self.current_line_idx = 0

        def step_and_continue():
            if not getattr(self, 'animation_running', False):
                return
            if self.current_line_idx >= total_lines:
                QtWidgets.QMessageBox.information(self, "Kết thúc", "Đã chạy hết chương trình!")
                self.current_line_idx = 0
                self.highlight_line(self.current_line_idx)
                bits.reset_data()
                self.animation_running = False
                self.ui.animate_button.setText("Animate")
                self.ui.animate_button.setStyleSheet("")
                return
            step_and_continue.started = True
            # Chạy một bước, truyền callback để gọi tiếp khi animation xong
            self.run_by_step_with_simulate(on_finished=step_and_continue)

        step_and_continue()

    def update_flags(self):
        """Cập nhật cờ NZCV trên giao diện dựa vào trạng thái hiện tại"""
        nzcv = bits.data['Flags']['NZCV']  # Lấy giá trị cờ từ bits.data
        n, z, c, v = int(nzcv[0]), int(nzcv[1]), int(nzcv[2]), int(nzcv[3])

        def highlight_flag(label, bit):
            """Cập nhật màu sắc cho cờ"""
            if bit == 1:
                label.setStyleSheet(label.styleSheet() + "background-color: lightgreen;")
            else:
                label.setStyleSheet(label.styleSheet().replace("background-color: lightgreen;", ""))

        # Cập nhật màu sắc cho từng cờ
        highlight_flag(self.ui.n_flag, n)
        highlight_flag(self.ui.z_flag, z)
        highlight_flag(self.ui.c_flag, c)
        highlight_flag(self.ui.v_flag, v)

    def handle_last_step(self):
        """Xử lý nút Last Step - quay lại bước trước đó"""
        # Kiểm tra có thể undo step không
        if not self.state_manager.can_undo_step() or not bits.can_undo_step():
            QtWidgets.QMessageBox.information(self, "Thông báo", "Không có bước nào để quay lại!")
            return

        # Khôi phục trạng thái bits
        if bits.restore_last_step():
            # Khôi phục trạng thái UI
            result = self.state_manager.restore_ui_state_from_step()
            if result:
                self.current_line_idx, self.current_step = result
                self.highlight_line(self.current_line_idx)

                # Xóa các hình vuông liên quan đến block trước đó
                order = [
                    'PC', 'P1', 'IM', 'P2', 'Control',
                    'P3', 'M1', 'Reg', 'P5',  
                    'P4', 'ALUControl', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem', 
                    'M3', 'Flags', 'AND1', 'AND2', 'OR',
                    'SL2', 'P8', 'ADD1', 'ADD2', 'M4'
                ]

                prev_block = 'PC'
                if self.current_step > 0:
                    print(self.current_step)
                    prev_block = order[self.current_step]

                paths_to_remove = simulate.line_next[prev_block]
                simulate.clear_animated_squares_from(self.ax, paths_to_remove)

                self.update_flags()

                # Xóa highlight đường xanh nếu có
                if hasattr(self, 'highlighted_lines'):
                    simulate.clear_highlighted_lines(self.highlighted_lines)
                if self.current_step < len(order):
                    next_block = order[self.current_step]
                else:
                    next_block = order[0]

                self.highlighted_lines = simulate.highlight_next_lines(
                    self.ax, next_block, simulate.line_next, simulate.lines
                )
                self.canvas.draw_idle()

    def handle_last_line(self):
        """Xử lý nút Last Line - quay lại dòng lệnh trước đó"""
        if not self.state_manager.can_undo_line() or not bits.can_undo_line():
            QtWidgets.QMessageBox.information(self, "Thông báo", "Không có dòng nào để quay lại!")
            return
        
        # Khôi phục trạng thái bits
        if bits.restore_last_line():
            # Khôi phục trạng thái UI
            result = self.state_manager.restore_ui_state_from_line()
            if result:
                self.current_line_idx, self.current_step = result
                self.highlight_line(self.current_line_idx)
                
                # Xóa backup của run_by_step trước đó
                self.state_manager.step_backup.clear()

                # Xóa animation hiện tại
                simulate.clear_animated_squares(self.ax)
                
                # Xóa highlight đường xanh nếu có
                if hasattr(self, 'highlighted_lines'):
                    simulate.clear_highlighted_lines(self.highlighted_lines)
                
                # Highlight các line tiếp theo từ PC
                self.highlighted_lines = simulate.highlight_next_lines(
                    self.ax, 'PC', simulate.line_next, simulate.lines
                )

                self.update_flags()

                
                self.canvas.draw_idle()

    def run_by_step_with_simulate(self, on_finished=None):
        """
        Chạy từng bước mô phỏng với hiệu ứng animate, cập nhật giao diện và trạng thái.
        """
        # Backup trạng thái trước khi thực hiện bước
        bits.backup_step_state()
        self.state_manager.backup_ui_state_for_step(self.current_line_idx, self.current_step)

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

        # Nếu đã hết order thì quay lại đầu, cập nhật dòng lệnh tiếp theo
        if self.current_step >= len(order):
            simulate.clear_animated_squares(self.ax)  # Xóa các khối vuông khi chạy hết 1 vòng
            self.current_step = 0
            self.current_line_idx = int(bits.data['PC']['Inp0']) // 4
            self.state_manager.step_backup.clear()
            # Backup trạng thái cho undo_line khi kết thúc một dòng lệnh
            self.state_manager.backup_ui_state_for_line(self.current_line_idx, self.current_step)
            if hasattr(bits, "backup_line_state"):
                bits.backup_line_state()


        # Kiểm tra nếu không còn lệnh để thực thi
        if bits.data['P2']['Inp0'] == 'Khong co lenh':
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không có lệnh tại địa chỉ này!\nDừng mô phỏng.")
            self.current_step = 0
            self.current_line_idx = 0
            bits.reset_data()
            self.highlight_line(self.current_line_idx)
            self.canvas.draw_idle()
            return

        # Nếu đã chạy hết các dòng code
        if self.current_line_idx >= total_lines:
            QtWidgets.QMessageBox.information(self, "Kết thúc", "Đã chạy hết chương trình!")
            self.current_line_idx = 0
            self.highlight_line(self.current_line_idx)
            bits.reset_data()
            simulate.clear_animated_squares(self.ax)
            self.canvas.draw_idle()
            return

        # Highlight dòng code hiện tại
        self.highlight_line(self.current_line_idx)

        block = order[self.current_step]

        # Xóa highlight cũ trên sơ đồ
        if hasattr(self, 'highlighted_lines'):
            simulate.clear_highlighted_lines(self.highlighted_lines)

        # Highlight các line tiếp theo trên sơ đồ (nếu không phải bước cuối)
        if self.current_step + 1 < len(order):
            next_block = order[self.current_step + 1]
        else:
            next_block = order[0]
        self.highlighted_lines = simulate.highlight_next_lines(
            self.ax, next_block, simulate.line_next, simulate.lines
        )

        # Nếu đang có animation cũ thì dừng lại
        if self.ani:
            self.ani.event_source.stop()

        # Animate block/line hiện tại
        self.ani = simulate.run_by_step_with_animate(
            self.ax, block, simulate.lines, simulate.line_next, self.ui,
            interval=0.1, on_finished=on_finished
        )

        # Nếu là bước ghi thanh ghi (M3) và RegWrite bật, cập nhật giá trị thanh ghi trên giao diện
        if block == 'M3' and int(bits.data['Reg']['RegWrite'], 2) == 1:
            rd = bits.data['Reg']['WriteRegister']
            rd_value = bits.data['Reg']['WriteData']
            if int(rd, 2) != 31:  # XZR (X31) luôn bằng 0, không cần cập nhật
                self.ui.registerShow.setItem(int(rd, 2), 0, QtWidgets.QTableWidgetItem(str(int(rd_value))))

        # Vẽ lại canvas
        self.canvas.draw_idle()

        # Tăng bước cho lần chạy tiếp theo
        self.current_step += 1


    def handle_run_by_step_click(self):
        """Xử lý khi người dùng nhấn nút Run by Step"""
        if hasattr(self, 'animation_running') and self.animation_running:
            # Nếu đang chạy animation, chỉ chạy một bước rồi tiếp tục animation
            self.run_by_step_with_simulate(on_finished=self.run_all_with_simulate)
        else:
            # Chạy một bước bình thường
            self.run_by_step_with_simulate()



    def run_by_line(self):
        order = [
            'PC', 'P1', 'IM', 'P2', 'Control',
            'P3', 'M1', 'Reg', 'P5',  
            'P4', 'ALUControl', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem', 
            'M3', 'Flags', 'AND1', 'AND2', 'OR',
            'SL2', 'P8', 'ADD1', 'ADD2', 'M4'
        ]
        total_lines = self.ui.codeEditor.document().blockCount()

        bits.backup_line_state()
        self.state_manager.backup_ui_state_for_line(
            self.current_line_idx, self.current_step
        )

        if self.current_line_idx >= total_lines:
            simulate.clear_animated_squares(self.ax)
            QtWidgets.QMessageBox.information(self, "Kết thúc", "Đã chạy hết chương trình!")
            self.current_line_idx = 0
            self.highlight_line(self.current_line_idx)
            bits.reset_data()
            return
        
        simulate.clear_animated_squares(self.ax)
        self.canvas.draw_idle()

        while self.current_step < len(order):
            block = order[self.current_step]
            simulate.logic_step_from_block(block, simulate.lines, simulate.line_next, self.ui)
            if block == 'M3' and int(bits.data['Reg']['RegWrite'],2) == 1:
                rd= bits.data['Reg']['WriteRegister']
                rd_value = bits.data['Reg']['WriteData']
                if int(rd, 2) != 31:
                    self.ui.registerShow.setItem(int(rd,2), 0, QtWidgets.QTableWidgetItem(str(int(rd_value))))
            self.current_step += 1
        self.current_step = 0
        self.current_line_idx = int(bits.data['PC']['Inp0'])//4
        self.highlight_line(self.current_line_idx)

        # Xóa highlight đường xanh nếu có
        if hasattr(self, 'highlighted_lines'):
            simulate.clear_highlighted_lines(self.highlighted_lines)
            del self.highlighted_lines
            # Highlight các line tiếp theo từ PC
            self.highlighted_lines = simulate.highlight_next_lines(
                self.ax, 'PC', simulate.line_next, simulate.lines
            )
        
        self.state_manager.step_backup.clear()

        if self.ui.animate_button.isChecked():
            self.run_all_with_simulate()

    def run_to_checkpoint(self):
        order = [
            'PC', 'P1', 'IM', 'P2', 'Control',
            'P3', 'M1', 'Reg', 'P5',  
            'P4', 'ALUControl', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem', 
            'M3', 'Flags', 'AND1', 'AND2', 'OR',
            'SL2', 'P8', 'ADD1', 'ADD2', 'M4'
        ]
        total_lines = self.ui.codeEditor.document().blockCount()

        if self.current_line_idx >= total_lines:
            simulate.clear_animated_squares(self.ax)
            QtWidgets.QMessageBox.information(self, "Kết thúc", "Đã chạy hết chương trình!")
            self.current_line_idx = 0
            self.highlight_line(self.current_line_idx)
            bits.reset_data()
            return

        simulate.clear_animated_squares(self.ax)
        self.canvas.draw_idle()
        while self.current_line_idx < total_lines and ((not self.ui.codeEditor.is_breakpoint(self.current_line_idx)) or self.check_in_checkpoint==0):
            
            self.check_in_checkpoint += 1

            while self.current_step < len(order):
                block = order[self.current_step]
                simulate.logic_step_from_block(block, simulate.lines, simulate.line_next, self.ui)
                if block == 'M3' and int(bits.data['Reg']['RegWrite'],2) == 1:
                    rd= bits.data['Reg']['WriteRegister']
                    rd_value = bits.data['Reg']['WriteData']
                    if int(rd, 2) != 31:
                        self.ui.registerShow.setItem(int(rd,2), 0, QtWidgets.QTableWidgetItem(str(int(rd_value))))
                self.current_step += 1
            self.current_step = 0
            self.current_line_idx = int(bits.data['PC']['Inp0'])//4
            self.highlight_line(self.current_line_idx)

            bits.backup_line_state()
            self.state_manager.backup_ui_state_for_line(
                self.current_line_idx, self.current_step
            )

        # Xóa highlight đường xanh nếu có
        self.check_in_checkpoint = 0
        if hasattr(self, 'highlighted_lines'):
            simulate.clear_highlighted_lines(self.highlighted_lines)
            del self.highlighted_lines
        if self.ui.animate_button.isChecked():
            self.run_all_with_simulate()

        self.state_manager.step_backup.clear()


    def handle_clean(self):
        
        # Xóa backup history
        self.state_manager.step_backup.clear()
        self.state_manager.line_backup.clear()

        # Đưa giá trị thanh ghi về mặc định (0)
        for i in range(self.ui.registerShow.rowCount() - 1):
            self.ui.registerShow.setItem(i, 0, QtWidgets.QTableWidgetItem("0"))
            item = self.ui.ramTable.item(i, 1)
            item.setBackground(QColor(255, 255, 200))

        for row in range(self.ui.ramTable.rowCount()):
            word_item = QtWidgets.QTableWidgetItem("0")
            if row % 8 == 0:
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

        if hasattr(self, 'highlighted_lines'):
            simulate.clear_highlighted_lines(self.highlighted_lines)
            
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
            "- RAM 64 bit có dấu, nhập ByteValue là 8 ký tự 0/1.<br>"
            "- Thanh ghi 64 bit có dấu, nhập giá trị từ -9223372036854775808 đến 9223372036854775807. Kết quả phép tính cho phép bị tràn số.<br>"
            "- Chỉ DoubleWordValue dòng đầu mới cho phép chỉnh sửa.<br>"
            "- LDUR và STUR chỉ hỗ trợ địa chỉ chia hết cho 8 từ 0 đến 504 (tương ứng với 64 dòng RAM).<br>"
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