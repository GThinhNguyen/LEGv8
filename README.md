# LEGv8 Simulator

## 🖥️ Giới thiệu

**LEGv8 Simulator** là phần mềm mô phỏng vi xử lý kiến trúc **LEGv8** (tập con của ARMv8 64-bit) với giao diện đồ họa trực quan (GUI). Phần mềm được thiết kế nhằm phục vụ học tập, nghiên cứu môn Kiến trúc Máy tính và Hợp ngữ:

- **Trực quan hóa luồng dữ liệu (Data Path)**: Mô phỏng tín hiệu điều khiển và đường đi của dữ liệu qua các khối chức năng (PC, Instruction Memory, Register File, ALU, Data Memory, Sign-Extend, MUX,...).
- **Hoạt họa (Animation)**: Hiển thị chuyển động trực quan của các gói dữ liệu theo thời gian thực với thanh chỉnh tốc độ mượt mà.
- **Quan sát trạng thái phần cứng**: Theo dõi và can thiệp trực tiếp giá trị của 32 thanh ghi (Registers), bộ nhớ dữ liệu (RAM) và các cờ điều kiện **NZCV**.
- **Hỗ trợ gỡ lỗi mạnh mẽ**: Đặt điểm dừng (Breakpoints), chạy từng dòng (Line), từng chu kỳ con (Step), hoàn tác linh hoạt (`Undo Step` / `Undo Line`), chống treo khi lặp vô hạn.

---

## 📦 Cấu trúc thư mục

```text
LEGv8/
├── .venv/                  # Môi trường ảo Python (tự tạo)
├── bits.py                 # Bộ giải mã lệnh, mô phỏng ALU, thanh ghi, RAM, cờ NZCV
├── demo.asm                # Mã nguồn hợp ngữ LEGv8 mẫu để thử nghiệm
├── main.py                 # Điều phối giao diện chính (PyQt5), xử lý sự kiện và luồng chạy
├── main.spec               # Cấu hình đóng gói PyInstaller xuất file .exe
├── mainwindow.ui           # Thiết kế giao diện Qt Designer
├── mainwindow_ui.py        # Mã nguồn giao diện sinh ra từ file .ui
├── requirements.txt        # Danh sách thư viện phụ thuộc (PyQt5, matplotlib, numpy)
├── simulate.py             # Module kết nối các thành phần mô phỏng
├── simulate_animation.py   # Xử lý hoạt họa (Animation) di chuyển trên sơ đồ Data Path
├── simulate_core.py        # Quản lý trạng thái và tính toán tọa độ đường dẫn tín hiệu
├── simulate_data.py        # Định nghĩa tọa độ các khối phần cứng và đường bus
├── simulate_highlight.py   # Highlight các thành phần và đường truyền đang kích hoạt
├── simulate_render.py      # Vẽ sơ đồ kiến trúc vi xử lý bằng Matplotlib
└── README.md               # Tài liệu hướng dẫn sử dụng
```

---

## ⚙️ Yêu cầu môi trường & Cài đặt

Khuyến nghị sử dụng **Python 3.11** (hoặc Python $\ge 3.8$ và $\le 3.12$ để tương thích tốt nhất với PyQt5).

### Bước 1: Khởi tạo môi trường ảo (Virtual Environment)

Mở terminal (PowerShell hoặc CMD) tại thư mục gốc của dự án (`d:\LEGv8`):

- **Trên Windows (dùng Python Launcher `py`):**
  ```powershell
  py -3.11 -m venv .venv
  ```
- **Hoặc dùng lệnh `python` mặc định:**
  ```powershell
  python -m venv .venv
  ```

### Bước 2: Kích hoạt môi trường ảo

- **Nếu dùng PowerShell:**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  > [!TIP]
  > Nếu gặp thông báo lỗi cấm chạy script (*running scripts is disabled on this system*), hãy cấp quyền thực thi tạm thời trong phiên làm việc hiện tại bằng lệnh:
  > ```powershell
  > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  > .\.venv\Scripts\Activate.ps1
  > ```

