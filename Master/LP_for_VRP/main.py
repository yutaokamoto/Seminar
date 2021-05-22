#!/usr/bin/env python
# coding: utf-8

# # ルートを評価するために解くLPについて
# - ルートが1つ与えられた後、そのルートを評価するためにLPを解く(ルートが実行可能であるとは限らない)
# 
# <!--- 各制約の違反度を変数とし、それらに重みをかけて足し合わせた関数の最小化問題とする-->
# - 車両が各顧客へ到着する時刻を変数とし、その合計を最小化する問題とする
# - 制約は、容量制約と時間枠制約とする
#     - 容量制約は、ある区間における2つの関数の積分値(面積)の大小を比較するという形で表す(車両の積荷の量を表す区分線形関数の\[x0, xn\]までの積分値と最大容量を表す線形関数の\[x0, xn\]までの積分値)
#     - 時間枠制約は、通常のVRPの定式化と同様に表す
# 

# # 前準備

# ## instances.pyからインスタンスを得る

# In[1]:


import instances
Customers = instances.Customers
tour = instances.tour


# In[2]:


instance_name = "C" + str(len(Customers)-1)


# # 問題を解く
# 2つの手法に対し、計算時間を比較

# ## 入力する行列、ベクトルの作成

# In[5]:


def distance(x1, y1, x2, y2):
    return ((x2-x1)**2+(y2-y1)**2)**(0.5)


# In[6]:


def make_preceding_constr(tour, Customers, Ax, Ap, b, c):
    # ルート内の顧客の順序に関する制約
    for index, i in enumerate(tour):
        try:
            i_next = tour[index+1]
        except:
            i_next = "depot"
            continue
        Ax.append([1 if target==i else -1 if target==i_next else 0 for target in tour])
        Ap.append([0 for _ in range(len(tour))])
        b.append(-distance(Customers[i].x, Customers[i].y, Customers[i_next].x, Customers[i_next].y))
    return Ax, Ap, b, c


# In[7]:


def make_tw_constr(tour, Customers, Ax, Ap, b, c):
    # 時間枠制約
    for index, i in enumerate(tour):
        Ax.append([-1 if i==target else 0 for index_, target in enumerate(tour)])
        Ap.append([-1 if i==target else 0 for index_, target in enumerate(tour)])
        b.append(-Customers[i].e)
        Ax.append([1 if i==target else 0 for index_, target in enumerate(tour)])
        Ap.append([-1 if i==target else 0 for index_, target in enumerate(tour)])
        b.append(Customers[i].l)
    return Ax, Ap, b, c


# In[8]:


def make_inputs(tour, Customers):
    import numpy as np
    Ax, Ap, b, c = [], [], [], [1 for _ in range(len(tour))]
    # ルート内の顧客の順序に関する制約
    Ax, Ap, b, c = make_preceding_constr(tour, Customers, Ax, Ap, b, c)
    print("Preceding constraints are done.")
    # 時間枠制約
    Ax, Ap, b, c = make_tw_constr(tour, Customers, Ax, Ap, b, c)
    print("Time-window constarints are done.")
    # ndarrayに変換
    Ax = np.array(Ax)
    Ap = np.array(Ap)
    b = np.array(b)
    c = np.array(c)
    return Ax, Ap, b, c


# ## 主問題を解く関数の定義
# 与えられた定数を元にLPのモデルを作成した上でそれを解き、最適解を返す関数

# In[85]:


def solve_primal(Ax, Ap, b, c, instance_name, num_vars):
    import gurobipy as gp
    from gurobipy import GRB
    import numpy as np
    import time
    
    # インスタンスの生成
    m = gp.Model("LP_for_VRP" + instance_name)
    # 定数を設定　←　入力として与えられる
    # 変数を設定
    """
    x_i : 顧客iへ車両が到着する時刻を表す変数
    p_i : 顧客iの時間枠の違反度を表す変数
    """
    x = m.addMVar(shape=num_vars, vtype=GRB.CONTINUOUS, name="x")
    p = m.addMVar(shape=num_vars, vtype=GRB.CONTINUOUS, name="p")

    # モデルのアップデート
    m.update()
    
    # 目的関数を設定
    ## 各制約の違反度を最小化する
    m.setObjective(c.T @ p, sense=gp.GRB.MINIMIZE)
    
    # 制約条件を設定
    m.addConstr(Ax @ x + Ap @ p <= b, name="c")

    # モデルのアップデート
    m.update()
    
    # 時間計測スタート
    start = time.time()
    
    # 最適化
    m.optimize()
    
    # 時間計測ストップ
    elapsed_time = time.time() - start
    
    # 解の表示
    """if m.Status == gp.GRB.OPTIMAL:
        for i in range(num_vars):
            print(f"車両が顧客{i}に到着する時刻は、{x[i].X}")
        print("最適値 : ", m.ObjVal)
    print('\033[34m'+f"実時間\t{elapsed_time}"+'\033[0m')"""
    
    # モデルをテキストファイルにする
    m.write("out"+instance_name+".json")
        
    return m


# ## 双対問題を解く関数の定義

# In[87]:


def solve_dual(Ax, Ap, b, c, instance_name, num_vars, PStarts, DStarts):
    import gurobipy as gp
    from gurobipy import GRB
    import numpy as np
    import time
    
    # インスタンスの生成
    m = gp.Model("LP_for_VRP" + instance_name)
    
    # 変数を設定
    """
    y_i : 主問題における制約式iの潜在価値
    """
    y = m.addMVar(shape=num_vars, vtype=GRB.CONTINUOUS, name="y")

    # モデルのアップデート
    m.update()
    
    # 目的関数を設定
    ## 各制約の違反度を最小化する
    m.setObjective(-1 * b.T @ y, sense=gp.GRB.MAXIMIZE)
    
    # 制約条件を設定
    c1 = m.addConstr(Ax.T @ y >= 0, name="c1")
    c2 = m.addConstr(Ap.T @ y + c >= 0, name="c2")
    c3 = m.addConstr(y >= 0, name="c3")
    c = c1+ c2 + c3

    # モデルのアップデート
    m.update()
    
    # 時間計測スタート
    start = time.time()
    
    # ホットスタートの使用
    """for i in range(num_vars):
        y[i].PStart = PStarts[i]
    for i in range(len(c)):
        c[i].DStart = DStarts[i]"""
    
    # 最適化
    m.Params.Method = 0
    #m.Params.Presolve = 0
    m.optimize()
    
    # 時間計測ストップ
    elapsed_time = time.time() - start
    
    # 解の表示
    """if m.Status == gp.GRB.OPTIMAL:
        for i in range(num_vars):
            print(f"主問題における制約{i}の潜在価格は、{y[i].X}")
        print("最適値 : ", m.ObjVal)
    print('\033[34m'+f"実時間\t{elapsed_time}"+'\033[0m')"""
    
    # モデルをテキストファイルにする
    m.write("out"+instance_name+".json")
        
    return m


# ## ①全体を1つのLPとして解くveb.

# ### 全体のPrimalを解く

# In[88]:


Ax, Ap, b, c = make_inputs(tour, Customers)


# In[89]:


# Gurobiによって最適解を求める
P = solve_primal(Ax, Ap, b, c, instance_name+"P", len(tour))



# ## ②前半と後半をつなげるveb.
# 1. 適当なところで前後に分ける
# 1. 前半後半それぞれのPrimalを解く
# 1. 前半と後半それぞれのPrimalの最適解を、全体のDualに入れて解く
# 1. 全体のPrimalの最適解を得る

# ### 1. 適当なところで前後に分ける
# - ひとまず半分くらいで分けることにする

# In[69]:


threshold = len(tour)//2
#print(threshold)

former = tour[:threshold]
latter = tour[threshold:]
#print(f"巡回路全体は、{tour}")
#print(f"前半は、{former}")
#print(f"後半は、{latter}")


# ### 2. 前半後半それぞれのPrimalを解く

# In[70]:


import numpy as np
# 係数行列、ベクトルを整える
A1x, A1p, A2x, A2p, A3x, A3p, b1, b2, b3, c1, c2 = [], [], [], [], [], [], [], [], [], [], []
index = 0
index_P_f, index_P_l = [], []
## A1, A2, A3を定める
## b1, b2, b3を定める
for Ax_i, Ap_i, b_i in zip(Ax, Ap, b):
    if np.linalg.norm(Ax_i[threshold:], ord=2)==0.:
        A1x.append(Ax_i[:threshold])
        A1p.append(Ap_i[:threshold])
        b1.append(b_i)
        index_P_f.append(index)
    elif np.linalg.norm(Ax_i[:threshold], ord=2)==0.:
        A2x.append(Ax_i[threshold:])
        A2p.append(Ap_i[threshold:])
        b2.append(b_i)
        index_P_l.append(index)
    else:
        A3x.append(Ax_i)
        A3p.append(Ap_i)
        b3.append(b_i)
    index += 1
## c1, c2, c3を定める
c1 = c[:threshold]
c2 = c[threshold:]
## リストからnumpy arrayに変換
A1x = np.array(A1x)
A1p = np.array(A1p)
A2x = np.array(A2x)
A2p = np.array(A2p)
A3x = np.array(A3x)
A3p = np.array(A3p)
b1 = np.array(b1)
b2 = np.array(b2)
b3 = np.array(b3)
c1 = np.array(c1)
c2 = np.array(c2)
"""for i in range(1, 4):
    print(f"A{i}x : ", end="")
    print(eval("A"+str(i)+"x"))
    print(f"A{i}p : ", end="")
    print(eval("A"+str(i)+"p"))
    print(f"b{i} : ", end="")
    print(eval("b"+str(i)))
    if i <= 2:
        print(eval("c"+str(i)))"""


# In[71]:


# Gurobiによって最適解を求める
P_f = solve_primal(A1x, A1p, b1, c1, instance_name+"P_f", len(former))
P_l = solve_primal(A2x, A2p, b2, c2, instance_name+"P_l", len(latter))



# ### 3. 前半後半それぞれのPrimalの最適解を、全体のDualに入れて解く

# In[74]:


# 初期解の保存
PStarts = np.array([0 for constr in P_f.getConstrs()+P_l.getConstrs()]) #np.array([constr.Pi for constr in P_f.getConstrs()+P_l.getConstrs()])
y3 = np.zeros((Ax.shape[0]-PStarts.shape[0],))
PStarts = np.append(PStarts, y3)
for i, constr in zip(index_P_f, P_f.getConstrs()):
    PStarts[i] = abs(constr.Pi)
for i, constr in zip(index_P_l, P_l.getConstrs()):
    PStarts[i] = abs(constr.Pi)

DStarts = np.array([var.x for var in P_f.getVars()+P_l.getVars()])
c3 = np.zeros((PStarts.shape[0],))
DStarts = np.append(DStarts, c3)


# In[75]:


# Gurobiによって最適解を求める
D = solve_dual(Ax, Ap, b, c, instance_name+"D", PStarts.shape[0], PStarts, DStarts)



# In[ ]:




