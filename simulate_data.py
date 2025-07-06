"""
Module chứa tất cả dữ liệu cấu hình của simulation
"""
import numpy as np
polygons = {
    'PC': np.array([[ -250, 520], [ -200, 570]]),
    'IM': np.array([[-120, 470], [40, 630]]),
    'Reg': np.array([[600, 450], [770, 690]]),
    'Mem': np.array([[1200, 620], [1350, 800]]),
    'Flags': np.array([[1030, 400], [1190, 440]]),

    'M1': np.array([[470, 480], [500, 580]]),
    'M2': np.array([[900, 550], [930, 650]]),
    'M3': np.array([[1690, 560], [1720, 660]]),
    'M4': np.array([[1630, -10], [1660, 90]]),

    'SE': np.array([[680, 700], [780, 800]]),
    'SL2': np.array([[940, 60], [1020, 140]]),
    'ALUControl': np.array([[910, 770], [1010, 870]]),
    'Control': np.array([[360, 150], [460, 400]]),

    'ALU': np.array([[1120, 520], [1120, 600], [1000, 640], [1000, 570], [1030, 560], [1000, 550], [1000, 480]]),
    'ADD2': np.array([[1180, 60], [1180, 95], [1120, 115], [1120, 82.5], [1135, 77.5], [1120, 72.5], [1120, 40]]),
    'ADD1': np.array([[240, -10], [240, 25], [180, 45], [180, 12.5], [195, 7.5], [180, 2.5], [180, -30]]),

    'OR': np.array([[1540, 360], [1610, 440]]),
    'AND1': np.array([[1380, 360], [1480, 440]]),
    'AND2': np.array([[1380, 480], [1480, 560]]),
}

points = {
    'P1': (-160, 530),
    'P2': (210, 500),
    'P3': (360, 560),
    'P4': (440, 750),
    'P5': (810, 570),
    'P6': (850, 630),
    'P7': (1160, 580),
    'P8': (-160, 50),
    'P9': (210, 470),
    'P10': (210, 560)
}

lines = {
    'L18': np.array([[420, 150], [1705, 150], [1705, 560]]),
    'L14': np.array([[440, 175], [1480, 175], [1480, 370], [1550, 370]]),
    'L15': np.array([[450, 200], [1340, 200], [1340, 380], [1380, 380]]),
    'L16': np.array([[460, 225], [1300, 225], [1300, 500], [1380, 500]]),
    'L17': np.array([[460, 250], [1260, 250], [1260, 620]]),
    'L19': np.array([[460, 275], [1220, 275], [1220, 620]]),
    'L20': np.array([[460, 300], [1080, 300], [1080, 400]]),
    'L22': np.array([[460, 325], [960, 325], [960, 770]]),
    'L21': np.array([[450, 350], [915, 350], [915, 550]]),
    'L23': np.array([[440, 375], [685, 375], [685, 450]]),
    'L13': np.array([[420, 400], [485, 400], [485, 480]]),

    'L24': np.array([[1010, 820], [1070, 820], [1070, 620]]),

    'L25': np.array([[1120, 540], [1380, 540]]),
    'L26': np.array([[1440, 400], [1550, 400]]),
    'L27': np.array([[1610, 400], [1645, 400], [1645, 100]]),
    'L28': np.array([[1440, 520], [1480, 520], [1480, 430], [1550, 430]]),

    'L45': np.array([[1120, 580], [1160, 580]]),
    'L46': np.array([[1160, 580], [1160, 650], [1200, 650]]),
    'L47': np.array([[1160, 580], [1690, 580]]),

    'L48': np.array([[1070, 500], [1070, 460]]),

    'L29': np.array([[40, 500], [210, 500]]),
    'L32': np.array([[210, 470], [210, 330], [360, 330]]),
    'L33': np.array([[210, 500], [210, 470], [600, 470]]),
    'L34': np.array([[210, 500], [470, 500]]),
    'L36': np.array([[210, 500], [210, 560], [360, 560]]),
    'L37': np.array([[360, 560], [470, 560]]),
    'L38': np.array([[360, 560], [360, 590], [600, 590]]),
    'L39': np.array([[210, 560], [210, 750], [440, 750]]),
    'L40': np.array([[440, 750], [680, 750]]),
    'L53': np.array([[440, 750], [440, 820], [910, 820]]),

    'L41': np.array([[770, 500], [1000, 500]]),
    'L42': np.array([[770, 570], [810, 570]]),
    'L43': np.array([[810, 570], [900, 570]]),
    'L44': np.array([[810, 570], [810, 700], [1200, 700]]),

    'L49': np.array([[1350, 640], [1690, 640]]),

    'L50': np.array([[500, 530], [600, 530]]),
    'L51': np.array([[930, 600], [1000, 600]]),
    'L52': np.array([[1720, 610], [1740, 610], [1740, 890], [360, 890], [360, 630], [600, 630]]),
    'L9a': np.array([[1660, 40], [1740, 40], [1740, -50], [ -225, -50], [ -225, 520]]),

    'L54': np.array([[780, 750], [850, 750], [850, 630]]),
    'L55': np.array([[850, 630], [900, 630]]),
    'L56': np.array([[850, 630], [850, 100], [940, 100]]),

    'L57': np.array([[1020, 100], [1120, 100]]),

    'L60': np.array([[1190, 420], [1380, 420]]),
    'L61': np.array([[360, 560], [360, 420], [1030, 420]]),

    'L58': np.array([[-200, 530], [-160, 530]]),
    'L59': np.array([[-160, 530], [-120, 530]]),
    'L1': np.array([[-160, 530], [-160, 50]]),
    'L5': np.array([[-160, 50], [1120, 50]]),
    'L2': np.array([[-160, 50], [-160, -20], [180, -20]]),

    'L4': np.array([[120, 30], [180, 30]]),

    'L8': np.array([[240, 10], [1630, 10]]),
    'L9b': np.array([[1180, 70], [1630, 70]])
}

