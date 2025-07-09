import mainwindow_ui
import copy

data_default = {
    'PC': {'Inp0': '0'},
    'IM': {'ReadAddress': '0'},
    'Reg': {'RegWrite': '0', 'ReadRegister1': '0', 'ReadRegister2': '0', 'WriteRegister': '0', 'WriteData': '0'},
    'Mem': {'Address': '0', 'WriteData': '0', 'MemWrite': '0', 'MemRead': '0'},
    'ALU': {'ALUControl': '0', 'ReadData1': '0', 'ReadData2': '0'},
    'ADD2': {'Inp0': '0', 'Inp1': '0'},
    'ADD1': {'Inp0': '0', 'Inp1': '4'},
    'M1': {'Control': '0', 'Inp0': '0', 'Inp1': '0'},
    'M2': {'Control': '0', 'Inp0': '0', 'Inp1': '0'},
    'M3': {'Control': '0', 'Inp0': '0', 'Inp1': '0'},
    'M4': {'Control': '0', 'Inp0': '0', 'Inp1': '0'},
    'Flags': {'Control': '0', 'NZCVtmp': '0000', 'NZCV': '0000', 'Condition': '00000'},
    'SE': {'Inp': '0'},
    'ALUControl': {'ALUop': '0', 'Ins': '0'},
    'Control': {'Inp0': '0'},
    'OR': {'Inp0': '0', 'Inp1': '0', 'Inp2': '0'},
    'AND1': {'Inp0': '0', 'Inp1': '0'},
    'AND2': {'Inp0': '0', 'Inp1': '0'},
    'SL2': {'Inp0': '0'},
    'P1': {'Inp0': '0'},
    'P2': {'Inp0': '0'},
    'P3': {'Inp0': '0'},
    'P4': {'Inp0': '0'},
    'P5': {'Inp0': '0'},
    'P6': {'Inp0': '0'},
    'P7': {'Inp0': '0'},
    'P8': {'Inp0': '0'}
}

data = copy.deepcopy(data_default)

# Hệ thống backup cho step và line
step_history = []  # Lịch sử từng bước
line_history = []  # Lịch sử từng dòng lệnh
MAX_HISTORY_SIZE = 30  # Giới hạn số lượng backup

def reset_data():
    """Reset data về trạng thái ban đầu"""
    global data, step_history, line_history
    data = copy.deepcopy(data_default)
    step_history.clear()
    line_history.clear()

def backup_step_state():
    """Lưu trạng thái hiện tại cho step history"""
    global step_history
    current_state = copy.deepcopy(data)
    step_history.append(current_state)
    
    # Giới hạn kích thước lịch sử
    if len(step_history) > MAX_HISTORY_SIZE:
        step_history.pop(0)

def backup_line_state():
    """Lưu trạng thái hiện tại cho line history"""
    global line_history
    current_state = copy.deepcopy(data)
    line_history.append(current_state)
    
    # Giới hạn kích thước lịch sử
    if len(line_history) > MAX_HISTORY_SIZE:
        line_history.pop(0)

def restore_last_step():
    """Khôi phục trạng thái bước trước đó"""
    global data, step_history
    if step_history:
        data = step_history.pop()
        return True
    return False

def restore_last_line():
    """Khôi phục trạng thái dòng lệnh trước đó"""
    global data, line_history
    if line_history:
        data = line_history.pop()
        return True
    return False

def can_undo_step():
    """Kiểm tra có thể undo step không"""
    return len(step_history) > 0

def can_undo_line():
    """Kiểm tra có thể undo line không"""
    return len(line_history) > 0

def signed_to_bin(value: int, n: int) -> str:
    min_val = - (1 << (n-1))
    max_val =   (1 << (n-1)) - 1
    if not (min_val <= value <= max_val):
        raise ValueError(f"{value} không thể biểu diễn trong {n} bit (phạm vi [{min_val}, {max_val}])")
    # Với số âm, lấy two's complement
    if value < 0:
        value = (1 << n) + value
    # Chuyển sang nhị phân, điền 0 đầu cho đủ n bit
    s = format(value, 'b').zfill(n)
    return s

def bin_to_signed(s):
    value = int(s, 2)
    bits = len(s)
    if value >= 2**(bits - 1):
        value -= 2**bits
    return value

def parse_signed(val):
    if isinstance(val, str) and set(val) <= {'0', '1'} and len(val) == 64:
        return bin_to_signed(val)
    try:
        return int(val)
    except Exception:
        return 0

def get_register_value(idx, ui):
    if idx == 31:
        return 0
    item = ui.registerShow.item(idx, 0)
    try:
        return int(item.text()) if item and item.text() not in ("", None) else 0
    except Exception:
        return 0
    
