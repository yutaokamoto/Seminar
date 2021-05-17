#!/usr/bin/env python
# coding: utf-8

# In[3]:


class Customer():
    def __init__(self, x, y, d, e, l, s):
        self.x = x
        self.y = y
        self.d = d
        self.e = e
        self.l = l
        self.s = s


# # インスタンスを作成する関数

# In[1]:


def make_instance():
    import random
    random.seed(0)
    Customers = {}
    Customers["depot"] = Customer(0,0,0,0,1000,0)
    # ここにコードを書く
    # ランダムに顧客数を決める
    N = random.randint(10, 10000)
    # ランダムに各顧客の情報(座標、時間枠, サービスタイム)を決める
    lower = 1
    for i in range(N):
        x = random.randint(0,10)
        y = random.randint(0,10)
        d = 0
        e = random.randint(lower,lower+2)
        l = random.randint(e,e+5)
        s = 0
        Customers[i] = Customer(x, y, d, e, l, s)
        lower = l
    return Customers


# # インスタンス化

# In[4]:


Customers = make_instance()


# ## 値の表示

# In[5]:


tour = list(Customers.keys())[1:] + ["depot"]





