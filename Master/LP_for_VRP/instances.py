#!/usr/bin/env python
# coding: utf-8

class Customer():
    def __init__(self, x, y, d, e, l, s, t=None):
        self.x = x
        self.y = y
        self.d = d
        self.e = e
        self.l = l
        self.s = s
        self.t = t # 集荷から配達までの制限時間


# # インスタンスを作成する関数
def make_instance():
    import random
    random.seed(0)
    Customers = {}
    # 車両がdepotへ帰還する時刻を最小化したいので、時間枠を[0,0]とする。
    Customers["depot"] = Customer(0,0,0,0,0,0,10000)
    # ここにコードを書く
    # ランダムに顧客数を決める
    N = 10#random.randint(1, 1)
    # ランダムに各顧客の情報(座標、時間枠, サービスタイム)を決める
    lower = 1
    for i in range(N):
        x = random.randint(0,10)
        y = random.randint(0,10)
        d = 0
        e = random.randint(lower,lower+2)
        l = random.randint(e,e+5)
        s = 0
        #t = random.randint(0,10)
        Customers[i] = Customer(x, y, d, e, l, s)
        lower = l
    return Customers


# # インスタンス化
Customers = make_instance()


# # 集荷地点と配達地点を定める
from scipy.special import comb
import random
random.seed(0)
N = len(Customers)
Cs = list(range(0,N))
r = random.randint(0,N//2)
P_plus_indexes = [random.randint(0,N-1) for i in range(r)]
P_plus = [Cs[i] for i in P_plus_indexes]
res = list(set(Cs)-set(P_plus))
Points = []
for p in P_plus:
    for d in res:
        if p<d:
            Points.append((p,d))
            break
for Point in Points:
    p, d = Point
    Customers[p].t = random.randint(0,100)
    Customers[d].t = random.randint(0,100)

# # 車両の各値の設定
C = 100
F = 80


# ## 巡回路の作成
tour = list(Customers.keys())[1:] + ["depot"]