def parse_reg(p: str) -> int:
    """
    Chuyển tên thanh ghi thành số:
    - 'Xn' -> n
    - 'Wn' -> n (lower 64-bit)
    - 'XZR', 'WZR', 'SP', 'WSP' -> 31
    - 'FP' -> 29 (frame pointer)
    - 'LR' -> 30 (link register)
    """
    p = p.upper()
    # Special aliases
    special = {
        'XZR': 31, 'SP': 28, 
        'FP': 29,  'LR': 30
    }
    if p in special:
        return special[p]
    # General Xn or Wn
    if (p.startswith('X') or p.startswith('W')) and p[1:].isdigit():
        return int(p[1:])
    raise ValueError(f"Invalid register: {p}")

def assemble_instruction(inst_str):
    parts = inst_str.replace(',', ' ').replace('[', ' ').replace(']', ' ').split()
    op = parts[0].upper()

    if op in ('ADD', 'SUB', 'AND', 'ORR', 'ADDS', 'SUBS', 'ANDS', 'EOR'):
        rd, rn, rm = map(parse_reg, parts[1:4])
        opcodes = {
            'ADD': 0b10001011000,
            'SUB': 0b11001011000,
            'AND': 0b10001010000,
            'ORR': 0b10101010000,
            'EOR': 0b11001010000,
            'ADDS':0b10101011000,
            'SUBS':0b11101011000,
            'ANDS':0b11101010000,
        }
        opcode = opcodes[op]
        shamt = 0
        instr = (opcode << 21) | (rm << 16) | (shamt << 10) | (rn << 5) | rd
    elif op == 'LDUR':
        # cú pháp: LDUR Xd, [Xn, #imm]
        rt = parse_reg(parts[1])
        rn = parse_reg(parts[2])
        imm = int(parts[3].lstrip('#'))
        opcode = 0b11111000010
        instr = (opcode << 21) | ((imm & 0x1FF) << 12) | (rn << 5) | rt
    elif op == 'STUR':
        rt = parse_reg(parts[1])
        rn = parse_reg(parts[2])
        imm = int(parts[3].lstrip('#'))
        opcode = 0b11111000000
        instr = (opcode << 21) | ((imm & 0x1FF) << 12) | (rn << 5) | rt
    elif op == 'CBZ':
        rt = parse_reg(parts[1])
        imm = int(parts[2].lstrip('#'))
        opcode = 0b10110100
        instr = (opcode << 24) | ((imm & 0x7FFFF) << 5) | rt
    elif op == 'B':
        imm = int(parts[1].lstrip('#'))
        opcode = 0b000101
        instr = (opcode << 26) | (imm & 0x3FFFFFF)
    elif op == 'ADDI':
        rd = parse_reg(parts[1])    
        rn = parse_reg(parts[2])  
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1001000100
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'SUBI':
        rd = parse_reg(parts[1])    
        rn = parse_reg(parts[2])  
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1101000100
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'ANDI':
        rd = parse_reg(parts[1])    
        rn = parse_reg(parts[2])  
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1001001000
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'ORRI':
        rd = parse_reg(parts[1])    
        rn = parse_reg(parts[2])  
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1011001000
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'EORI':
        rd = parse_reg(parts[1])    
        rn = parse_reg(parts[2])  
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1101001000
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'ADDIS':
        rd = parse_reg(parts[1])    
        rn = parse_reg(parts[2])  
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1011000100
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'ANDIS':
        rd = parse_reg(parts[1])    
        rn = parse_reg(parts[2])  
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1111001000
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'SUBIS':
        rd = parse_reg(parts[1])    
        rn = parse_reg(parts[2])  
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1111000100
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op.startswith('B.'):
        cond_map = {
            'B.EQ':  0b0000,
            'B.NE':  0b0001,
            'B.MI':  0b0100,
            'B.PL':  0b0101,
            'B.VS':  0b0110,
            'B.VC':  0b0111,
            'B.GE':  0b1010,
            'B.LT':  0b1011,
            'B.GT':  0b1100,
            'B.LE':  0b1101,
        }
        imm = int(parts[1].lstrip('#'))
        opcode = 0b01010100  # B.cond opcode
        cond = cond_map.get(op)
        if cond is None:
            raise ValueError(f"Unsupported conditional branch: {op}")
        instr = (opcode << 24) | ((imm & 0x7FFFF) << 5) | cond
    else:
        raise ValueError(f"assemble_instruction(): lệnh không hỗ trợ: {inst_str}")

    return format(instr, '032b'),

