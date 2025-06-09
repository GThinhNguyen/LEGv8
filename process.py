from PyQt5.QtWidgets import QFileDialog, QMessageBox

def handle_open_file(ui):
    """
    Xử lý khi nhấn nút 'Open file':
    - Hiển thị hộp thoại chọn file
    - Đọc nội dung file
    - Hiển thị nội dung trong QTextEdit
    """
    # Hiện hộp thoại chọn file
    options = QFileDialog.Options()
    file_name, _ = QFileDialog.getOpenFileName(
        None,
        "Open Assembly File",
        "",
        "Text Files (*.txt);;All Files (*)",
        options=options
    )
    
    if file_name:
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read()
                ui.textEdit.setPlainText(content)  # Hiển thị nội dung lên giao diện
        except Exception as e:
            # Hiển thị lỗi nếu có
            QMessageBox.critical(None, "Error", f"Could not read file:\n{str(e)}")


def handle_close_file(ui):
    """
    Xử lý khi nhấn nút 'Close file':
    - Xóa nội dung đang hiển thị trong QTextEdit
    - Reset các cờ và thanh ghi nếu muốn (mở rộng sau)
    """
    confirm = QMessageBox.question(
        None,
        "Confirm Close",
        "Are you sure you want to close the current file?",
        QMessageBox.Yes | QMessageBox.No
    )
    
    if confirm == QMessageBox.Yes:
        ui.textEdit.clear()

        # Nếu bạn muốn reset các thanh ghi/cờ thì thêm như dưới:
        for row in range(32):
            ui.registerShow.setItem(row, 0, None)
        ui.n_flag.setText("N")
        ui.z_flag.setText("Z")
        ui.c_flag.setText("C")
        ui.v_flag.setText("V")

