#!/usr/bin/env python
# coding: utf-8

# # コマンドライン引数

# In[1]:


import sys

args = sys.argv


# In[ ]:


N = int(args[2])


# In[ ]:


time_limit = int(args[3])


# In[ ]:


output_file = args[1]+"_N"+str(N)+"_TL"+str(time_limit)+".txt"


# In[2]:


print(output_file)


# # 問題例の作成

# In[495]:


class Timewindow():
    def __init__(self, e, l):
        self.e = e
        self.l = l


# In[496]:


class Coordinate():
    def __init__(self, x, y):
        self.x = x
        self.y = y


# In[497]:


class Customer():
    def __init__(self, d, tw, coo, penalty, reward):
        self.demand = d
        self.tw = Timewindow(*tw)
        self.coordinate = Coordinate(*coo)
        self.penalty = penalty
        self.reward = reward


# In[498]:


class Vehicle():
    def __init__(self, c, tour):
        self.capacity = c
        self.tour = tour


# In[499]:


class piecewise_func():
    def __init__(self, e, l, interception, slope):
        self.e, self.l = e, l
        self.linear_func = lambda x : interception-(x-e)*slope
    def val(self, x):
        if x < self.e or self.l < x:
            return 0
        elif self.e <= x <= self.l:
            return self.linear_func(x)


# In[500]:


class Reward_func():
    def __init__(self, interception, slope):
        self.interception = interception
        self.slope = slope


# In[862]:


def ex(N):
    """
    V : 客集合
        N : 客数
        d : 需要
        tw : 時間枠
        (x, y) : 座標
        penalty : 時間枠を違反した場合にかかる、単位時間あたりの違反料
    K : 車両集合
        c : 容料
        #loading : 現在積んでいる荷物の量
        tour : 巡回路
    """
    import random
    random.seed(0)
    #N = 1024 #random.randint(5, 10)
    max_d = N #10
    max_tw = N*10 #50
    max_co = N*0.2 #10
    max_slope = 3
    max_interception = 5
    V = {}
    sum_d = 0
    V[0] = Customer(0, [0,max_tw], (0,0), 0, piecewise_func(*(0, max_tw), *(0,0)))
    for i in range(1, N+1):
        d = random.uniform(-max_d, max_d)
        tw = sorted([random.uniform(0, max_tw) for i in range(2)])
        x, y = random.uniform(-max_co, max_co), random.uniform(-max_co, max_co)
        penalty = random.uniform(1, 10)
        slope = (-1)*random.uniform(0, max_slope)
        interception = random.uniform(0, max_interception) + (tw[1]-tw[0])*(-slope)
        reward = Reward_func(interception, slope)#piecewise_func(*tw, interception, slope)
        V[i] = Customer(d, tw, (x, y), penalty, reward)
        sum_d += d*(d>0)
        
    K = {}
    min_cap = max_d*0.8
    max_cap = max_d*2
    """
    M = 2 # random.randint(N//2, N*2)
    for k in range(M):
        c = random.uniform(min_cap, max_cap)
        K[k] = Vehicle(c, [])
    """
    sum_cap = 0
    i = 0
    while sum_cap<sum_d*3:
        c = random.uniform(min_cap, max_cap)
        K[i] = Vehicle(c, {})
        sum_cap += c
        i += 1
    #"""
    return V, K


# # 問題を解く

# ## 巡回路を生成  
# 先生のソルバーを使う

# In[869]:


V, K = ex(N)


# In[870]:


# 入力
## 顧客
C={} # 客の座標を保存する辞書
TW={} # 客の時間枠を保存する辞書
demand={} # 客の要求量(正の値は集荷，負の値は配達)
S={} # 客のサービス時間

for i in V:
    if i != 0:
        name="c"+str(i-1)
        x, y = V[i].coordinate.x, V[i].coordinate.y
        C[name] = (x,y)
        e, l = V[i].tw.e, V[i].tw.l
        TW[name] = (e,l)
        demand[name] = (V[i].demand, )
        S[name] = 0 #random.randint(10,20)
C["depot"]=(0,0)

## 車両
M = len(K) # number of vehicles
capacities = [(K[k].capacity, ) for k in range(M)] # capacity of vehicle


# In[873]:


# 距離関数の定義
def Distance(t1,t2):
    return ((t1[0]-t2[0])**2+(t1[1]-t2[1])**2)**(0.5)

# ソルバーの読み込み
import sys
sys.path.append('..')

#from vrplib.vrp_d_1m1_t_model import *
import vrplib.vrp_d_1m1_t_model as vrp

# ソルバーの実行
model = vrp.Model("example") # モデルインスタンスの生成