line_next = {
    # Control outputs
    'Control': ['L13','L14', 'L15', 'L16', 'L17', 'L18', 'L19', 'L20', 'L21', 'L22', 'L23'],
    'PC': ['L58'],
    'IM': ['L29'],
    'Reg': ['L41', 'L42'],
    'ALU': ['L25', 'L45', 'L48'],
    'ALUControl': ['L24'],
    'Mem': ['L49'],
    'Flags': ['L60'],
    'ADD1': ['L8'],
    'ADD2': ['L9b'],
    'AND1': ['L26'],
    'AND2': ['L28'],
    'OR': ['L27'],
    'SL2': ['L57'],
    'M1': ['L50'],
    'M2': ['L51'],
    'M3': ['L52'],
    'M4': ['L9a'],
    'SE': ['L54'],

    # Points to lines
    'P1': ['L59', 'L1'],
    'P2': ['L32', 'L33', 'L34', 'L36', 'L39'],
    'P3': ['L37', 'L38', 'L61'],
    'P4': ['L40', 'L53'],
    'P5': ['L43', 'L44'],
    'P6': ['L55', 'L56'],
    'P7': ['L46', 'L47'],
    'P8': ['L2', 'L5'],

}

# key là tên block, value là list các dict chứa thông tin đối tượng đích, cổng và giá trị hiện tại
connection_map = {
    'L13': [{'to': 'M1', 'port': 'Control', 'value': '0'}],
    'L14': [{'to': 'OR', 'port': 'Inp0', 'value': '0'}],
    'L15': [{'to': 'AND1', 'port': 'Inp0', 'value': '0'}],
    'L16': [{'to': 'AND2', 'port': 'Inp0', 'value': '0'}],
    'L17': [{'to': 'Mem', 'port': 'MemRead', 'value': '0'}],
    'L18': [{'to': 'M3', 'port': 'Control', 'value': '0'}],
    'L19': [{'to': 'Mem', 'port': 'MemWrite', 'value': '0'}],
    'L20': [{'to': 'Flags', 'port': 'Control', 'value': '0'}],
    'L21': [{'to': 'M2', 'port': 'Control', 'value': '0'}],
    'L22': [{'to': 'ALUControl', 'port': 'ALUop', 'value': '0'}],
    'L23': [{'to': 'Reg', 'port': 'RegWrite', 'value': '0'}],
    'L24': [{'to': 'ALU', 'port': 'ALUControl', 'value': '0'}],
    'L25': [{'to': 'AND2', 'port': 'Inp1', 'value': '0'}],
    'L26': [{'to': 'OR', 'port': 'Inp1', 'value': '0'}],
    'L27': [{'to': 'M4', 'port': 'Control', 'value': '0'}],
    'L28': [{'to': 'OR', 'port': 'Inp2', 'value': '0'}],
    'L29': [{'to': 'P2', 'port': 'Inp0', 'value': '0'}],
    'L32': [{'to': 'Control', 'port': 'Inp0', 'value': '0'}],
    'L33': [{'to': 'Reg', 'port': 'ReadRegister1', 'value': '0'}],
    'L34': [{'to': 'M1', 'port': 'Inp0', 'value': '0'}],
    'L36': [{'to': 'P3', 'port': 'Inp0', 'value': '0'}],
    'L37': [{'to': 'M1', 'port': 'Inp1', 'value': '0'}],
    'L38': [{'to': 'Reg', 'port': 'WriteRegister', 'value': '0'}],
    'L39': [{'to': 'P4', 'port': 'Inp0', 'value': '0'}],
    'L40': [{'to': 'SE', 'port': 'Inp', 'value': '0'}],
    'L41': [{'to': 'ALU', 'port': 'ReadData1', 'value': '0'}],
    'L42': [{'to': 'P5', 'port': 'Inp0', 'value': '0'}],
    'L43': [{'to': 'M2', 'port': 'Inp0', 'value': '0'}],
    'L44': [{'to': 'Mem', 'port': 'WriteData', 'value': '0'}],
    'L45': [{'to': 'P7', 'port': 'Inp0', 'value': '0'}],
    'L46': [{'to': 'Mem', 'port': 'Address', 'value': '0'}],
    'L47': [{'to': 'M3', 'port': 'Inp0', 'value': '0'}],
    'L48': [{'to': 'Flags', 'port': 'NZCVtmp', 'value': '0'}],
    'L49': [{'to': 'M3', 'port': 'Inp1', 'value': '0'}],
    'L50': [{'to': 'Reg', 'port': 'ReadRegister2', 'value': '0'}],
    'L51': [{'to': 'ALU', 'port': 'ReadData2', 'value': '0'}],
    'L52': [{'to': 'Reg', 'port': 'WriteData', 'value': '0'}],
    'L53': [{'to': 'ALUControl', 'port': 'Ins', 'value': '0'}],
    'L54': [{'to': 'P6', 'port': 'Inp0', 'value': '0'}],
    'L55': [{'to': 'M2', 'port': 'Inp1', 'value': '0'}],
    'L56': [{'to': 'SL2', 'port': 'Inp0', 'value': '0'}],
    'L57': [{'to': 'ADD2', 'port': 'Inp1', 'value': '0'}],
    'L58': [{'to': 'P1', 'port': 'Inp0', 'value': '0'}],
    'L59': [{'to': 'IM', 'port': 'ReadAddress', 'value': '0'}],
    'L60': [{'to': 'AND1', 'port': 'Inp1', 'value': '0'}],
    'L61': [{'to': 'Flags', 'port': 'Condition', 'value': '0'}],
    

    'L1':  [{'to': 'P8', 'port': 'Inp0', 'value': '0'}],
    'L2':  [{'to': 'ADD1', 'port': 'Inp0', 'value': '0'}],
    'L4':  [{'to': 'ADD1', 'port': 'Inp1', 'value': '100'}],
    'L5':  [{'to': 'ADD2', 'port': 'Inp0', 'value': '0'}],
    'L8':  [{'to': 'M4', 'port': 'Inp0', 'value': '0'}],
    'L9a': [{'to': 'PC', 'port': 'Inp0', 'value': '0'}],
    'L9b': [{'to': 'M4', 'port': 'Inp1', 'value': '0'}],
}

# Mapping for full names of blocks, allow line breaks with \n
full_names = {
    'IM': 'Instruction\nmemory',
    'Reg': 'Registers',
    'Mem': 'Data\nmemory',
    'SE': 'Sign-\nextend',
    'ALUControl': 'ALU\ncontrol',
    'SL2': 'Shift\nleft 2'
}