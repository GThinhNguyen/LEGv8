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
