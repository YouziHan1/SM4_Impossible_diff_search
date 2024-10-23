import DDT_LAT


# 模块使用示例
plaintext = '12'.zfill(32)  # 填充到32字符
s_box = ['d6', '90', 'e9', 'fe', 'cc', 'e1', '3d', 'b7', '16', 'b6', '14', 'c2', '28', 'fb', '2c', '05',
                      '2b', '67', '9a', '76', '2a', 'be', '04', 'c3', 'aa', '44', '13', '26', '49', '86', '06', '99',
                      '9c', '42', '50', 'f4', '91', 'ef', '98', '7a', '33', '54', '0b', '43', 'ed', 'cf', 'ac', '62',
                      'e4', 'b3', '1c', 'a9', 'c9', '08', 'e8', '95', '80', 'df', '94', 'fa', '75', '8f', '3f', 'a6',
                      '47', '07', 'a7', 'fc', 'f3', '73', '17', 'ba', '83', '59', '3c', '19', 'e6', '85', '4f', 'a8',
                      '68', '6b', '81', 'b2', '71', '64', 'da', '8b', 'f8', 'eb', '0f', '4b', '70', '56', '9d', '35',
                      '1e', '24', '0e', '5e', '63', '58', 'd1', 'a2', '25', '22', '7c', '3b', '01', '21', '78', '87',
                      'd4', '00', '46', '57', '9f', 'd3', '27', '52', '4c', '36', '02', 'e7', 'a0', 'c4', 'c8', '9e',
                      'ea', 'bf', '8a', 'd2', '40', 'c7', '38', 'b5', 'a3', 'f7', 'f2', 'ce', 'f9', '61', '15', 'a1',
                      'e0', 'ae', '5d', 'a4', '9b', '34', '1a', '55', 'ad', '93', '32', '30', 'f5', '8c', 'b1', 'e3',
                      '1d', 'f6', 'e2', '2e', '82', '66', 'ca', '60', 'c0', '29', '23', 'ab', '0d', '53', '4e', '6f',
                      'd5', 'db', '37', '45', 'de', 'fd', '8e', '2f', '03', 'ff', '6a', '72', '6d', '6c', '5b', '51',
                      '8d', '1b', 'af', '92', 'bb', 'dd', 'bc', '7f', '11', 'd9', '5c', '41', '1f', '10', '5a', 'd8',
                      '0a', 'c1', '31', '88', 'a5', 'cd', '7b', 'bd', '2d', '74', 'd0', '12', 'b8', 'e5', 'b4', 'b0',
                      '89', '69', '97', '4a', '0c', '96', '77', '7e', '65', 'b9', 'f1', '09', 'c5', '6e', 'c6', '84',
                      '18', 'f0', '7d', 'ec', '3a', 'dc', '4d', '20', '79', 'ee', '5f', '3e', 'd7', 'cb', '39', '48']

        # 系统参数 FK
FK = ['a3b1bac6', '56aa3350', '677d9197', 'b27022dc']

        # 32个固定参数 CK
CK = ['00070e15', '1c232a31', '383f464d', '545b6269',
                   '70777e85', '8c939aa1', 'a8afb6bd', 'c4cbd2d9',
                   'e0e7eef5', 'fc030a11', '181f262d', '343b4249',
                   '50575e65', '6c737a81', '888f969d', 'a4abb2b9',
                   'c0c7ced5', 'dce3eaf1', 'f8ff060d', '141b2229',
                   '30373e45', '4c535a61', '686f767d', '848b9299',
                   'a0a7aeb5', 'bcc3cad1', 'd8dfe6ed', 'f4fb0209',
                   '10171e25', '2c333a41', '484f565d', '646b7279']

main_key = '0123456789abcdeffedcba9876543210'
# 密钥扩展

def shift_to_left(string, num):
    """循环左移"""
    return string[num % len(string):] + string[:num % len(string)]


def x_o_r(string_list):
    """异或"""
    result = 0
    for i in range(len(string_list)):
        result ^= string_list[i]
    return hex(result)[2:].zfill(8)


def Sbox(s_box, row_column):
    """S盒转换"""
    index = int(row_column, 16)
    return s_box[index]



