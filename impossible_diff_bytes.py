# 0 差分为0
# 1 差分为已知确定值delta
# 2 差分为未知非零值
# 3 差分为delta^某未知非零值     可能等于0
# 4 差分为未知值

#矛盾
#0 {1，2}
#1 {0，2，3}
#2 {0}
#3 {1}
#confict=[[1,2],[0,2,3],[0],[1]]




def xor(a,b):
    result=[]
    for i in range(len(a)):
        if (a[i]==0 and b[i]==0) or (a[i]==1 and b[i]==1):
           result.append(0)
        elif (a[i]==0 and b[i]==1) or (a[i]==1 and b[i]==0):
            result.append(1)
        elif (a[i]==2 and b[i]==0) or (a[i]==0 and b[i]==2)  or (a[i]==1 and b[i]==3) or (a[i]==3 and b[i]==1):
            result.append(2)
        elif (a[i]==2 and b[i]==1) or (a[i]==1 and b[i]==2) or (a[i]==3 and b[i]==0) or (a[i]==0 and b[i]==3) :
            result.append(3)
        else:
            result.append(4)
    return result #[x,x,x,x]


def xor_in(state):
    out=[0,0,0,0]
    for i in range(1,len(state)):
        out = xor(state[i],out)
    return out #=[x,x,x,x]

def S_box_diff(state):
    output=[]
    for i in range(len(state)):
        if state[i]==0:
            output.append(0)
        elif state[i]==1:
            output.append(1)
        elif state[i]==2:
            output.append(2)
        else:
            output.append(4)
    return output

def L_diff(state):
    output=[]
    # 左移2bit
    output1 = []
    for i in range(len(state)):
        if state[i]==0 and state[(i+1)%4]==0:
            output1.append(0)
        else:
            output1.append(4)
    output.append(output1)
    # 左移10bit
    output2 = []
    state2=state[1:]+[state[0]]
    for i in range(len(state2)):
        if state[i] == 0 and state[(i + 1) % 4] == 0:
            output2.append(0)
        else:
            output2.append(4)
    output.append(output2)
    # 左移18bit
    output3 = []
    state3 = state[2:] + state[:2]
    for i in range(len(state3)):
        if state[i] == 0 and state[(i + 1) % 4] == 0:
            output3.append(0)
        else:
            output3.append(4)
    output.append(output3)
    # 左移24bit
    output4=[state[3]]+state[0:3]
    output.append(output4)
    res=state
    for i in range(len(output)):
        res=xor(output[i],res)
    return res #[x,x,x,x]


def encode_1(state):
    result_state = []
    for i in range (32):

        result=xor(state,L_diff(S_box_diff(xor_in(state))))
        state=state[1:]
        state.extend([result])
        #print("state:",state)
        num=0
        for j in range(len(state)):
            #rint(state[i])
            num+=state[j].count(4)
        if num==16 :
            print("加密方向差分路线为：",result_state)
            return result_state,i
        result_state.append(state)
        print("第", i + 1, "轮:", state)
    return result_state,31


