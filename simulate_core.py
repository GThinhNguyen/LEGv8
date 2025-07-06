"""
Module chứa logic cốt lõi của simulation
"""
import bits
from simulate_data import connection_map

def logic_step_from_block(start_block, lines, line_next, ui):
    """
    Xử lý logic truyền dữ liệu giữa các block, KHÔNG tạo animation.
    """
    bit_tuple = bits.get_bits_for_path(start_block, ui)
    next_blocks = line_next.get(start_block, [])
    
    for i, next_line in enumerate(next_blocks):
        bit_str = bit_tuple[i] if isinstance(bit_tuple, (tuple, list)) and i < len(bit_tuple) else str(bit_tuple[-1]) if isinstance(bit_tuple, (tuple, list)) else str(bit_tuple)
        if next_line in connection_map:
            for conn in connection_map[next_line]:
                conn['value'] = str(bit_str)
                bits.data[conn['to']][conn['port']] = conn['value']

def add2(bit_data, lines_list):
    """
    Thêm subscript 2 cho các line nhất định
    """
    lines_need_subscript = {'L30', 'L31', 'L32', 'L33', 'L34', 'L35', 'L36', 'L37', 'L38', 'L53', 'L50', 'L61'}
    
    if isinstance(bit_data, (tuple, list)):
        result = []
        for i, bit_str in enumerate(bit_data):
            if i < len(lines_list) and lines_list[i] in lines_need_subscript:
                result.append(f"{bit_str}$_2$")
            else:
                result.append(str(bit_str))
        return result
    else:
        if lines_list and lines_list[0] in lines_need_subscript:
            return f"{bit_data}$_2$"
        else:
            return str(bit_data)

def get_simulation_order():
    """Trả về thứ tự các block trong simulation"""
    return [
        'PC', 'P1', 'IM', 'P2', 'Control',
        'P3', 'M1', 'Reg', 'P5',
        'P4', 'ALUControl', 'SE', 'P6', 'M2', 'ALU', 'P7', 'Mem',
        'M3', 'Flags', 'AND1', 'AND2', 'OR',
        'SL2', 'P8', 'ADD1', 'ADD2', 'M4'
    ]