def tal(s_box, A):
    """非线性变换 tal"""
    B = ''
    for i in range(4):
        B += Sbox(s_box, A[i * 2: i * 2 + 2])
    return B


def L(B):
    """线性变换 L"""
    bin_B = bin(int(B, 16))[2:].zfill(32)
    B_shift_2 = shift_to_left(bin_B, 2)
    B_shift_10 = shift_to_left(bin_B, 10)
    B_shift_18 = shift_to_left(bin_B, 18)
    B_shift_24 = shift_to_left(bin_B, 24)
    C = x_o_r([int(bin_B, 2), int(B_shift_2, 2), int(B_shift_10, 2), int(B_shift_18, 2), int(B_shift_24, 2)])
    return C


def L_(B):
    """线性变换 L'"""
    bin_B = bin(int(B, 16))[2:].zfill(32)
    B_shift_13 = shift_to_left(bin_B, 13)
    B_shift_23 = shift_to_left(bin_B, 23)
    C = x_o_r([int(bin_B, 2), int(B_shift_13, 2), int(B_shift_23, 2)])
    return C


def key_extension(MK, FK, CK):
    """密钥扩展算法"""
    K = [''] * 36
    rk = [''] * 32
    T_ = lambda tmp: L_(tal(s_box, tmp))

    for i in range(4):
        K[i] = x_o_r([int(MK[i], 16), int(FK[i], 16)])

    for i in range(32):
        rk[i] = K[i + 4] = x_o_r([int(K[i], 16), int(T_(
            x_o_r([int(K[i + 1], 16), int(K[i + 2], 16), int(K[i + 3], 16), int(CK[i], 16)])), 16)])

    return rk

rk = key_extension([main_key[i * 8: i * 8 + 8] for i in range(4)], FK, CK)

def F(X0, X1, X2, X3, rk):
    """轮函数 F"""
    T = lambda tmp: L(tal(s_box, tmp))
    result = x_o_r([int(X0, 16), int(T(x_o_r([int(X1, 16), int(X2, 16), int(X3, 16), int(rk, 16)])), 16)])
    return result

'''
def encrypt(plaintext, rk):
    """加密"""
    X = [''] * 36
    X[0] = plaintext[0:8]
    X[1] = plaintext[8:16]
    X[2] = plaintext[16:24]
    X[3] = plaintext[24:32]

    for i in range(32):
        X[i + 4] = F(X[i], X[i + 1], X[i + 2], X[i + 3], rk[i])

    ciphertext = ''.join(X[::-1][:4])
    return ciphertext


def decrypt(ciphertext, rk):
    """解密"""
    X = [''] * 36
    X[0] = ciphertext[0:8]
    X[1] = ciphertext[8:16]
    X[2] = ciphertext[16:24]
    X[3] = ciphertext[24:32]

    for i in range(32):
        X[i + 4] = F(X[i], X[i + 1], X[i + 2], X[i + 3], rk[31 - i])

    plaintext = ''.join(X[::-1][:4])
    return plaintext
'''
def encrypt(plaintext, rk,i):
    """加密"""
    X = [''] * 36
    X[0] = plaintext[0:8]
    X[1] = plaintext[8:16]
    X[2] = plaintext[16:24]
    X[3] = plaintext[24:32]


    X[i + 4] = F(X[i], X[i + 1], X[i + 2], X[i + 3], rk[i])

    #ciphertext = ''.join(X[::-1][:4])
    ciphertext=''.join((X[-4:]))
    return ciphertext

def find_s_out_diff(ddt,s_in,ddt_):
    # 找差分分布表最出现概率最高的输出差分

    diff_out=''
    for i in range(3,-1,-1):
        num=int(s_in[i],16)

        max_value=max(ddt[num])

        ddt_.append(max_value)
        # 出现次数最高的对应的列index就是输出差分
        diff_out=diff_out+hex(ddt[num].index(max_value))[2:]
    #return ddt[diff_in].index(max_value),max_value
    return diff_out



table=DDT_LAT.Differential_box
X=['']*9



result={}

