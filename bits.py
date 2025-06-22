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
    'Control': {'Inp': '0'},
    'XOR': {'Inp0': '0', 'Inp1': '0', 'Inp2': '0'},
    'AND1': {'Inp0': '0', 'Inp1': '0'},
    'AND2': {'Inp0': '0', 'Inp1': '0'},
    'SL2': {'Inp0': '0'},
    'P1': {'Val': '0'},
    'P2': {'Val': ''},
    'P3': {'Val': '0'},
    'P4': {'Val': '0'},
    'P5': {'Val': '0'},
    'P6': {'Val': '0'},
    'P7': {'Val': '0'},
    'P8': {'Val': '0'}
}

def get_register_value(idx):
    item = main.ui.registerShow.item(idx, 0)
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
        instr = (opcode << 21) | (rm << 16) | (rn << 5) | rd
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

    return format(instr, '032b')

def get_bits_for_path(block, to_key=None, ui=None):
    # Trả về giá trị hoặc hàm trả giá trị dạng chuỗi
    if block in ['M1', 'M2', 'M3', 'M4']:
        return lambda: data[block]['Inp0'] if data[block]['Control'] == '0' else data[block]['Inp1']
    if block in ['P1', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8']:
        return lambda: data[block]['Val']
    if block == 'P2':
        return lambda: (data['P2']['Val'][5:9], data['P2']['Val'][16:20], data['P2']['Val'][21:31])
    if block in ['ADD1', 'ADD2']:
        return lambda: str(int(data[block]['Inp0']) + int(data[block]['Inp1']))
    if block == 'XOR':
        return lambda: format(int(data['XOR']['Inp0'],2) ^ int(data['XOR']['Inp1'],2) ^ int(data['XOR']['Inp2'],2), 'b')
    if block in ['AND1', 'AND2']:
        return lambda: format(int(data[block]['Inp0'],2) & int(data[block]['Inp1'],2), 'b')
    if block == 'Control':
      # tra ve mang Reg2Loc UncondBranch FlagBranch ZeroBranch memRead memtoReg MemWrite FlagWrite ALUSrc ALUOp   RegWrite
        inp = data['Control']['Inp']
        controls = {
            '10001011000': '00000000011',  # ADD
            '11001011000': '00000000011',  # SUB
            '10001010000': '00000000011',  # AND
            '10101010000': '00000000011',  # ORR
            '11111000010': '00001100101',  # LDUR
            '11111000000': '10000010100',  # STUR
            '00010100000': '01000000000',  # B
            '10110100000': '10010000000'   # CBZ
        }
        return controls.get(inp, '0'*12)
    if block == 'SE':
        inp = data['SE']['Inp']
        sign = inp[0]
        return sign * (64 - len(inp)) + inp
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
            return table.get(ins, '0010')
        if aluop == '00': return '0010'
        if aluop == '01': return '0111'
        return '0000'
    if block == 'PC':
        return data['PC']['Inp0']
    if block == 'IM':
        addr = int(data['IM']['ReadAddress'], 2)
        idx = addr // 4
        lines = main.ui.textEdit.toPlainText().splitlines()
        if 0 <= idx < len(lines):
            return assemble_instruction(lines[idx].strip())
        return '0'*32
    if block == 'Reg':
        def reg_out():
            r1 = int(data['Reg']['ReadRegister1'],2)
            r2 = int(data['Reg']['ReadRegister2'],2)
            return format(get_register_value(r1), 'b'), format(get_register_value(r2), 'b')
        return reg_out
    if block == 'Mem':
        def mem_access():
            # chuyển địa chỉ nhị phân sang số (số byte)
            addr = int(data['Mem']['Address'], 2)
            # số hàng chứa WordValue = addr // 4 * 4 (chỉ dòng đầu mỗi 4 bytes)
            word_row = (addr // 4) * 4
            # ĐỌC BỘ NHỚ
            if data['Mem']['MemRead'] == '1':
                item = main.ui.ramTable.item(word_row, 3)  # cột WordValue
                val = int(item.text()) if item and item.text().isdigit() else 0
                # trả về chuỗi nhị phân 32-bit
                return format(val, '032b')
            # GHI BỘ NHỚ
            if data['Mem']['MemWrite'] == '1':
                # giá trị cần ghi (nhị phân -> int)
                val = int(data['Mem']['WriteData'], 2)
                # cập nhật WordValue
                w_item = main.ui.ramTable.item(word_row, 3)
                if w_item:
                    w_item.setText(str(val))
                # cập nhật 4 ByteValue tương ứng (giả sử bạn muốn lưu luôn từng byte)
                for i in range(4):
                    byte_val = (val >> (8 * (3 - i))) & 0xFF
                    b_item = main.ui.ramTable.item(word_row + i, 1)  # cột ByteValue
                    if b_item:
                        b_item.setText(str(byte_val))
                # sau khi ghi, không cần trả về gì (bạn có thể trả chuỗi rỗng)
                return ''
            # mặc định
            return '0' * 32
        return mem_access
    if block == 'ALU':
        def alu():
            a = int(data['ALU']['ReadData1'],2)
            b = int(data['ALU']['ReadData2'],2)
            op = get_bits_for_path('ALUControl')()
            if op == '0010': res = a + b
            elif op == '0110': res = a - b
            elif op == '0000': res = a & b
            elif op == '0001': res = a | b
            elif op == '0111': res = a ^ b
            else: res = 0
            return format(res, 'b')
        return alu
    if block == 'Flags':
        def fl():
            if data['Flags']['Control'] == '1':
                return {'N': data['Flags']['N'], 'Z': data['Flags']['Z'], 'C': data['Flags']['C'], 'V': data['Flags']['V']}
            return None
        return fl

    return None