#字节级 16字节 128bits
state=[[1,1,1,1],[1,1,1,1],[1,1,1,1],[0,0,0,0]]
encode_1(state)
# def decode_1(state):
#     result_state_rev=[]
#     for i in range (32):
#         result=xor_out(state[::-1],F(xor_in(state[::-1])))
#         state=[result]+state[:3]
#         num = state.count(4)
#         if num == 4:
#             print("解密方向差分路线为：",result_state_rev)
#             return result_state_rev,i
#         result_state_rev.append(state)
#         #print("第", 32-i, "轮:", state)
#     return result_state_rev,31
#
#
#
#
#
#
#
# #
# #
# #
# # def F(result):
# #     if result == 0:
# #         output=0
# #     else:#输入差分不为零则输出差分一定不为零 但是为未知值
# #         output=2
# #     return output
#
# # def xor_out(state,F_out):
# #     result=xor(state[0],F_out)
# #     return result
# # #
# # # def encode(state):
# # #     for i in range (32):
# # #         result=xor_out(state,F(xor_in(state)))
# # #         state=state[1:]+[result]
# # #         num=state.count(4)
# # #         if num==4 :
# # #             return True
# # #         print("第", i + 1, "轮:", state)
# #
# #
# # def decode(state):
# #     for i in range (32):
# #         result=xor_out(state[::-1],F(xor_in(state[::-1])))
# #         state=[result]+state[:3]
# #         num = state.count(4)
# #         if num == 4:
# #             return True
# #         print("第", 32-i, "轮:", state)
# #
# #
# # def encode_1(state):
# #     result_state = []
# #     for i in range (32):
# #         result=xor_out(state,F(xor_in(state)))
# #         state=state[1:]+[result]
# #         num=state.count(4)
# #         if num==4 :
# #             print("加密方向差分路线为：",result_state)
# #             return result_state,i
# #         result_state.append(state)
# #         #print("第", i + 1, "轮:", state)
# #     return result_state,31
# #
# #
# #
# # def decode_1(state):
# #     result_state_rev=[]
# #     for i in range (32):
# #         result=xor_out(state[::-1],F(xor_in(state[::-1])))
# #         state=[result]+state[:3]
# #         num = state.count(4)
# #         if num == 4:
# #             print("解密方向差分路线为：",result_state_rev)
# #             return result_state_rev,i
# #         result_state_rev.append(state)
# #         #print("第", 32-i, "轮:", state)
# #     return result_state_rev,31
#
#
# def compare(state_in,state_out,num_in,num_out,conflict):
#     round_num=0
#     for i in range (4):
#         found_conflict =False
#         for j in range (num_out-1, -1, -1):
#             found_conflict = False
#             if state_out[j][i]!=4 :
#                 num_1=state_out[j][i]
#
#                 for k in range (num_in-1, -1, -1):
#
#                     if state_in[k][i] != 4:
#                         num_2 = state_in[k][i]
#
#                         if num_2 in conflict[num_1]:
#                             if j+1+k+1>=round_num:
#                                 round_num=j+1+k+1
#                             print("第",i+1,"字节找到矛盾：反向第",j+1,"轮与正向第",k+1,"轮，不可能差分长度为",j+1+k+1)
#                             found_conflict = True
#                     if found_conflict:
#                         break
#             if found_conflict:
#                 break
#     return round_num
#
#
#
# conflict_state=[[1,2],[0,2,3],[0],[1]]
#
# # state111 = [random.choice([0, 1]) for _ in range(4)]
# #
# # state1=[1,1,1,0]
# # state_1,round_num_in=encode_1(state1)
# # print(round_num_in)
# # state2=[1,1,1,0]
# # state_2,round_num_out=decode_1(state2)
# #
# # print(round_num_out)
#
#
# # compare(state_1,state_2,round_num_in,round_num_out,conflict_state)
#
# round_num=0
# for input in range(1,16):
#     state_in_ = [int(bit) for bit in f"{input:04b}"]
#     for output in range(1,16):
#         state_out_ = [int(bit) for bit in f"{output:04b}"]
#         #print("输入差分为：",state_in_, " 输出差分为：",state_out_)
#         state_1, round_num_in = encode_1(state_in_)
#         state_2, round_num_out = decode_1(state_out_)
#         temp=compare(state_1, state_2, round_num_in, round_num_out,conflict_state)
#         if temp>round_num:
#             round_num=temp
#             result_input=state_in_
#             result_output=state_out_
# print("===============================================================================================")
# print("最长轮数的不可能差分路线有",round_num,"轮")
# print("此时输入差分为",result_input,"输出差分为",result_output)
# state_1, round_num_in = encode_1(result_input)
# state_2, round_num_out = decode_1(result_output)
# compare(state_1, state_2, round_num_in, round_num_out,conflict_state)