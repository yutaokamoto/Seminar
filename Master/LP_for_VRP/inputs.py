def distance(x1, y1, x2, y2):
    return ((x2-x1)**2+(y2-y1)**2)**(0.5)

def make_preceding_constr(tour, Customers, Points, As, Ac_leq, Ar_leq, Ap, Aq, b_leq):
    # ルート内の顧客の順序に関する制約
    for index, i in enumerate(tour):
        try:
            i_next = tour[index+1]
        except:
            break
        As.append([1 if target==i else -1 if target==i_next else 0 for target in tour])
        Ac_leq.append([1 if target==i else 0 for target in tour])
        b_leq.append(-distance(Customers[i].x, Customers[i].y, Customers[i_next].x, Customers[i_next].y))
        ## 以下はすべての行列のサイズを合わせるために行を追加している
        Ar_leq.append([0 for target in tour])
        Ap.append([0 for target in tour])
        Aq.append([0 for target in tour])
    return As, Ac_leq, Ar_leq, Ap, Aq, b_leq

def make_tw_constr(tour, Customers, Points, As, Ac_leq, Ar_leq, Ap, Aq, b_leq):
    # 時間枠制約
    for index, i in enumerate(tour):
        As.append([-1 if i==target else 0 for target in tour])
        Ap.append([-1 if i==target else 0 for target in tour])
        b_leq.append(-Customers[i].e)
        As.append([1 if i==target else 0 for target in tour])
        Ap.append([-1 if i==target else 0 for target in tour])
        b_leq.append(Customers[i].l)
        ## 以下はすべての行列のサイズを合わせるために行を追加している
        for _ in range(2):
            Ac_leq.append([0 for target in tour])
            Ar_leq.append([0 for target in tour])
            Aq.append([0 for target in tour])
    return As, Ac_leq, Ar_leq, Ap, Aq, b_leq

def make_nonnega_constr(tour, Points, As, Ac_leq, Ar_leq, Ap, Aq, b_leq):
    # 変数の非負制約
    for index, i in enumerate(tour):
        As.append([-1 if i==target else 0 for index_, target in enumerate(tour)])
        Ac_leq.append([-1 if i==target else 0 for index_, target in enumerate(tour)])
        Ar_leq.append([-1 if i==target else 0 for index_, target in enumerate(tour)])
        Ap.append([-1 if i==target else 0 for index_, target in enumerate(tour)])
        Aq.append([-1 if i==target else 0 for index_, target in enumerate(tour)])
        b_leq.append(0)
    return As, Ac_leq, Ar_leq, Ap, Aq, b_leq

def make_time_limit_constr(tour, Customers, Points, As, Ac_leq, Ar_leq, Ap, Aq, b_leq):
    # ピックアップからデリバリーまでの時間制限に関する制約
    for index, pair in enumerate(Points):
        p = pair[0]
        d = pair[1]
        As.append([-1 if target==p else 1 if target==d else 0 for target in tour])
        Aq.append([-1 if target==p else 0 for target in tour])
        b_leq.append(Customers[p].t)
        ## 以下はすべての行列のサイズを合わせるために行を追加している
        Ac_leq.append([0 for target in tour])
        Ar_leq.append([0 for target in tour])
        Ap.append([0 for target in tour])
    return As, Ac_leq, Ar_leq, Ap, Aq, b_leq

def make_charge_constr(tour, Customers, Points, As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq, F, C):
    # 自動車の燃料を補充することに関する制約
    for i in tour:
        Ac_leq.append([1 if i==target else 0 for target in tour])
        Ar_leq.append([1 if i==target else 0 for target in tour])
        b_leq.append(C)
        ## 以下はすべての行列のサイズを合わせるために行を追加している
        As.append([0 for target in tour])
        Ap.append([0 for target in tour])
        Aq.append([0 for target in tour])
        if i==0:
            Ar_eq.append([1] + [0 for j in range(len(tour)-1)])
            b_eq.append(F)
            ## 以下はすべての行列のサイズを合わせるために行を追加している
            Ac_eq.append([0 for target in tour])
        else:
            if i=="depot":
                i_prev = tour[-1]
            else:
                i_prev = i-1
            Ac_eq.append([-1 if i_prev==target else 0 for target in tour])
            Ar_eq.append([1 if i==target else -1 if i_prev==target else 0 for target in tour])
            b_eq.append(-0.1*distance(Customers[i].x, Customers[i].y, Customers[i_prev].x, Customers[i_prev].y))
    return As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq

def make_inputs(tour, Customers, Points, F, C):
    import numpy as np
    As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq, op, oq \
        = [], [], [], [], [], [], [], [], [], [1 for _ in range(len(tour))], [1 for _ in range(len(tour))]
    
    # ルート内の顧客の順序に関する制約
    ##As, Ac_leq, b_leq = make_preceding_constr(tour, Customers, As, Ac_leq, b_leq)
    As, Ac_leq, Ar_leq, Ap, Aq, b_leq = make_preceding_constr(tour, Customers, Points, As, Ac_leq, Ar_leq, Ap, Aq, b_leq)
    print("Preceding constraints are done.")
    
    # 時間枠制約
    ##As, Ap, b_leq = make_tw_constr(tour, Customers, As, Ap, b_leq)
    As, Ac_leq, Ar_leq, Ap, Aq, b_leq = make_tw_constr(tour, Customers, Points, As, Ac_leq, Ar_leq, Ap, Aq, b_leq)
    print("Time-window constarints are done.")
    
    # 非負制約
    ##As, Ac_leq, Ar_leq, Ap, Aq, b_eq = make_nonnega_constr(tour, Points, As, Ac_leq, Ar_leq, Ap, Aq, b_leq)
    ##print("Non-negative constarints are done.")
    
    # ピックアップからデリバリーまでの時間制限に関する制約
    #As, Aq, b_leq = time_limit_constr(tour, Customers, Points, As, Aq, b_leq)
    As, Ac_leq, Ar_leq, Ap, Aq, b_leq = make_time_limit_constr(tour, Customers, Points, As, Ac_leq, Ar_leq, Ap, Aq, b_leq)
    print("Pick-up and delivery constarints are done.")
    
    # 自動車の燃料を補充することに関する制約
    #Ac_eq, Ac_leq, Ar_eq, Ar_leq, b_eq, b_leq = charge_constr(tour, Ac_eq, Ac_leq, Ar_eq, Ar_leq, b_eq, b_leq, F, C)
    As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq = make_charge_constr(tour, Customers, Points, As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq, F, C)
    print("Charge constarints are done.")
    
    # ndarrayに変換
    As = np.array(As)
    Ac_eq = np.array(Ac_eq)
    Ac_leq = np.array(Ac_leq)
    Ar_eq = np.array(Ar_eq)
    Ar_leq = np.array(Ar_leq)
    Ap = np.array(Ap)
    Aq = np.array(Aq)
    b_eq = np.array(b_eq)
    b_leq = np.array(b_leq)
    op = np.array(op)
    oq = np.array(oq)
    return As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq, op, oq