# 为了减少活跃S盒个数，输入差分（Δ，0，0，0），Δ=（α，0，0，0），穷举前8bit
for diff_in in range(1,2**8):
    max_ddt = [[], [], [], [], []]
    #diff_in=hex(diff_in)[2:].zfill(32)
    #diff_in=hex(diff_in)[2:].zfill(24)+'0'.zfill(8)
    #diff_in = hex(diff_in)[2:].zfill(16) + '0'.zfill(16)
    diff_in = hex(diff_in)[2:].zfill(8) + '0'.zfill(24)
    #print(diff_in)
    #print(diff_in)
    result[diff_in]=[]
    # 差分分组,第0组输入差分非0其余都为0
    X[0] = diff_in[0:8]
    X[1] = diff_in[8:16]
    X[2] = diff_in[16:24]
    X[3] = diff_in[24:32]


    #==============第一轮==================
    # 获取抑或后过s盒后最大可能的输出差分
    after_xor = x_o_r([int(X[1], 16), int(X[2], 16), int(X[3], 16)])
    # 分组（4*8bit）进入s盒
    s_in = [after_xor[i:i + 2] for i in range(0, len(after_xor), 2)]
    # 要求活跃s盒有一个
    if s_in.count('00') < 3:
        continue
    diff_s = find_s_out_diff(table, s_in,max_ddt[0])

    #for dif1 in diff_s:
    X[4] = x_o_r([int(L(diff_s), 16), int(X[0], 16)])


    #===============第二轮=================
    # 获取抑或后过s盒后最大可能的输出差分
    after_xor1 = x_o_r([int(X[2], 16), int(X[3], 16), int(X[4], 16)])
    # 分组（4*8bit）进入s盒
    s_in1 = [after_xor1[i:i + 2] for i in range(0, len(after_xor1), 2)]
    # 要求活跃s盒有一个
    if s_in1.count('00') < 3:
        # print(s_in1)
        continue

    diff_s1 = find_s_out_diff(table, s_in1,max_ddt[1])
    # for dif2 in diff_s1:
    X[5] = x_o_r([int(L(diff_s1), 16), int(X[1], 16)])
    #print(X[5])


    #==============第三轮==================
    after_xor2 = x_o_r([int(X[3], 16), int(X[4], 16), int(X[5], 16)])

    # 分组（4*8bit）进入s盒
    s_in2 = [after_xor2[i:i + 2] for i in range(0, len(after_xor2), 2)]

    '''
    if s_in2.count('00') < 3:
        continue
    '''
    diff_s2 = find_s_out_diff(table, s_in2,max_ddt[2])

    X[6] = x_o_r([int(L(diff_s2), 16), int(X[2], 16)])


    #=============第四轮====================

    after_xor3 = x_o_r([int(X[4], 16), int(X[5], 16), int(X[6], 16)])
    # 分组（4*8bit）进入s盒
    s_in3 = [after_xor3[i:i + 2] for i in range(0, len(after_xor3), 2)]
    # 要求活跃s盒有一个
    '''
    if s_in3.count('00') < 3:
        continue
    '''
    diff_s3 = find_s_out_diff(table, s_in3,max_ddt[3])

    X[7] = x_o_r([int(L(diff_s3), 16), int(X[3], 16)])


    #===========第五轮===================
    # 获取抑或后过s盒后最大可能的输出差分
    after_xor4 = x_o_r([int(X[5], 16), int(X[6], 16), int(X[7], 16)])
    # 分组（4*8bit）进入s盒
    s_in4 = [after_xor4[i:i + 2] for i in range(0, len(after_xor4), 2)]
    # 要求活跃s盒有一个
    '''
    if s_in4.count('00') < 3:
        continue
    print(s_in4)
    '''

    diff_s4 = find_s_out_diff(table, s_in4,max_ddt[4])
    X[8]=x_o_r([int(L(diff_s4), 16), int(X[4], 16)])


    result[diff_in].append([diff_in,X[1]+X[2]+X[3]+X[4],X[2]+X[3]+X[4]+X[5], X[3]+X[4]+X[5]+X[6], X[4]+X[5]+X[6]+X[7],X[5]+X[6]+X[7]+X[8]])
    print("=========================================================================================")
    print("输入差分为：",diff_in)
    print("找到的差分路线为：",result[diff_in])
    print("概率为：",max_ddt)



















