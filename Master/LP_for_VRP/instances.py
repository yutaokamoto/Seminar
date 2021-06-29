#!/usr/bin/env python
# coding: utf-8

class Customer():
    def __init__(self, x, y, d, e, l, s, t=None):
        self.x = x
        self.y = y
        self.d = d
        self.e = e
        self.l = l
        self.s = s # サービスタイム
        self.t = t # 集荷から配達までの制限時間


# # インスタンスを作成する関数
def make_instance():
    import random
    random.seed(0)
    Customers = {}
    # 車両がdepotへ帰還する時刻を最小化したいので、時間枠を[0,0]とする。
    Customers["depot"] = Customer(0,0,0,0,0,0,100000)
    # ここにコードを書く
    # ランダムに顧客数を決める
    N = 100#random.randint(1, 1)
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
import random
random.seed(0)
tour = list(Customers.keys())[1:]
n = len(tour)
n_pair = random.randint(0, n//2)
pickup = set()
delivery = set()
Points = []
for i in range(n_pair):
    p, d = -1, -1
    while True:
        p = random.randint(0, n-1)
        d = random.randint(p, n-1)
        if p!=d and (p not in pickup) and (d not in delivery):
            break
    pickup |= {p}
    delivery |= {d}
    Points.append((p, d))
    #print("p= ", p, ", d = ", d)
    Customers[p].t = random.randint(0,100000)
    #print("demand of 'p' = ", Customers[p].d)
    if Customers[d].d >= 0:
        Customers[d].d = 0
    Customers[d].d -= Customers[p].d

# # 車両の各値の設定
C = 500
F = C*0.8


# ## 巡回路の作成
tour = list(Customers.keys())[1:] + ["depot"]