- **Nếu dùng Command Prompt (CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

- **Nếu dùng Git Bash / Linux / macOS:**
  ```bash
  source .venv/Scripts/activate
  ```

*(Khi kích hoạt thành công, bạn sẽ thấy tiền tố `(.venv)` xuất hiện ở đầu dòng lệnh).*

### Bước 3: Cài đặt các thư viện cần thiết

Khi môi trường ảo đã được kích hoạt, chạy lệnh sau để cài đặt toàn bộ phụ thuộc:

```powershell
pip install -r requirements.txt
```

Danh sách các thư viện bao gồm:
- `PyQt5`: Bộ công cụ giao diện người dùng GUI.
- `matplotlib`: Hiển thị sơ đồ kiến trúc vi xử lý và render đồ họa.
- `numpy`: Xử lý tính toán ma trận tọa độ hoạt ảnh.

---

## 🚀 Hướng dẫn khởi chạy chương trình

### Cách 1: Chạy khi đã kích hoạt môi trường ảo (Khuyên dùng)
```powershell
python main.py
```

### Cách 2: Chạy trực tiếp từ đường dẫn `.venv` (Không cần kích hoạt trước)
- **PowerShell:**
  ```powershell
  .\.venv\Scripts\python.exe main.py
  ```
- **Command Prompt (CMD):**
  ```cmd
  .venv\Scripts\python.exe main.py
  ```

### Cách 3: Chạy file `.exe` độc lập (Không cần cài Python)
Nếu đã được đóng gói thành công bằng PyInstaller, bạn chỉ cần nhấp đúp vào file:
```
dist\main\main.exe
```

---

## 📝 Hướng dẫn sử dụng chi tiết

### 1. Soạn thảo và Nạp mã nguồn
- **Open**: Nhấn để mở các tệp mã nguồn LEGv8 có sẵn (`.asm`, `.s`, `.txt`). Bạn có thể thử nghiệm ngay với tệp [demo.asm](demo.asm).
- **Save**: Lưu nội dung hiện tại trên trình soạn thảo ra tệp.
- **Quy tắc viết mã**:
  - Mỗi dòng là một lệnh hợp ngữ hợp lệ.
  - Các dòng mã phải viết liên tục, **không để dòng trống**.
  - Có thể thêm chú thích bằng dấu `//` ở cuối dòng (ví dụ: `ADDI X1, XZR, #5 // X1 = 5`).
  - Địa chỉ lệnh bắt đầu từ `0` và tự động tăng `4` byte cho mỗi dòng tiếp theo.

### 2. Các chế độ thực thi & Mô phỏng
- **Skip Line**: Thực thi ngay dòng lệnh hiện tại không qua hoạt họa (cho kết quả tức thì).
- **Skip Step**: Thực thi nhanh một chu kỳ/bước con trong pipeline của lệnh hiện tại (P1 $\rightarrow$ P2 $\rightarrow$ P3 $\rightarrow$ P4 $\rightarrow$ P5/Mem/WB).
- **Run by Line** (Animation): Mô phỏng toàn bộ các bước của dòng lệnh hiện tại kèm hoạt họa di chuyển của tín hiệu và dữ liệu trên sơ đồ.
- **Run by Step** (Animation): Chạy hoạt họa chi tiết từng bước nhỏ để quan sát tỉ mỉ giá trị đi qua từng linh kiện.
- **Run All**: Chạy tự động toàn bộ chương trình cho tới khi kết thúc. Đã tích hợp bộ đếm an toàn (giới hạn 1000 chu kỳ) để chống treo giao diện khi gặp vòng lặp vô hạn.

### 3. Điểm dừng (Breakpoints) & Run to Checkpoint
- **Đặt Breakpoint**: Nhấp chuột trái vào **cột hiển thị số dòng** ở khung soạn thảo bên trái. Dòng được chọn sẽ xuất hiện dấu chấm tròn màu đỏ. Nhấp lại lần nữa để hủy điểm dừng.
- **Run to Checkpoint**: Bấm nút này để chương trình tự động thực thi nhanh cho tới khi gặp điểm dừng đã đặt hoặc kết thúc mã.

### 4. Thanh tốc độ & Hoàn tác (Undo)
- **Thanh trượt Speed (1 - 10)**: Điều chỉnh tốc độ khung hình và vận tốc di chuyển của animation (Mức 1: chậm nhất để quan sát rõ; Mức 10: nhanh nhất).
- **Undo Line**: Khôi phục trạng thái vi xử lý (PC, thanh ghi, RAM, cờ NZCV, sơ đồ) về trước khi chạy dòng lệnh vừa rồi.
- **Undo Step**: Hoàn tác từng bước nhỏ vừa thực hiện.
- **Clean**: Reset toàn bộ trạng thái vi xử lý về ban đầu: đặt lại PC = 0, xóa trắng các thanh ghi, đặt lại RAM và xóa các cờ trạng thái.

### 5. Xem và Can thiệp trạng thái phần cứng
- **Bảng thanh ghi (Registers)**:
  - Hiển thị 32 thanh ghi 64-bit (`X0` đến `X30` và `XZR / X31`).
  - Thanh ghi `XZR` luôn luôn bằng 0 theo chuẩn ARM (không thể sửa đổi).
  - Bạn có thể **nhấp đúp chuột vào bất kỳ thanh ghi nào (`X0` - `X30`)** để nhập giá trị số nguyên mới trước hoặc trong khi mô phỏng.
- **Bảng bộ nhớ (RAM)**:
  - Bộ nhớ gồm 512 bytes, được nhóm thành các từ kép (DoubleWord - 64-bit / 8 byte mỗi dòng).
  - Có thể nhấp đúp để sửa trực tiếp chuỗi nhị phân 8-bit ở cột `ByteValue` hoặc giá trị số nguyên ở cột `DoubleWordValue`.
- **Cờ trạng thái NZCV**:
  - **N** (Negative): Bật khi kết quả phép tính có dấu là âm.
  - **Z** (Zero): Bật khi kết quả phép tính bằng 0.
  - **C** (Carry): Bật khi có nhớ từ bit cao nhất (phép cộng không dấu).
  - **V** (Overflow): Bật khi có tràn số bù hai (phép tính có dấu).

---

## 📖 Tập lệnh hỗ trợ

| Phân loại | Cú pháp mẫu | Mô tả |
| :--- | :--- | :--- |
| **R-format** | `ADD Xd, Xn, Xm` | Cộng giá trị 2 thanh ghi: $Xd = Xn + Xm$ |
| | `ADDS Xd, Xn, Xm` | Cộng và cập nhật cờ điều kiện NZCV |
| | `SUB Xd, Xn, Xm` | Trừ giá trị 2 thanh ghi: $Xd = Xn - Xm$ |
| | `SUBS Xd, Xn, Xm` | Trừ và cập nhật cờ điều kiện NZCV |
| | `AND / ORR / EOR` | Các phép toán logic bit (AND, OR, XOR) |
| | `ANDS Xd, Xn, Xm` | Phép AND và cập nhật cờ NZCV |
| **I-format** | `ADDI Xd, Xn, #imm` | Cộng với hằng số: $Xd = Xn + imm$ |
| | `ADDIS Xd, Xn, #imm` | Cộng với hằng số và cập nhật cờ NZCV |
| | `SUBI Xd, Xn, #imm` | Trừ đi hằng số: $Xd = Xn - imm$ |
| | `SUBIS Xd, Xn, #imm` | Trừ đi hằng số và cập nhật cờ NZCV |
| | `ANDI / ORRI / EORI` | Phép toán logic bit với hằng số |
| **D-format** | `LDUR Xt, [Xn, #imm]` | Nạp dữ liệu từ RAM tại địa chỉ $Xn + imm$ vào $Xt$ |
| | `STUR Xt, [Xn, #imm]` | Lưu giá trị từ $Xt$ vào RAM tại địa chỉ $Xn + imm$ |
| **CB-format** | `CBZ Xt, #imm` | Nhảy tương đối nếu $Xt == 0$ |
| | `CBNZ Xt, #imm` | Nhảy tương đối nếu $Xt \ne 0$ |
| **B-format** | `B #imm` | Nhảy không điều kiện tới địa chỉ tương đối $PC + imm \times 4$ |
| | `B.cond #imm` | Nhảy có điều kiện dựa trên cờ NZCV (`B.EQ`, `B.NE`, `B.LT`, `B.LE`, `B.GT`, `B.GE`, `B.MI`, `B.PL`, `B.VS`, `B.VC`) |

---

## 🛠️ Đóng gói thành file thực thi `.exe`

Nếu muốn xuất phần mềm thành file thực thi chạy độc lập trên Windows mà không cần cài đặt Python:

```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Cài đặt PyInstaller (nếu chưa có)
pip install pyinstaller

# Đóng gói theo file cấu hình có sẵn
pyinstaller main.spec
```

Sau khi đóng gói hoàn tất, file chạy sẽ nằm tại thư mục:
```
dist\main\main.exe
```

---

## 👨‍💻 Tác giả & Đóng góp

- **Giáo viên hướng dẫn:** ThS. Phạm Tuấn Sơn
- **Sinh viên thực hiện:** Nguyễn Ngọc Tin, Nguyễn Gia Thịnh
- **Cơ sở đào tạo:** Khoa Công nghệ Thông tin
