import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox

# Biến toàn cục lưu đường dẫn file hiện tại
current_file_path = None

def handle_open_file(ui):
    """
    Hiển thị hộp thoại mở file, đọc nội dung và hiển thị vào codeEditor.
    Cập nhật thanh trạng thái với tên file.
    """
    global current_file_path
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_path, _ = QFileDialog.getOpenFileName(
        ui.centralwidget,
        "Chọn file LEGv8 (.txt, .s, .asm)",
        os.getcwd(),
        "LEGv8 Files (*.txt *.s *.asm);;All Files (*)",
        options=options
    )
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ui.codeEditor.setPlainText(content)
            current_file_path = file_path
            # Cập nhật title thông qua widget cha
            main_window = ui.centralwidget.window()
            main_window.setWindowTitle(f"LEGv8 Simulator - {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.critical(ui.centralwidget, "Lỗi mở file", str(e))

def handle_close_file(ui):
    """
    Đóng file hiện tại: xóa nội dung codeEditor và thiết lập lại tiêu đề.
    """
    global current_file_path
    if current_file_path is None:
        QMessageBox.information(ui.centralwidget, "Thông báo", "Chưa có file nào được mở.")
        return
    # Hỏi người dùng có chắc muốn đóng không
    reply = QMessageBox.question(
        ui.centralwidget,
        "Xác nhận",
        f"Bạn có muốn đóng file {os.path.basename(current_file_path)} không?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        ui.codeEditor.clear()
        current_file_path = None
        # Đặt lại tiêu đề qua widget cha
        main_window = ui.centralwidget.window()
        main_window.setWindowTitle("LEGv8 Simulator")
