data = {
    'PC': {'Inp0': 0},
    'IM': {'ReadAddress': 0},
    'Reg': {'Control': 0, 'ReadRegister1': 0, 'ReadRegister2': 0, 'WriteRegister': 0, 'WriteData': 0},
    'Mem': {'Address': 0, 'WriteData': 0},
    'ALU': {'Control': 0, 'Inp0': 0, 'Inp1': 0},
    'ADD2': {'Inp0': 0, 'Inp1': 0},
    'ADD1': {'Inp0': 0, 'Inp1': 0},
    'M1': {'Control': 0, 'Inp0': 0, 'Inp1': 0},
    'M2': {'Control': 0, 'Inp0': 0, 'Inp1': 0},
    'M3': {'Control': 0, 'Inp0': 0, 'Inp1': 0},
    'M4': {'Control': 0, 'Inp0': 0, 'Inp1': 0},
    'Flags': {'Control': 0, 'N': 0, 'Z': 0, 'C': 0, 'V': 0},
    'SE': {'Inp': 0},
    'ALUControl': {'Control': 0},
    'Control': {'Inp': 0},
    'XOR': {'Inp0': 0, 'Inp1': 0, 'Inp2': 0},
    'AND1': {'Inp0': 0, 'Inp1': 0},
    'AND2': {'Inp0': 0, 'Inp1': 0},
    'SL2': {'Inp0': 0},
    'P1': {'Val': 0},
    'P2': {'Val': 0},
    'P3': {'Val': 0},
    'P4': {'Val': 0},
    'P5': {'Val': 0},
    'P6': {'Val': 0},
    'P7': {'Val': 0},
    'P8': {'Val': 0}
}


data_path = {
    'L13': 0,
    'L14': 0,
    'L15': 0,
    'L16': 0,
    'L17': 0,
    'L18': 0,
    'L19': 0,
    'L20': 0,
    'L21': 0,
    'L22': 0,
    'L23': 0,
    'L24': 0,
    'L25': 0,
    'L26': 0,
    'L27': 0,
    'L28': 0,
    'L29': 0,
    'L32': 0,
    'L33': 0,
    'L34': 0,
    'L36': 0,
    'L37': 0,
    'L38': 0,
    'L39': 0,
    'L40': 0,
    'L41': 0,
    'L42': 0,
    'L43': 0,
    'L44': 0,
    'L45': 0,
    'L46': 0,
    'L47': 0,
    'L48': 0,
    'L49': 0,
    'L50': 0,
    'L51': 0,
    'L52': 0,
    'L53': 0,
    'L54': 0,
    'L55': 0,
    'L56': 0,
    'L57': 0,
    'L58': 0,
    'L59': 0,
    'L60': 0,
    'L1': 0,
    'L2': 0,
    'L4': 0,
    'L5': 0,
    'L8': 0,
    'L9a': 0,
    'L9b': 0,
}


def get_bits_for_path(block, to_key):
    if block in ['M1', 'M2', 'M3', 'M4']:
        def mux_output():
            control = data[block]['Control']
            return data[block]['Inp0'] if control == 0 else data[block]['Inp1']
        return mux_output
    elif block in data and to_key in data[block]:
        return 0
    else:
        return 0