## 客インスタンスの生成
for i in C:
    if i == "depot":
        continue
    model += vrp.Customer(i,demand=demand[i],timewindow=TW[i],servicetime=S[i])

## 車両インスタンスの生成
for k in range(M):
    model += vrp.Vehicle("v"+str(k),capacity=capacities[k])
    
## 枝インスタンスの生成
for i in C:
    for j in C:
        if i!=j:
            dist = time = Distance(C[i],C[j])
            model += vrp.Edge(i,j,dist,time)


# In[874]:


## 最適化の実行
obj=model.optimize(IterLimit=100000,TimeLimit=time_limit,Verbose=False,OutputFlag=False)


# ## 各車両の巡回路を保存

# In[875]:


for v in model.vehiclesL:
    K[int(v.name[1:])].tour = (0,) + tuple(map(lambda x:int(x.name[1:])+1, v.routing[1:-1]))


# ## 巡回路を評価（各顧客の出発時刻を決める）  
# どのくらい時間がかかるか調べる

# In[877]:


def distance(i, j, V):
    x0 = V[i].coordinate.x
    y0 = V[i].coordinate.y
    x1 = V[j].coordinate.x
    y1 = V[j].coordinate.y
    return ((x0-x1)**2 + (y0-y1)**2)**(1/2)


# In[878]:


import gurobipy as gp

# インスタンスの生成
m = gp.Model("LP_for_VRP_small")

# 定数を設定
#V, K = ex() #ex_small()

# 変数を設定
"""
x_ik : 顧客iへ車両kが到着する時刻を表す変数
y_i : 車両が顧客iに到着する時刻が、顧客iの時間枠に対して、どの程度違反しているかを表す変数
"""
x = {(i,k):m.addVar(vtype=gp.GRB.CONTINUOUS, name=f"x({i},{k})") for k in K for i in K[k].tour}
y = {i:m.addVar(vtype=gp.GRB.CONTINUOUS, name=f"y({i})") for i in V}

m.update()


# In[879]:


# 目的関数を設定
## 各顧客iの到着時刻x_ikと顧客iの時間枠を元に計算した違反料の和を最小化する
m.setObjective(gp.quicksum(V[i].penalty*y[i] for i in V), sense=gp.GRB.MINIMIZE)


# In[880]:


# 制約条件を設定
## 時間枠の違反に関する制約
for k in K:
    for i in K[k].tour:
        #m.addConstr(y[i,k] == penalty(i, x[i,k], V))
        m.addConstr(V[i].tw.e-y[i] <= x[i,k])
        m.addConstr(x[i,k] <= V[i].tw.l+y[i])
## 任意の車両の巡回路内における、各顧客への到着時刻の先行、後行に関する制約
for k in K:
    for idx_p, i_p in enumerate(K[k].tour):
        for idx_f, i_f in enumerate(K[k].tour):
            if idx_p < idx_f:
                #print(f"顧客{i_p}は顧客{i_f}よりも先に訪れられる")
                m.addConstr(x[i_p, k] + distance(i_p, i_f, V) <= x[i_f, k])
## 全ての車両はデポを出発し、サービス時間内に到着するという制約
for k in K:
    m.addConstr(0 <= x[0,k])


# In[884]:


import time

# 時間計測スタート
start = time.time()

# 最適化
m.optimize()

# 時間計測ストップ
elapsed_time = time.time() - start

fea_flag = False
if m.Status == gp.GRB.OPTIMAL:
    fea_flag = True
    
objval = m.ObjVal
                
"""# 解の表示
if m.Status == gp.GRB.OPTIMAL:
    for k in K:
        for i in K[k].tour:
            print(f"車両{k}が顧客{i}に到着する時刻は、{x[i, k].X}")
    print("最適値 : ", m.ObjVal)
    
print('\033[31m'+f"実時間\t{elapsed_time}"+'\033[0m')"""


# # ファイルに結果を出力

# In[ ]:


print(f"顧客数 : {N}, 実行可能性 : {fea_flag}, 目的関数値 : {objval}, 実時間 : {elapsed_time}")


# In[ ]:


with open(output_file, mode="w") as f:
    f.write("Number of customers : "+str(N)+"\n")
    f.write("Feasibility : "+str(fea_flag)+"\n")
    f.write("Objective value : "+str(objval)+"\n")
    f.write("Execution time : "+str(elapsed_time)+"\n")
    #f.write("顧客数 : "+str(N)+"\n"+"実行可能性 : "+str(fea_flag)+"\n"+"目的関数値 : "+str(objval)+"\n"+"実時間 : "+str(elapsed_time)+"\n")

