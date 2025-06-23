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

def get_register_value(idx, ui):
    item = ui.registerShow.item(idx, 0)
    return int(item.text()) if item and item.text().isdigit() else 0

def assemble_instruction(inst_str):
    parts = inst_str.replace(',', '').replace('[', '').replace(']', '').split()
    op = parts[0].upper()

    if op in ('ADD', 'SUB', 'AND', 'ORR'):
        rd, rn, rm = [int(p.replace('X','')) for p in parts[1:4]]
        opcodes = {
            'ADD': 0b10001011000,
            'SUB': 0b11001011000,
            'AND': 0b10001010000,
            'ORR': 0b10101010000,
        }
        opcode = opcodes[op]
        shamt = 0
        instr = (opcode << 21) | (rm << 16) | (shamt << 10) | (rn << 5) | rd
    elif op == 'LDUR':
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
        return (format(int(data[block]['Inp0']) + int(data[block]['Inp1']), 'b'),)
    if block == 'OR':
        return (format(int(data['OR']['Inp0'],2) | int(data['OR']['Inp1'],2) | int(data['OR']['Inp2'],2), 'b'),)
    if block in ['AND1', 'AND2']:
        return (format(int(data[block]['Inp0'],2) & int(data[block]['Inp1'],2), 'b'),)
    if block == 'Control':
        inp = data['Control']['Inp0']
        controls = {
            '10001011000': '0,0,0,0,0,0,0,0,0,10,1',  # ADD
            '11001011000': '0,0,0,0,0,0,0,0,0,10,1',  # SUB
            '10001010000': '0,0,0,0,0,0,0,0,0,10,1',  # AND
            '10101010000': '0,0,0,0,0,0,0,0,0,10,1',  # ORR
            '11111000010': '0,0,0,0,1,1,0,0,1,00,1',  # LDUR
            '11111000000': '1,0,0,0,0,0,1,0,1,00,0',  # STUR
            '00010100000': '0,1,0,0,0,0,0,0,0,00,0',  # B
            '10110100000': '1,0,1,1,0,0,0,0,0,01,0'   # CBZ
        }
        if inp in controls:
            return tuple(controls[inp].split(','))
        else:
            raise KeyError(f"Unrecognized opcode: {inp}")
    if block == 'SE':
        instr = data['SE']['Inp']  # chuỗi 32-bit: instr[0] = bit 31, instr[31] = bit 0
        opcode1 = instr[0:11]       # 11-bit opcode
        opcode2= instr[0:8]        # 8-bit opcode
        opcode3 = instr[0:6]        # 6-bit opcode
        # Xác định vị trí và độ dài immediate theo định dạng D, CBZ, B
        if opcode1 in ('11111000010', '11111000000'):    # LDUR, STUR (D-type)
            # immediate bits [20:12] => indices [11:20) trong Python
            imm = instr[11:20]
        elif opcode2 == '10110100':  # CBZ (CB-type)
            imm = instr[8:27]
        elif opcode3 == '000101':     # B (B-type)
            imm = instr[6:32]
        else:
            # Không phải lệnh có immediate
            return ('0' * 64,)

        # sign-extend lên 64 bit
        sign_bit = imm[0]
        extended = sign_bit * (64 - len(imm)) + imm

        return (extended,)
    if block == 'ALUControl':
        aluop = data['ALUControl']['ALUop']
        ins   = data['ALUControl']['Ins']
        if aluop == '10':
            table = {
                '10001011000': '0010', # ADD
                '11001011000': '0110', # SUB
                '10001010000': '0000', # AND
                '10101010000': '0001' # ORR
            }
            return (table.get(ins, '0000'),)
        if aluop == '00': return ('0010',)
        if aluop == '01': return ('0111',)
        return ('0000',)
    if block == 'PC':
        return (data['PC']['Inp0'],)
    if block == 'IM':
        addr = int(data['IM']['ReadAddress'], 2)
        idx = addr // 4
        lines = ui.codeEditor.toPlainText().splitlines()        
        if 0 <= idx < len(lines):
            return assemble_instruction(lines[idx].strip())
        return ('0'*64,)
    if block == 'Reg':
        def reg_out():
            r1 = int(data['Reg']['ReadRegister1'], 2)
            r2 = int(data['Reg']['ReadRegister2'], 2)
            return (format(get_register_value(r1, ui), 'b'), format(get_register_value(r2, ui), 'b'))
        return reg_out()
    
    if block == 'Mem':
        addr = int(data['Mem']['Address'], 2)
        word_row = (addr // 4) * 4
        if data['Mem']['MemWrite'] == '1':
            val = int(data['Mem']['WriteData'], 2)
            w_item = main.ui.ramTable.item(word_row, 3)
            if w_item:
                w_item.setText(str(val))
            for i in range(4):
                byte_val = (val >> (8 * (3 - i))) & 0xFF
                b_item = main.ui.ramTable.item(word_row + i, 1)
                if b_item:
                    b_item.setText(str(byte_val))
            return ('',)
        if data['Mem']['MemRead'] == '1':
            item = main.ui.ramTable.item(word_row, 3)
            val = int(item.text()) if item and item.text().isdigit() else 0
            return (format(val, '032b'),)
        return ('0' * 32,)

    if block == 'ALU':
        a = int(data['ALU']['ReadData1'],2)
        b = int(data['ALU']['ReadData2'],2)
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
        return (zeroFlag ,format(res, 'b'), Flag)
    if block == 'Flags':
        control = data['Flags']['Control']
        if control == '1':
            nzcv = data['Flags']['NZCVtmp']
            data['Flags']['NZCV'] = nzcv
        
        zeroFlag = data['Flags']['NZCV'][1]
        return (zeroFlag,)
    
    if block == 'SL2':
        inp = data['SL2']['Inp0'] 
        val = int(inp, 2)        
        shifted_val = val << 2   
        shifted_bin = format(shifted_val & 0xFFFFFFFF, '032b')  
        return (shifted_bin,)
        
    print(f"get_bits_for_path(): không hỗ trợ block {block}")
    return (None,)