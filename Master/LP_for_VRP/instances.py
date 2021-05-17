#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Customer():
    def __init__(self, x, y, d, e, l, s):
        self.x = x
        self.y = y
        self.d = d
        self.e = e
        self.l = l
        self.s = s


# # インスタンスを作成する関数

# In[19]:


def make_instance():
    import random
    random.seed(0)
    Customers = {}
    Customers["depot"] = Customer(0,0,0,0,1000,0)
    # ここにコードを書く
    # ランダムに顧客数を決める
    N = random.randint(10, 1000)
    # ランダムに各顧客の情報(座標、時間枠, サービスタイム)を決める
    for i in range(N):
        x = random.randint(0,100)
        y = random.randint(0,100)
        d = 0
        e = random.randint(0,100)
        l = random.randint(e,1000)
        s = 0
        Customers[i] = Customer(x, y, d, e, l, s)
    return Customers


# # インスタンス化

# In[20]:


Customers = make_instance()


# ## 値の表示

# In[21]:


"""print("\t", list(vars(Customers["depot"]).keys()))
for i in Customers.keys():
    print(i, end="\t")
    for key, val in vars(Customers[i]).items():
        print(val, end=" ")
    print()


# In[22]:


for i in range(len(Customers)-1):
    print(f"{i}\t[{Customers[i].e}, {Customers[i].l}]")"""


# # 巡回路

# In[25]:


tour = list(Customers.keys())[1:] + ["depot"]





