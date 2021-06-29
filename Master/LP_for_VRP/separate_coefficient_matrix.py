import numpy as np
def separate(As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq, op, oq, threshold):
    # 制約式の係数行列、右辺ベクトルを分ける
    As_1, Ac_eq_1, Ac_leq_1, Ar_eq_1, Ar_leq_1, Ap_1, Aq_1, b_eq_1, b_leq_1, op_1, oq_1\
        = [], [], [], [], [], [], [], [], [], [], []
    As_2, Ac_eq_2, Ac_leq_2, Ar_eq_2, Ar_leq_2, Ap_2, Aq_2, b_eq_2, b_leq_2, op_2, oq_2\
        = [], [], [], [], [], [], [], [], [], [], []
    As_3, Ac_eq_3, Ac_leq_3, Ar_eq_3, Ar_leq_3, Ap_3, Aq_3, b_eq_3, b_leq_3, op_3, oq_3\
        = [], [], [], [], [], [], [], [], [], [], []
    index = 0
    index_P_f_eq, index_P_f_leq = [], []
    index_P_l_eq, index_P_l_leq = [], []
    for As_i, Ac_leq_i, Ar_leq_i, Ap_i, Aq_i, b_leq_i in zip(As, Ac_leq, Ar_leq, Ap, Aq, b_leq):
        if np.linalg.norm(As_i[threshold:], ord=2)==0.:
            As_1.append(As_i[:threshold])
            Ac_leq_1.append(Ac_leq_i[:threshold])
            Ar_leq_1.append(Ar_leq_i[:threshold])
            Ap_1.append(Ap_i[:threshold])
            Aq_1.append(Aq_i[:threshold])
            b_leq_1.append(b_leq_i)
            index_P_f_leq.append(index)
        elif np.linalg.norm(As_i[:threshold], ord=2)==0.:
            As_2.append(As_i[threshold:])
            Ac_leq_2.append(Ac_leq_i[threshold:])
            Ar_leq_2.append(Ar_leq_i[threshold:])
            Ap_2.append(Ap_i[threshold:])
            Aq_2.append(Aq_i[threshold:])
            b_leq_2.append(b_leq_i)
            index_P_l_leq.append(index)
        else:
            As_3.append(As_i[:threshold])
            Ac_leq_3.append(Ac_leq_i[:threshold])
            Ar_leq_3.append(Ar_leq_i[:threshold])
            Ap_3.append(Ap_i[:threshold])
            Aq_3.append(Aq_i[:threshold])
            b_leq_3.append(b_leq_i)
        index += 1

    index = 0
    for Ac_eq_i, Ar_eq_i, b_eq_i in zip(Ac_eq, Ar_eq, b_eq):
        if np.linalg.norm(Ac_eq_i[threshold:], ord=2)==0.:
            Ac_eq_1.append(Ac_eq_i[:threshold])
            Ar_eq_1.append(Ar_eq_i[:threshold])
            b_eq_1.append(b_eq_i)
            index_P_f_eq.append(index)
        elif np.linalg.norm(As_i[:threshold], ord=2)==0.:
            Ac_eq_2.append(Ac_eq_i[threshold:])
            Ar_eq_2.append(Ar_eq_i[threshold:])
            b_eq_2.append(b_eq_i)
            index_P_l_eq.append(index)
        else:
            Ac_eq_3.append(Ac_eq_i[:threshold])
            Ar_eq_3.append(Ar_eq_i[:threshold])
            b_eq_3.append(b_eq_i)
        index += 1

    # 目的関数の係数ベクトルを定める
    op_1 = op[:threshold]
    op_2 = op[threshold:]
    oq_1 = oq[:threshold]
    oq_2 = oq[threshold:]

    # リストからnumpy arrayに変換
    As_1 = np.array(As_1)
    Ac_eq_1 = np.array(Ac_eq_1)
    Ac_leq_1 = np.array(Ac_leq_1)
    Ar_eq_1 = np.array(Ar_eq_1)
    Ar_leq_1 = np.array(Ar_leq_1)
    Ap_1 = np.array(Ap_1)
    Aq_1 = np.array(Aq_1)
    b_eq_1 = np.array(b_eq_1)
    b_leq_1 = np.array(b_leq_1)
    op_1 = np.array(op_1)
    oq_1 = np.array(oq_1)

    As_2 = np.array(As_2)
    Ac_eq_2 = np.array(Ac_eq_2)
    Ac_leq_2 = np.array(Ac_leq_2)
    Ar_eq_2 = np.array(Ar_eq_2)
    Ar_leq_2 = np.array(Ar_leq_2)
    Ap_2 = np.array(Ap_2)
    Aq_2 = np.array(Aq_2)
    b_eq_2 = np.array(b_eq_2)
    b_leq_2 = np.array(b_leq_2)
    op_2 = np.array(op_2)
    oq_2 = np.array(oq_2)
    return As_1, Ac_eq_1, Ac_leq_1, Ar_eq_1, Ar_leq_1, Ap_1, Aq_1, b_eq_1, b_leq_1, op_1, oq_1, As_2, Ac_eq_2, Ac_leq_2, Ar_eq_2, Ar_leq_2, Ap_2, Aq_2, b_eq_2, b_leq_2, op_2, oq_2, index_P_f_eq, index_P_f_leq, index_P_l_eq, index_P_l_leq