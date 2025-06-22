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
    'ADD1': {'Inp0': '0', 'Inp1': '0'},
    'M1': {'Control': '0', 'Inp0': '0', 'Inp1': '0'},
    'M2': {'Control': '0', 'Inp0': '0', 'Inp1': '0'},
    'M3': {'Control': '0', 'Inp0': '0', 'Inp1': '0'},
    'M4': {'Control': '0', 'Inp0': '0', 'Inp1': '0'},
    'Flags': {'Control': '0', 'N': '0', 'Z': '0', 'C': '0', 'V': '0'},
    'SE': {'Inp': '0'},
    'ALUControl': {'ALUop': '0', 'Ins': '0'},
    'Control': {'Inp0': '0'},
    'XOR': {'Inp0': '0', 'Inp1': '0', 'Inp2': '0'},
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
        return (tuple(data[block]['Inp0']) if data[block]['Control'] == '0' else tuple(data[block]['Inp1']))
    if block in ['P1', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8']:
        return (data[block]['Inp0'], data[block]['Inp0'])
    if block == 'P2':
        # Trả về tuple các trường opcode, Rn, Rm, Rd, full instruction từ chuỗi nhị phân 32 bit
        val = data['P2']['Inp0']
        return (
            val[0:11],   # opcode (bits 0-10)
            val[12:17],  # Rn (bits 12-16)
            val[16:21],  # Rm (bits 16-20)
            val[21:26],  # Rd (bits 21-25)
            val          # full 32-bit instruction
        )
    if block in ['ADD1', 'ADD2']:
        return (lambda: (str(int(data[block]['Inp0']) + int(data[block]['Inp1'])),),)
    if block == 'XOR':
        return (lambda: (format(int(data['XOR']['Inp0'],2) ^ int(data['XOR']['Inp1'],2) ^ int(data['XOR']['Inp2'],2), 'b'),),)
    if block in ['AND1', 'AND2']:
        return (lambda: (format(int(data[block]['Inp0'],2) & int(data[block]['Inp1'],2), 'b'),),)
    if block == 'Control':
        inp = data['Control']['Inp0']
        print(inp)
        controls = {
            '10001011000': '0,0,0,0,0,0,0,1,0,10,1',  # ADD
            '11001011000': '0,0,0,0,0,0,0,1,0,10,1',  # SUB
            '10001010000': '0,0,0,0,0,0,0,1,0,10,1',  # AND
            '10101010000': '0,0,0,0,0,0,0,1,0,10,1',  # ORR
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
        inp = data['SE']['Inp']
        sign = inp[0]
        return (sign * (64 - len(inp)) + inp,)
    if block == 'ALUControl':
        aluop = data['ALUControl']['ALUop']
        ins   = data['ALUControl']['Ins']
        if aluop == '10':
            table = {
                '10001011000': '0010',
                '11001011000': '0110',
                '10001010000': '0000',
                '10101010000': '0001'
            }
            return (table.get(ins, '0010'),)
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
        return ('0'*32,)
    if block == 'Reg':
        def reg_out():
            r1 = int(data['Reg']['ReadRegister1'], 2)
            r2 = int(data['Reg']['ReadRegister2'], 2)
            print(r1, r2)
            return (format(get_register_value(r1, ui), 'b'), format(get_register_value(r2, ui), 'b'))
        return reg_out()
    if block == 'Mem':
        def mem_access():
            addr = int(data['Mem']['Address'], 2)
            word_row = (addr // 4) * 4
            if data['Mem']['MemRead'] == '1':
                item = main.ui.ramTable.item(word_row, 3)
                val = int(item.text()) if item and item.text().isdigit() else 0
                return (format(val, '032b'),)
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
            return ('0' * 32,)
        return (mem_access,)
    if block == 'ALU':
        def alu():
            a = int(data['ALU']['ReadData1'],2)
            b = int(data['ALU']['ReadData2'],2)
            op = get_bits_for_path('ALUControl')[0]()
            if op == '0010': res = a + b
            elif op == '0110': res = a - b
            elif op == '0000': res = a & b
            elif op == '0001': res = a | b
            elif op == '0111': res = a ^ b
            else: res = 0
            return (format(res, 'b'), lambda: 1 if res == 0 else 0)
        return (alu,)
    if block == 'Flags':
        def fl():
            if data['Flags']['Control'] == '1':
                return ({'N': data['Flags']['N'], 'Z': data['Flags']['Z'], 'C': data['Flags']['C'], 'V': data['Flags']['V']},)
            return (None,)
        return (fl,)

    return (None,)


