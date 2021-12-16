
from operator import gt, lt, eq
from numpy import prod

print('Day 16 of Advent of Code!')

HEX_TO_BIN = {'0': '0000', 
            '1': '0001',
            '2': '0010',
            '3': '0011',
            '4': '0100',
            '5': '0101',
            '6': '0110',
            '7': '0111',
            '8': '1000',
            '9': '1001',
            'A': '1010',
            'B': '1011',
            'C': '1100',
            'D': '1101',
            'E': '1110',
            'F': '1111'}

ID_TO_OP = {0: sum,
            1: prod,
            2: min,
            3: max,
            4: 'VAL',
            5: gt,
            6: lt,
            7: eq}

LITERAL_PACKETS = ['4']
VERSION_ID_SIZE = 3
LITERAL_PACKET = 4
LITERAL_START = 6
HEADER_LENGTH = 6
LITERAL_FRAME = 5
LEN_ID_NUMBER = 1
LEN_ID_SIZE = 0
LEN_ID_POSITION = 6
LENGTH_FRAME = 15
NUMBER_FRAME = 11

def convert_to_bin(hex_packet):
    return ''.join(HEX_TO_BIN[digit] for digit in hex_packet)

def sum_versions(packet, total_versions=0):
    def get_value(packet):
        literal = ''
        pos, last = 0, False
        while True:
            current = packet[pos:pos+LITERAL_FRAME]
            if current[0] == '0':
                last = True
            literal += current[1:]
            pos += 5
            if last:
                break
        return int(literal, 2), packet[pos:]

    def is_ending(packet):
        return len(packet) == 0 or set(packet) == {'0'}
    
    if is_ending(packet):
        return
    
    version, id = int(packet[:VERSION_ID_SIZE], 2), int(packet[VERSION_ID_SIZE:VERSION_ID_SIZE*2], 2)
    total_versions += version
    
    if id in LITERAL_PACKETS:
        packet = packet[LITERAL_START:]
        value, data = get_value(packet)
        if not is_ending(data):
            total_versions = sum_versions(data, total_versions)
    else:
        length_id = int(packet[LEN_ID_POSITION], 2)
        
        if length_id == LEN_ID_SIZE:
            data = packet[LEN_ID_POSITION + LENGTH_FRAME + 1:]
            if not is_ending(data):
                total_versions = sum_versions(data, total_versions)
        
        elif length_id == LEN_ID_NUMBER:
            data = packet[LEN_ID_POSITION + NUMBER_FRAME + 1:]
            total_versions = sum_versions(data, total_versions)

    return total_versions

def evaluate(ptr, packet, versions=0):   
    parsed = {}
    v, id = int(packet[ptr:ptr+VERSION_ID_SIZE], 2), int(packet[ptr+VERSION_ID_SIZE:ptr+2*VERSION_ID_SIZE], 2)
    
    versions += v

    parsed["op"] = ID_TO_OP[id]
    ptr += HEADER_LENGTH

    if id == LITERAL_PACKET:
        literal = ''
        while int(packet[ptr]):
            literal += packet[ptr+1:ptr+LITERAL_FRAME]
            ptr += LITERAL_FRAME
        literal += packet[ptr+1:ptr+LITERAL_FRAME]
        ptr += LITERAL_FRAME
        parsed["value"] = int(literal, 2)

    else:
        l_id = int(packet[ptr])
        parsed['sub_packets'] = []
        ptr += 1

        if l_id == LEN_ID_NUMBER:
            children_number = int(packet[ptr:ptr + NUMBER_FRAME], 2)
            ptr += NUMBER_FRAME
            for child in range(children_number):
                sub_packet, ptr, versions = evaluate(ptr, packet, versions)
                parsed['sub_packets'].append(sub_packet)
                #recurse no-of-children times and advance ptr
        
        elif l_id == LEN_ID_SIZE:
            data_size = int(packet[ptr:ptr + LENGTH_FRAME], 2)
            ptr += LENGTH_FRAME            
            packet_stop = ptr + data_size
            while ptr < packet_stop:
                sub_packet, ptr, versions = evaluate(ptr, packet, versions)
                parsed['sub_packets'].append(sub_packet)
                #recurse and advance ptr after each recursion
    
        all_sub_values = [sub_pack.get("value") for sub_pack in parsed['sub_packets']]
        all_sub_values = [value for value in all_sub_values if value is not None]
        
        if 0 <= id <= 3:
            parsed["value"] = ID_TO_OP[id](all_sub_values)
        else:
            parsed["value"] = 1 if ID_TO_OP[id](all_sub_values[0], all_sub_values[1]) else 0

    if ptr >= len(packet) - LENGTH_FRAME:
        print(f'An awful way to print total versions: {versions}')
    return parsed, ptr, versions

print('Tests...')
test_packets = [('A0016C880162017C3686B18A3D4780', 54), ('C200B40A82', 3), ('04005AC33890', 54), ('9C0141080250320F1802104A08', 1)]
for packet, result in test_packets:
    print(f'Evaluating test packet {packet}...', evaluate(0, convert_to_bin(packet))[0]['value'] == result)
print('---------------------')

print('Solution...')
with open('inp', mode='r') as inp:
    raw_data = inp.read()
    packet = convert_to_bin(raw_data)
    print(f'Evaluating input...', evaluate(0, packet)[0]['value'])