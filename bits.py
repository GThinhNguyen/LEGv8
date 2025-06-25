import mainwindow_ui
import simulate
import main

# Bộ nhớ giả lập\ nMEMORY = {}

data = {
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
    'Flags': {'Control': '0', 'NZCVtmp': '0000', 'NZCV': '0000'},
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

def bin_to_signed(s):
    value = int(s, 2)
    bits = len(s)
    if value >= 2**(bits - 1):
        value -= 2**bits
    return value

def parse_signed(val):
    if isinstance(val, str) and set(val) <= {'0', '1'} and len(val) == 32:
        return bin_to_signed(val)
    try:
        return int(val)
    except Exception:
        return 0

def get_register_value(idx, ui):
    item = ui.registerShow.item(idx, 0)
    try:
        return int(item.text()) if item and item.text() not in ("", None) else 0
    except Exception:
        return 0

def assemble_instruction(inst_str):
    parts = inst_str.replace(',', '').replace('[', '').replace(']', '').split()
    op = parts[0].upper()

    if op in ('ADD', 'SUB', 'AND', 'ORR', 'ADDS', 'SUBS', 'ANDS'):
        rd, rn, rm = [int(p.replace('X','')) for p in parts[1:4]]
        opcodes = {
            'ADD': 0b10001011000,
            'SUB': 0b11001011000,
            'AND': 0b10001010000,
            'ORR': 0b10101010000,
            'ADDS':0b10101011000,
            'SUBS':0b11101011000,
            'ANDS':0b11101010000,
        }
        opcode = opcodes[op]
        shamt = 0
        instr = (opcode << 21) | (rm << 16) | (shamt << 10) | (rn << 5) | rd
    elif op == 'LDUR':
        # cú pháp: LDUR Xd, [Xn, #imm]
        rt = int(parts[1].replace('X',''))
        rn = int(parts[2].replace('X',''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b11111000010
        instr = (opcode << 21) | ((imm & 0x1FF) << 12) | (rn << 5) | rt
    elif op == 'STUR':
        rt = int(parts[1].replace('X',''))
        rn = int(parts[2].replace('X',''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b11111000000
        instr = (opcode << 21) | ((imm & 0x1FF) << 12) | (rn << 5) | rt
    elif op == 'CBZ':
        rt = int(parts[1].replace('X',''))
        imm = int(parts[2].lstrip('#'))
        opcode = 0b10110100
        instr = (opcode << 24) | ((imm & 0x7FFFF) << 5) | rt
    elif op == 'B':
        imm = int(parts[1].lstrip('#'))
        opcode = 0b000101
        instr = (opcode << 26) | (imm & 0x3FFFFFF)
    elif op == 'ADDI':
        rd = int(parts[1].replace('X', ''))
        rn = int(parts[2].replace('X', ''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1001000100
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'SUBI':
        rd = int(parts[1].replace('X', ''))
        rn = int(parts[2].replace('X', ''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1101000100
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'ANDI':
        rd = int(parts[1].replace('X', ''))
        rn = int(parts[2].replace('X', ''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1001001000
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'ORRI':
        rd = int(parts[1].replace('X', ''))
        rn = int(parts[2].replace('X', ''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1011001000
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'ADDIS':
        rd = int(parts[1].replace('X',''))
        rn = int(parts[2].replace('X',''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1011000100
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'ANDIS':
        rd = int(parts[1].replace('X',''))
        rn = int(parts[2].replace('X',''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1111001000
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    elif op == 'SUBIS':
        rd = int(parts[1].replace('X',''))
        rn = int(parts[2].replace('X',''))
        imm = int(parts[3].lstrip('#'))
        opcode = 0b1111000100
        instr = (opcode << 22) | ((imm & 0xFFF) << 10) | (rn << 5) | rd
    else:
        raise ValueError(f"assemble_instruction(): lệnh không hỗ trợ: {inst_str}")

    return format(instr, '032b'),

def get_bits_for_path(block, ui = None):
    # Trả về giá trị hoặc hàm trả giá trị dạng tuple
    if block in ['M1', 'M2', 'M3', 'M4']:
        if data[block]['Control'] == '0':
            return (data[block]['Inp0'],)
        else:
            return (data[block]['Inp1'],)
    if block in ['P1', 'P3', 'P5', 'P6', 'P7', 'P8']:
        return (data[block]['Inp0'], data[block]['Inp0'])
    if block == 'P4':
        instr = data['P4']['Inp0']
        opcode = instr[0:11]
        return (data[block]['Inp0'], opcode)
    if block == 'P2':
        #  Trả về tuple các trường opcode, Rn, Rm, Rd, full instruction từ chuỗi nhị phân 32 bit
        instr = data['P2']['Inp0']
        opcode = instr[0:11]
        rm     = instr[11:16]
        rn     = instr[22:27]
        rd     = instr[27:32]
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
            '10101011000': '0,0,0,0,0,0,0,1,0,10,1',  #ADDS
            '11101011000': '0,0,0,0,0,0,0,1,0,10,1',  #SUBS
            '11101010000': '0,0,0,0,0,0,0,1,0,10,1',  #ANDS
            '11111000010': '0,0,0,0,1,1,0,0,1,00,1',  # LDUR
            '11111000000': '1,0,0,0,0,0,1,0,1,00,0',  # STUR
        }
        if inp in controls:
            return tuple(controls[inp].split(','))
        if inp[0:8] == '10110100':  # CBZ
            return ('1', '0', '1', '1', '0', '0', '0', '0', '0', '01', '0')
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
        if inp[0:10] == '1011000100':  # ADDIS
            return ('0', '0', '0', '0', '0', '0', '0', '1', '1', '10', '1')
        if inp[0:10] == '1111000100':  # SUBIS
            return ('0', '0', '0', '0', '0', '0', '0', '1', '1', '10', '1')
        if inp[0:10] == '1111001000':  # ANDIS
            return ('0', '0', '0', '0', '0', '0', '0', '1', '1', '10', '1')
        raise KeyError(f"Unrecognized opcode: {inp}")
    if block == 'SE':
        instr = data['SE']['Inp']  # chuỗi 32-bit: instr[0] = bit 31, instr[31] = bit 0
        opcode1 = instr[0:11]       # 11-bit opcode
        opcode2= instr[0:8]        # 8-bit opcode
        opcode3 = instr[0:6]        # 6-bit opcode
        opcode4 = instr[0:10]       # 10-bit opcode
        # Xác định vị trí và độ dài immediate theo định dạng D, CBZ, B
        if opcode1 in ('11111000010', '11111000000'):    # LDUR, STUR (D-type)
            # immediate bits [20:12] => indices [11:20) trong Python
            imm = instr[11:20]
        elif opcode2 == '10110100':  # CBZ (CB-type)
            imm = instr[8:27]
        elif opcode3 == '000101':     # B (B-type)
            imm = instr[6:32]
        elif opcode4 in ('1001000100', '1101000100', '1001001000', '1011001000', '1011000100', '1111000100', '1111001000'):  # ADDI, SUBI, ANDI, ORRI, ADDIS, SUBIS, ANDIS (I-type)
            imm = instr[10:22]
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
            }
            table2 = {
                '1001000100': '0010',  # ADDI
                '1011000100': '0010',  # ADDIS
                '1101000100': '0110',  # SUBI
                '1111000100': '0110',  # SUBIS
                '1001001000': '0000',  # ANDI
                '1111001000': '0000',  # ANDIS
                '1011001000': '0001'   # ORRI
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
            return assemble_instruction(lines[idx].strip())
        return ('0'*64,)
    if block == 'Reg':
        def reg_out():
            r1 = int(data['Reg']['ReadRegister1'], 2)
            r2 = int(data['Reg']['ReadRegister2'], 2)
            return (get_register_value(r1, ui), format(get_register_value(r2, ui)))
        return reg_out()
    
    if block == 'Mem':
        addr = int(data['Mem']['Address'], 10)
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
        a = parse_signed(data['ALU']['ReadData1'])
        b = parse_signed(data['ALU']['ReadData2'])
        print(a,b)
        op = data['ALU']['ALUControl']
        if op == '0010': res = a + b
        elif op == '0110': res = a - b
        elif op == '0000': res = a & b
        elif op == '0001': res = a | b
        elif op == '0111': res = a ^ b
        else: res = 0
        zeroFlag = 1 if res == 0 else 0
        nFlag = 1 if res < 0 else 0
        cFlag = 1 if res > 0xFFFFFFFF else 0
        vFlag = 1 if (a < 0 and b < 0 and res >= 0) or (a >= 0 and b >= 0 and res < 0) else 0
        Flag = str(nFlag) + str(zeroFlag) + str(cFlag) + str(vFlag)
        return (zeroFlag ,res, Flag)
    if block == 'Flags':
        control = data['Flags']['Control']
        if control == '1':
            nzcv = data['Flags']['NZCVtmp']
            data['Flags']['NZCV'] = nzcv
        
        nzcv = data['Flags']['NZCV']  # string 4 ký tự, ví dụ "1010"
        n, z, c, v = nzcv[0], nzcv[1], nzcv[2], nzcv[3]

        # Nếu muốn đổi màu nền để nổi bật khi flag = 1:
        def highlight_flag(label, bit):
            if bit == '1':
                label.setStyleSheet(label.styleSheet() + "background-color: lightgreen;")
            else:
                # reset về lightgray như mặc định
                label.setStyleSheet(label.styleSheet().replace("background-color: lightgreen;", ""))

        highlight_flag(ui.n_flag, n)
        highlight_flag(ui.z_flag, z)
        highlight_flag(ui.c_flag, c)
        highlight_flag(ui.v_flag, v)
        zeroFlag = data['Flags']['NZCV'][1]
        return (zeroFlag,)
    
    if block == 'SL2':
        inp = data['SL2']['Inp0'] 
        val = int(inp, 10)     
        shifted_val = val << 2    
        return (shifted_val,)
        
    print(f"get_bits_for_path(): không hỗ trợ block {block}")
    return (None,)