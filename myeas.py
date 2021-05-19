import string
from copy import copy

def input_single_block():
    text = input("Enter text: ")
    key = input("Enter key: ")
    text = text[:16]
    key = key[:16]
    
    if len(text) < 16:
        for i in range(len(text) - 1, 15):
            text+="0";
    if len(key) < 16:
        for i in range(len(key) - 1, 15):
            key+="0";
    return text, key
    

'''def convert_to_table(text):
    table = []
    for i in range(4):
        table.append([]);
        for j in range(4):
            table[i].append('0');
    for i in range(4):
        for j in range(4):
            table[i][j] = text[i + 4*j];
    return table;

def print_state(state):
    for i in range(4):
        for j in range(4):
            print(state[i][j], end=' ')
        print()'''

Rcon = [
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x04, 0x00, 0x00, 0x00],
        [0x08, 0x00, 0x00, 0x00],
        [0x10, 0x00, 0x00, 0x00],
        [0x20, 0x00, 0x00, 0x00],
        [0x40, 0x00, 0x00, 0x00],
        [0x80, 0x00, 0x00, 0x00],
        [0x1b, 0x00, 0x00, 0x00],
        [0x36, 0x00, 0x00, 0x00]
]

sbox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]
sboxInv = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

def subBytes(state):
    for i in range(len(state)):
        state[i] = sbox[state[i]]
    return state

def subBytesInv(state):
    for i in range(len(state)):
        state[i] = sboxInv[state[i]]
    return state

def swap(i1, i2, state):
    tmp = state[i1]
    state[i1] = state[i2]
    state[i2] = tmp

def shiftRows(state):
    '''swap(4, 7, state);
    swap(4, 5, state);
    swap(5, 6, state);'''
    swap(4, 5, state)
    swap(5, 6, state)
    swap(6, 7, state)

    swap(8, 10, state)
    swap(9, 11, state)

    '''swap(12, 15, state)
    swap(13, 15, state)
    swap(14, 15, state)'''
    swap(14, 15, state);
    swap(13, 14, state);
    swap(12, 13, state);

def shiftRowsInv(state):
    '''swap(4, 7, state)
    swap(6, 7, state)
    swap(5, 6, state)'''
    swap(6, 7, state)
    swap(5, 6, state)
    swap(4, 5, state)

    swap(8, 10, state)
    swap(9, 11, state)

    '''swap(12, 15, state)
    swap(12, 14, state)
    swap(12, 13, state)'''
    swap(12, 13, state);
    swap(13, 14, state);
    swap(14, 15, state);

def addRoundKey(state, roundKey):
    for i in range(len(state)):
        state[i] = state[i]^roundKey[i]

