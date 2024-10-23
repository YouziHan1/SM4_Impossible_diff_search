


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

# def S_box_after(state):












# 0 差分为0
# 1 差分为已知确定值delta
# 2 差分为未知非零值
# 3 差分为delta^某未知非零值
# 4 差分为未知值

#矛盾
#0 {1，2}
#1 {0，2，3}
#2 {0}
#3 {1}
#confict=[[1,2],[0,2,3],[0],[1]]


def xor(a,b):
    if (a==0 and b==0) or (a==1 and b==1):
        return 0
    elif (a==0 and b==1) or (a==1 and b==0):
        return 1
    elif (a==2 and b==0) or (a==0 and b==2)  or (a==1 and b==3) or (a==3 and b==1):
        return 2
    elif (a==2 and b==1) or (a==1 and b==2) or (a==3 and b==0) or (a==0 and b==3) :
        return 3
    else:
        return 4


def xor_in(state):
    result=0
    for i in range(1,len(state)):
        result = xor(state[i],result)
        #print(result)
    return result

def F(result):
    if result == 0:
        output=0
    else:#输入差分不为零则输出差分一定不为零 但是为未知值
        output=2
    return output

def xor_out(state,F_out):
    result=xor(state[0],F_out)
    return result

def encode(state):
    for i in range (32):
        result=xor_out(state,F(xor_in(state)))
        state=state[1:]+[result]
        num=state.count(4)
        if num==4 :
            return True
        print("第", i + 1, "轮:", state)


def decode(state):
    for i in range (32):
        result=xor_out(state[::-1],F(xor_in(state[::-1])))
        state=[result]+state[:3]
        num = state.count(4)
        if num == 4:
            return True
        print("第", 32-i, "轮:", state)


def encode_1(state):
    result_state = []
    for i in range (32):
        result=xor_out(state,F(xor_in(state)))
        state=state[1:]+[result]
        num=state.count(4)
        if num==4 :
            print("加密方向差分路线为：",result_state)
            return result_state,i
        result_state.append(state)
        #print("第", i + 1, "轮:", state)
    return result_state,31



def decode_1(state):
    result_state_rev=[]
    for i in range (32):
        result=xor_out(state[::-1],F(xor_in(state[::-1])))
        state=[result]+state[:3]
        num = state.count(4)
        if num == 4:
            print("解密方向差分路线为：",result_state_rev)
            return result_state_rev,i
        result_state_rev.append(state)
        #print("第", 32-i, "轮:", state)
    return result_state_rev,31


def compare(state_in,state_out,num_in,num_out,conflict):
    round_num=0
    for i in range (4):
        found_conflict =False
        for j in range (num_out-1, -1, -1):
            found_conflict = False
            if state_out[j][i]!=4 :
                num_1=state_out[j][i]

                for k in range (num_in-1, -1, -1):

                    if state_in[k][i] != 4:
                        num_2 = state_in[k][i]

                        if num_2 in conflict[num_1]:
                            if j+1+k+1>=round_num:
                                round_num=j+1+k+1
                            print("第",i+1,"字节找到矛盾：反向第",j+1,"轮与正向第",k+1,"轮，不可能差分长度为",j+1+k+1)
                            found_conflict = True
                    if found_conflict:
                        break
            if found_conflict:
                break
    return round_num



conflict_state=[[1,2],[0,2,3],[0],[1]]

# state111 = [random.choice([0, 1]) for _ in range(4)]
#
# state1=[1,1,1,0]
# state_1,round_num_in=encode_1(state1)
# print(round_num_in)
# state2=[1,1,1,0]
# state_2,round_num_out=decode_1(state2)
#
# print(round_num_out)


# compare(state_1,state_2,round_num_in,round_num_out,conflict_state)

round_num=0
for i in range(1,16):
    state_in_ = [int(bit) for bit in f"{i:04b}"]
    for j in range(1,16):
        state_out_ = [int(bit) for bit in f"{j:04b}"]
        #print("输入差分为：",state_in_, " 输出差分为：",state_out_)
        state_1, round_num_in = encode_1(state_in_)
        state_2, round_num_out = decode_1(state_out_)
        temp=compare(state_1, state_2, round_num_in, round_num_out,conflict_state)
        if temp>round_num:
            round_num=temp
            result_input=state_in_
            result_output=state_out_
print("===============================================================================================")
print("最长轮数的不可能差分路线有",round_num,"轮")
print("此时输入差分为",result_input,"输出差分为",result_output)
state_1, round_num_in = encode_1(result_input)
state_2, round_num_out = decode_1(result_output)
compare(state_1, state_2, round_num_in, round_num_out,conflict_state)