def remove_double_slash_comment(line):
    # Loại bỏ phần comment bắt đầu từ //
    return line.split('//')[0].rstrip()

def get_bits_for_path(block, ui = None):
    # Trả về giá trị hoặc hàm trả giá trị dạng tuple
    if block in ['M1', 'M2', 'M3', 'M4']:
        if data[block]['Control'] == '0':
            return (data[block]['Inp0'],)
        else:
            return (data[block]['Inp1'],)
    if block in ['P1', 'P5', 'P6', 'P7', 'P8']:
        return (data[block]['Inp0'], data[block]['Inp0'])
    if block == 'P3':
        return (data[block]['Inp0'], data[block]['Inp0'], data[block]['Inp0'])  
    if block == 'P4':
        instr = data['P4']['Inp0']
        instr_binary = assemble_instruction(instr)
        opcode = instr_binary[0][0:11]
        return (instr, opcode)
    if block == 'P2':
        #  Trả về tuple các trường opcode, Rn, Rm, Rd, full instruction từ chuỗi nhị phân 32 bit
        instr = data['P2']['Inp0']
        instr_binary = assemble_instruction(instr)
        opcode = instr_binary[0][0:11]
        rm     = instr_binary[0][11:16]
        rn     = instr_binary[0][22:27]
        rd     = instr_binary[0][27:32]
        return (opcode, rn, rm, rd, instr)
        
    if block in ['ADD2', 'ADD1']:
        return (int(data[block]['Inp0']) + int(data[block]['Inp1']),)
    if block == 'OR':
        return (format(int(data['OR']['Inp0'],2) | int(data['OR']['Inp1'],2) | int(data['OR']['Inp2'],2), 'b'),)
    if block in ['AND1', 'AND2']:
        return (format(int(data[block]['Inp0'],2) & int(data[block]['Inp1'],2), 'b'),)
    if block == 'Control':
        # tra ve mang Reg2Loc UncondBranch FlagBranch ZeroBranch memRead memtoReg MemWrite FlagWrite ALUSrc ALUOp   RegWrite
        inp = data['Control']['Inp0']
        controls = {
            '10001011000': '0,0,0,0,0,0,0,0,0,10,1',  # ADD
            '11001011000': '0,0,0,0,0,0,0,0,0,10,1',  # SUB
            '10001010000': '0,0,0,0,0,0,0,0,0,10,1',  # AND
            '10101010000': '0,0,0,0,0,0,0,0,0,10,1',  # ORR
            '11001010000': '0,0,0,0,0,0,0,0,0,10,1',  # EOR
            '10101011000': '0,0,0,0,0,0,0,1,0,10,1',  # ADDS
            '11101011000': '0,0,0,0,0,0,0,1,0,10,1',  # SUBS
            '11101010000': '0,0,0,0,0,0,0,1,0,10,1',  # ANDS
            '11111000010': '0,0,0,0,1,1,0,0,1,00,1',  # LDUR
            '11111000000': '1,0,0,0,0,0,1,0,1,00,0',  # STUR
        }
        if inp in controls:
            return tuple(controls[inp].split(','))
        if inp[0:8] == '10110100':  # CBZ
            return ('1', '0', '0', '1', '0', '0', '0', '0', '0', '01', '0')
        if inp[0:8] == '01010100':  # B.cond
            return ('0', '0', '1', '0', '0', '0', '0', '0', '0', '01', '0')
        if inp[0:6] == '000101':  # B
            return ('0', '1', '0', '0', '0', '0', '0', '0', '0', '00', '0')
        if inp[0:10] == '1001000100':  # ADDI
            return ('0', '0', '0', '0', '0', '0', '0', '0', '1', '10', '1')
        if inp[0:10] == '1101000100':  # SUBI
            return ('0', '0', '0', '0', '0', '0', '0', '0', '1', '10', '1')
        if inp[0:10] == '1001001000':  # ANDI
            return ('0', '0', '0', '0', '0', '0', '0', '0', '1', '10', '1')
        if inp[0:10] == '1011001000':  # ORRI
            return ('0', '0', '0', '0', '0', '0', '0', '0', '1', '10', '1')
        if inp[0:10] == '1101001000':  # EORI
            return ('0', '0', '0', '0', '0', '0', '0', '0', '1', '10', '1')
        if inp[0:10] == '1011000100':  # ADDIS
            return ('0', '0', '0', '0', '0', '0', '0', '1', '1', '10', '1')
        if inp[0:10] == '1111000100':  # SUBIS
            return ('0', '0', '0', '0', '0', '0', '0', '1', '1', '10', '1')
        if inp[0:10] == '1111001000':  # ANDIS
            return ('0', '0', '0', '0', '0', '0', '0', '1', '1', '10', '1')
        raise KeyError(f"Unrecognized opcode: {inp}")
    if block == 'SE':
        instr = data['SE']['Inp']  
        instr_binary = assemble_instruction(instr)
        opcode1 = instr_binary[0][0:11]     
        opcode2= instr_binary[0][0:8]   
        opcode3 = instr_binary[0][0:6]     
        opcode4 = instr_binary[0][0:10]  
        # Xác định vị trí và độ dài immediate
        if opcode1 in ('11111000010', '11111000000'):    # LDUR, STUR (D-type)
            # immediate bits [20:12] => indices [11:20) trong Python
            imm = instr_binary[0][11:20]
        elif opcode2 in ('10110100', '01010100'):  # CBZ (CB-type), B.cond (CB-type)
            imm = instr_binary[0][8:27]
        elif opcode3 == '000101':     # B (B-type)
            imm = instr_binary[0][6:32]
        elif opcode4 in ('1001000100', '1101000100', '1001001000', '1011001000', '1011000100', '1111000100', '1111001000', '1101001000'):  # ADDI, SUBI, ANDI, ORRI, ADDIS, SUBIS, ANDIS, EORI (I-type)
            imm = instr_binary[0][10:22]
        else:
            # Không phải lệnh có immediate
            return ('0',)

        # sign-extend lên 64 bit
        sign_bit = imm[0]
        extended = sign_bit * (64 - len(imm)) + imm
        # Trả về giá trị đã sign-extend
        kq = bin_to_signed(extended)

        return (kq,)
    if block == 'ALUControl':
        aluop = data['ALUControl']['ALUop']
        ins   = data['ALUControl']['Ins']
        if aluop == '10':
            table = {
                '10001011000': '0010', # ADD
                '10101011000': '0010', # ADDS
                '11001011000': '0110', # SUB
                '11101011000': '0110', # SUBS
                '10001010000': '0000', # AND
                '11101010000': '0000', # ANDS
                '10101010000': '0001', # ORR
                '11001010000': '0011', # EOR
            }
            table2 = {
                '1001000100': '0010',  # ADDI
                '1011000100': '0010',  # ADDIS
                '1101000100': '0110',  # SUBI
                '1111000100': '0110',  # SUBIS
                '1001001000': '0000',  # ANDI
                '1111001000': '0000',  # ANDIS
                '1011001000': '0001',  # ORRI
                '1101001000': '0011',  # EORI
            }
            if ins in table:
                return (table[ins],)
            if ins[0:10] in table2:
                return (table2[ins[0:10]],)
        if aluop == '00': return ('0010',)
        if aluop == '01': return ('0111',)
        return ('0000',)
    if block == 'PC':
        return (data['PC']['Inp0'],)
    if block == 'IM':
        addr = int(data['IM']['ReadAddress'])
        idx = addr // 4
        lines = ui.codeEditor.toPlainText().splitlines() 

        if 0 <= idx < len(lines):
            return (remove_double_slash_comment(lines[idx].strip()),)
        return ("Khong co lenh",)
    if block == 'Reg':
        def reg_out():
            r1 = int(data['Reg']['ReadRegister1'], 2)
            r2 = int(data['Reg']['ReadRegister2'], 2)
            return (get_register_value(r1, ui), format(get_register_value(r2, ui)))
        return reg_out()
    
    if block == 'Mem':
        addr = int(data['Mem']['Address'], 10)
        if addr < 0 or addr >= ui.ramTable.rowCount() or addr % 8 != 0:
            return ('0',)
        if data['Mem']['MemRead'] == '1':
            item = ui.ramTable.item(addr, 3)
            try:
                val = int(item.text()) if item and item.text() not in ("", None) else 0
            except Exception:
                val = 0
            return (val,)

        if data['Mem']['MemWrite'] == '1':
            write_data = int(data['Mem']['WriteData'], 10)
            ui.ramTable.setItem(addr, 3, mainwindow_ui.QTableWidgetItem(str(write_data)))
            return ('0',)
        return ('0',)

    if block == 'ALU':
        a = parse_signed(data['ALU']['ReadData1'])   # signed 64-bit
        b = parse_signed(data['ALU']['ReadData2'])   # signed 64-bit
        op = data['ALU']['ALUControl']

        MASK_64 = 0xFFFFFFFFFFFFFFFF
        MAX_UINT = MASK_64
        MAX_INT =  0x7FFFFFFFFFFFFFFF
        MIN_INT = -0x8000000000000000

        # Chuyển sang unsigned 64-bit:
        def to_u64(x):
            return x & MASK_64

        # Chuyển kết quả 64-bit sang signed:
        def to_s64(x):
            x = x & MASK_64
            return x if x <= MAX_INT else x - (1 << 64)

        a_u = to_u64(a)
        b_u = to_u64(b)

        raw = 0
        if op == '0010':         # ADD
            raw = a_u + b_u
        elif op == '0110':       # SUB = a - b
            # thực chất: a + (2^64 - b)
            raw = (a_u - b_u) & MASK_64
        elif op == '0111':       # MOV (res = b)
            raw = b_u
        elif op == '0000':       # AND
            raw = a_u & b_u
        elif op == '0001':       # ORR
            raw = a_u | b_u
        elif op == '0011':       # EOR
            raw = a_u ^ b_u
        else:
            raw = 0

        # Kết quả thực tế (signed 64-bit):
        res = to_s64(raw)

        # Z flag: 1 nếu res == 0
        zeroFlag = 1 if res == 0 else 0
        # N flag: 1 nếu res âm
        nFlag    = 1 if res < 0 else 0

        # C flag:
        # - Với ADD: carry nếu raw > MAX_UINT
        # - Với SUB: borrow nếu a_u < b_u, nhưng ARM/NZCV định nghĩa C=1 khi KHÔNG borrow => C = 1 nếu a_u >= b_u
        # - Các op khác để 0
        if op == '0010':           # ADD
            cFlag = 1 if (a_u + b_u) > MAX_UINT else 0
        elif op == '0110':         # SUB
            cFlag = 1 if a_u >= b_u else 0
        else:
            cFlag = 0

        # V flag (signed overflow):
        # - Với ADD: 1 nếu a và b cùng dấu, nhưng res khác dấu
        # - Với SUB: 1 nếu a và b khác dấu, và res khác dấu của a
        if op == '0010':  # ADD
            if (a >= 0 and b >= 0 and res < 0) or (a < 0 and b < 0 and res >= 0):
                vFlag = 1
            else:
                vFlag = 0
        elif op == '0110':  # SUB
            if (a >= 0 and b < 0 and res < 0) or (a < 0 and b >= 0 and res >= 0):
                vFlag = 1
            else:
                vFlag = 0
        else:
            vFlag = 0

        Flag = f"{nFlag}{zeroFlag}{cFlag}{vFlag}"
        return (zeroFlag, res, Flag)

    if block == 'Flags':
        control = data['Flags']['Control']
        if control == '1':
            data['Flags']['NZCV'] = data['Flags']['NZCVtmp']
        
        nzcv = data['Flags']['NZCV']  # string 4 ký tự
        n, z, c, v = nzcv[0], nzcv[1], nzcv[2], nzcv[3]
        n, z, c, v = int(n), int(z), int(c), int(v) 
        def highlight_flag(label, bit):
            if bit == 1:
                label.setStyleSheet(label.styleSheet() + "background-color: lightgreen;")
            else:
                label.setStyleSheet(label.styleSheet().replace("background-color: lightgreen;", ""))

        highlight_flag(ui.n_flag, n)
        highlight_flag(ui.z_flag, z)
        highlight_flag(ui.c_flag, c)
        highlight_flag(ui.v_flag, v)
        cond_code = data['Flags']['Condition']  # string 5 bit, e.g. "01011"
        # Chúng ta chỉ cần 4 bit thấp:
        cond = int(cond_code[-4:], 2)

        # Mapping cond → hàm kiểm tra
        def cond_met(cond):
            return {
                0b0000: lambda: z,                  # EQ: Z == 1
                0b0001: lambda: not z,              # NE: Z == 0
                0b0100: lambda: n,                  # MI: N == 1
                0b0101: lambda: not n,              # PL: N == 0
                0b0110: lambda: v,                  # VS: V == 1
                0b0111: lambda: not v,              # VC: V == 0
                0b1010: lambda: n == v,             # GE: N == V
                0b1011: lambda: n != v,             # LT: N != V
                0b1100: lambda: not z and (n == v), # GT: Z == 0 & N == V
                0b1101: lambda: z or (n != v),      # LE: Z == 1 or N != V
            }.get(cond, lambda: False)()

        # Tính xem có nhảy không
        branch_taken = cond_met(cond)

        return (1 if branch_taken else 0,)
    
    if block == 'SL2':
        inp = data['SL2']['Inp0'] 
        val = int(inp, 10)     
        shifted_val = val << 2    
        return (shifted_val,)
        
    return (None,)