def galuaMultipy(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256

def mixColumn(state, i, tmp):
    i1 = i
    i2 = i + 4
    i3 = i + 4*2
    i4 = i + 4*3
    state[i1] = galuaMultipy(tmp[i1], 2)^galuaMultipy(tmp[i2], 3)^galuaMultipy(tmp[i3], 1)^galuaMultipy(tmp[i4], 1)
    state[i2] = galuaMultipy(tmp[i1], 1)^galuaMultipy(tmp[i2], 2)^galuaMultipy(tmp[i3], 3)^galuaMultipy(tmp[i4], 1)
    state[i3] = galuaMultipy(tmp[i1], 1)^galuaMultipy(tmp[i2], 1)^galuaMultipy(tmp[i3], 2)^galuaMultipy(tmp[i4], 3)
    state[i4] = galuaMultipy(tmp[i1], 3)^galuaMultipy(tmp[i2], 1)^galuaMultipy(tmp[i3], 1)^galuaMultipy(tmp[i4], 2)

def mixColumns(state):
    tmp = copy(state)
    for i in range(4):
        mixColumn(state, i, tmp)

def mixColumnInv(state, i, tmp):
    i1 = i
    i2 = i + 4
    i3 = i + 4*2
    i4 = i + 4*3
    state[i1] = galuaMultipy(tmp[i1], 14)^galuaMultipy(tmp[i2], 11)^galuaMultipy(tmp[i3], 13)^galuaMultipy(tmp[i4], 9)
    state[i2] = galuaMultipy(tmp[i1], 9)^galuaMultipy(tmp[i2], 14)^galuaMultipy(tmp[i3], 11)^galuaMultipy(tmp[i4], 13)
    state[i3] = galuaMultipy(tmp[i1], 13)^galuaMultipy(tmp[i2], 9)^galuaMultipy(tmp[i3], 14)^galuaMultipy(tmp[i4], 11)
    state[i4] = galuaMultipy(tmp[i1], 11)^galuaMultipy(tmp[i2], 13)^galuaMultipy(tmp[i3], 9)^galuaMultipy(tmp[i4], 14)

def mixColumnsInv(state):
    tmp = copy(state)
    for i in range(4):
        mixColumnInv(state, i, tmp)

def cypherRound(state, round_key):
    subBytes(state)
    shiftRows(state)
    mixColumns(state)
    addRoundKey(state, round_key)

def cypherRoundInv(state, round_key):
    addRoundKey(state, round_key)
    mixColumnsInv(state)
    shiftRowsInv(state)
    subBytesInv(state)

def encryptBlock(block, key_scedule):
    state = block
    addRoundKey(state, key_scedule[0])
    for i in range(1, 10):
        cypherRound(state, key_scedule[i])
    subBytes(state)
    shiftRows(state)
    addRoundKey(state, key_scedule[10])
    return state

def decryptBlock(block, key_scedule):
    state = block
    addRoundKey(state, key_scedule[10]) 
    shiftRowsInv(state)
    subBytesInv(state)
    i = 9
    while i >= 1:
        cypherRoundInv(state, key_scedule[i])
        i-=1
    addRoundKey(state, key_scedule[0])
    return state

'''================================key scedule======================================'''
def getNewFirstColumn(key, roundx):
    new_column = []
    for i in range(len(key)):
        if i%4 == 3:
            new_column.append(key[i])
    swap(0, 1, new_column)
    swap(1, 2, new_column)
    swap(2, 3, new_column)
    new_culumn = subBytes(new_column)
    first_column = []
    for i in range(len(key)):
        if i%4 == 0:
            first_column.append(key[i])
    for i in range(len(new_column)):
        new_column[i] ^= first_column[i];
    for i in range(len(new_column)):
        new_column[i] ^= Rcon[roundx][i]
    return new_column

def getRoundKey(key, roundx):
    new_column = getNewFirstColumn(key, roundx);
    new_key = [0]*16
    for i in range(len(new_key)):
        if i%4 == 0:
            new_key[i] = new_column[int(i/4)]
        else:
            new_key[i] = key[i]^new_key[i-1]
    return new_key    

def makeKeyScedule(key):
    key_scedule = [0]*11
    key_scedule[0] = key;
    for i in range(1, 11):
        key_scedule[i] = getRoundKey(key_scedule[i-1], i-1)
    return key_scedule
'''================================key scedule======================================'''

def rearrange(inp):
    new_input = [0]*16
    k = 0
    for i in range(0, 4):
        for j in range(i, 16, 4):
            new_input[j] = inp[k]
            k+=1
    return new_input

def rearrange_inv(inp):
    new_input = [0]*16
    k = 0
    for i in range(0, 4):
        for j in range(i, 16, 4):
            new_input[k] = inp[j]
            k+=1
    #print(new_input)
    return new_input

def get_blocks(text):
    size = len(text)//16;
    if len(text) % 16 != 0:
        size += 1
    blocks = []
    for i in range(size):
        blocks.append([])
    index = 0
    for i in range(len(text)):
        blocks[index].append(text[i]);
        if i % 16 == 15:
            index += 1;
    skoka = 0
    if len(blocks[size - 1]) < 16:
        for i in range(len(blocks[size - 1]), 16):
            blocks[size - 1].append(0)
            #skoka += 1
    return blocks

def get_text(blocks):
    a = []
    for item in blocks:
        a += item
    #a = bytes(a)
    return a

def text_to_blocks(text):
    text_list_b = list(bytes(text, 'latin-1'))
    blocks = get_blocks(text_list_b)
    for i in range(len(blocks)):
        blocks[i] = rearrange(blocks[i])
    return blocks

def text_to_blocks_inv(blocks):
    for i in range(len(blocks)):
        blocks[i] = rearrange_inv(blocks[i])
    text_list_b = get_text(blocks)
    for i in range(len(text_list_b)):
        text_list_b[i] = chr(text_list_b[i])
    #text = text_list_b.decode('ascii')
    text = ''.join(text_list_b)
    return text

def key_to_keyscedule(key):
    key = list(bytes(key, 'latin-1'))
    key = rearrange(key)
    key_scedule = makeKeyScedule(key)
    return key_scedule

def encrypt_ECB(text, key):
    blocks = text_to_blocks(text)
    key_scedule = key_to_keyscedule(key)
    for i in range(len(blocks)):
        blocks[i] = encryptBlock(blocks[i], key_scedule)
    cyphertext = text_to_blocks_inv(blocks)
    return cyphertext
    

def decrypt_ECB(text, key):
    blocks = text_to_blocks(text)
    key_scedule = key_to_keyscedule(key)
    for i in range(len(blocks)):
        blocks[i] = decryptBlock(blocks[i], key_scedule)
    text = text_to_blocks_inv(blocks)
    return text

def encrypt_CBC(text, key, init_vector):
    blocks = text_to_blocks(text)
    key_scedule = key_to_keyscedule(key)
    init_vector = list(bytes(init_vector, 'latin-1'))
    init_vector = rearrange(init_vector)
    for i in range(len(blocks)):
        if i == 0:
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j]^init_vector[j]
        else:
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j]^blocks[i-1][j]      
        blocks[i] = encryptBlock(blocks[i], key_scedule)
    cyphertext = text_to_blocks_inv(blocks)
    return cyphertext

