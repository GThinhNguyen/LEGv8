# LEGv8 Simulator

## 🖥️ Giới thiệu

**LEGv8 Simulator** là phần mềm mô phỏng vi xử lý LEGv8 với giao diện trực quan, giúp sinh viên và người học dễ dàng:

- Quan sát RAM, thanh ghi, và các bước thực thi lệnh.
- Thực hành viết, kiểm tra, và debug mã LEGv8.
- Hiểu rõ cơ chế hoạt động của các lệnh và mô phỏng tràn số, thanh ghi đặc biệt (XZR), bộ nhớ, v.v.

## 🚀 Tính năng

- **Mô phỏng chạy từng bước**: Hiển thị trực quan từng bước thực thi lệnh bằng Run by Step.
- **Chạy toàn bộ**: Hỗ trợ Run All chạy ra kết quả cuối cùng, nếu đang chạy Run by Step thì chương trình sẽ chạy từ bước hiện tại đến hết.
- **Kiểm tra cú pháp, highlight code**: Nhận diện lệnh, thanh ghi, số, chú thích.
- **Kiểm soát nhập liệu**: Chỉ cho phép nhập giá trị 32 bit có dấu cho thanh ghi/RAM.
- **XZR (X31) luôn bằng 0**: Đúng chuẩn ARM, không thể ghi đè.
- **Chú thích code**: Hỗ trợ comment với `//`.
- **Hướng dẫn sử dụng chi tiết**: Có sẵn trong phần mềm.

## 📦 Cấu trúc thư mục

```
LEGv8/
├── main.py             # Giao diện, điều phối chương trình
├── bits.py             # Xử lý nhị phân, ALU, thanh ghi, sign extension
├── simulate.py         # Mô phỏng pipeline, animation, vẽ sơ đồ
├── mainwindow_ui.py    # Giao diện sinh ra từ Qt Designer
├── process.py          # Xử lý file (open, save, close)
├── README.md
└── ...
```

## ⚙️ Yêu cầu cài đặt

- Python >= 3.7
- PyQt5
- matplotlib
- numpy

Cài đặt nhanh:

```bash
pip install pyqt5 matplotlib numpy
```

## 📝 Hướng dẫn sử dụng

1. **Chạy chương trình:**
   Cách 1:
   Đảm bảo yêu cầu cài đặt

   ```bash
   python main.py
   ```

   Cách 2:
   Ngoài ra có thể chạy file main.exe trong thư mục dist

2. **Các chức năng chính:**

   - **Open:** Mở file mã lệnh LEGv8 (.txt, .s, .asm).
   - **Save:** Lưu file mã lệnh.
   - **Run by Step:** Chạy từng bước mô phỏng từng bước.
   - **Run All:** Chạy toàn bộ chương trình. Nếu đang chạy Run by Step thì chương trình sẽ chạy từ bước hiện tại đến hết.
   - **Clean:** Đặt lại RAM, thanh ghi, trạng thái mô phỏng.
   - **Instruction:** Xem hướng dẫn sử dụng chi tiết.

3. **Nhập code:**

   - Viết mã LEGv8 vào khung code, mỗi dòng một lệnh. Mỗi dòng code phải viết liền nhau, không được có dòng trống. Địa chỉ các dòng code bắt đầu từ 0 và cách nhau 4 byte.
   - Có thể dùng `//` để chú thích cuối dòng. Nhưng phải đảm bảo dòng nào cũng có code.

4. **Giới hạn nhập liệu:**

   - **Thanh ghi:** Chỉ nhận giá trị từ -2147483648 đến 2147483647 (32 bit có dấu).
   - **RAM:** ByteValue chỉ nhận 8 ký tự 0/1.
   - **XZR (X31):** Luôn bằng 0, không thể thay đổi.
   - **WordValue:** Chỉ dòng đầu mỗi word mới cho phép chỉnh sửa.

5. **Cú pháp lệnh cơ bản:**

   - `ADD Xd, Xn, Xm` (tương tự: SUB, AND, ORR, EOR, ADDS, SUBS, ANDS)
   - `ADDI Xd, Xn, #imm` (tương tự: SUBI, ANDI, ORRI, EORI, ADDIS, SUBIS, ANDIS)
   - `LDUR Xd, [Xn, #imm]` (tương tự: STUR)
   - `CBZ Xn, #imm`
   - `B #imm`
   - `B.EQ #imm` (tương tự các điều kiện: B.EQ, B.NE, B.MI, B.PL, B.VS, B.VC, B.GE, B.LT, B.GT, B.LE)

6. **Lưu ý:**
   - Kết quả phép tính trên ALU luôn giả lập tràn số 32 bit có dấu (two's complement).
   - LDUR/STUR chỉ hỗ trợ địa chỉ chia hết cho 4 từ 0 đến 508 (128 dòng RAM).
   - Mỗi dòng code phải viết liền nhau, không được có dòng trống.
   - Địa chỉ các dòng code bắt đầu từ 0 và cách nhau 4 byte.

## 👨‍💻 Tác giả & liên hệ

- **Giáo viên hướng dẫn:** Phạm Tuấn Sơn
- **Sinh viên thực hiện:** Nguyễn Ngọc Tin, Nguyễn Gia Thịnh

---

**Mọi thắc mắc, góp ý xin liên hệ nhóm tác giả.**