def decrypt_CBC(text, key, init_vector):
    blocks = text_to_blocks(text)
    key_scedule = key_to_keyscedule(key)
    init_vector = list(bytes(init_vector, 'latin-1'))
    init_vector = rearrange(init_vector)
    for i in range(len(blocks)):
        blocks[i] = decryptBlock(blocks[i], key_scedule)
        if i == 0:
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j]^init_vector[j]
        else:
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j]^blocks[i-1][j]
    cyphertext = text_to_blocks_inv(blocks)
    return cyphertext        

def OFB(text, key, init_vector):
    blocks = text_to_blocks(text)
    key_scedule = key_to_keyscedule(key)
    init_vector = list(bytes(init_vector, 'latin-1'))
    init_vector = rearrange(init_vector)
    for i in range(len(blocks)):
        init_vector = encryptBlock(init_vector, key_scedule)
        for j in range(len(blocks[i])):
            blocks[i][j] = blocks[i][j]^init_vector[j]
    cyphertext = text_to_blocks_inv(blocks)
    return cyphertext

def encrypt_CFB(text, key, init_vector):
    blocks = text_to_blocks(text)
    key_scedule = key_to_keyscedule(key)
    init_vector = list(bytes(init_vector, 'latin-1'))
    init_vector = rearrange(init_vector)#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    for i in range(len(blocks)):
        if i == 0:
            init_vector = encryptBlock(init_vector, key_scedule)
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j] ^ init_vector[j]
        else:
            tmp = copy(blocks[i-1])
            tmp_cypher = encryptBlock(tmp, key_scedule)
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j] ^ tmp_cypher[j]
    cyphertext = text_to_blocks_inv(blocks)
    return cyphertext

def decrypt_CFB(text, key, init_vector):
    blocks = text_to_blocks(text)
    key_scedule = key_to_keyscedule(key)
    init_vector = list(bytes(init_vector, 'latin-1'))
    init_vector = rearrange(init_vector)
    for i in range(len(blocks)):
        if i == 0:
            init_vector = encryptBlock(init_vector, key_scedule)
            tmp = copy(blocks[i])
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j] ^ init_vector[j]
        else:
            #tmp = copy(blocks[i-1])
            tmp_cypher = encryptBlock(tmp, key_scedule)
            tmp = copy(blocks[i])
            for j in range(len(blocks[i])):
                blocks[i][j] = blocks[i][j] ^ tmp_cypher[j]
    cyphertext = text_to_blocks_inv(blocks)
    return cyphertext


def main():
    text = input()
    key = input()
    init_vector = input()
    iv = init_vector
    #cyphertext = encrypt_ECB(text, key)
    #print(cyphertext)
    #text = decrypt_ECB(cyphertext, key)
    print(text)
    cyphertext = encrypt_CFB(text, key, init_vector)
    print(cyphertext)
    text = decrypt_CFB(cyphertext, key, init_vector)
    print(text)
   # text = OFB(cyphertext, key, init_vector)
    #print(text)
    #print(text)
    #print(cyphertext)
    #decrytext = decrypt_ECB(cyphertext, key)
    #print(decrytext)

main()
















