
# coding: utf-8

# In[5]:

from vrp_model_base import *


# In[6]:

from freight import *
from timecost import *
from distance import *


# In[3]:

class Customer(Customer_):
    def __init__(self,name,**kwargs):
        '''
        Parameters
        ----------
        name : str
            客の名前
        kwargs : dictionary
            "demand" : tuple, default (0,)
                客の需要量(多次元も可能)．正の値は集荷，負の値は配達．
            "timewindow" : int,float,tuple,Piecewise,default None
                客の時間枠
            "servicetime" : int, default 0
                客でのサービス時間
        '''
        args={"demand":(0,),"timewindow":None,"servicetime":0}
        args.update(kwargs)
        self.data=args        
        super().__init__(name,                         freight_1M1=CustomerFreight(*args["demand"]),                         timecost=CustomerTimeCost(timewindow=args["timewindow"],servicetime=args["servicetime"])                        )        
                         
class Edge(Edge_):
    def __init__(self,nfrom,nto,distance,traveltime,travelcost=None):
        '''
        Parameters
        ----------
        distance : float
        traveltime : int,float,Piecewise
        travelcost : int,float,Piecewise,None,default None
        '''
        self.nfrom,self.nto = nfrom,nto
        self.data={"distance":distance,"traveltime":traveltime,"travelcost":travelcost}
        super().__init__(nfrom,nto,distance=distance,timecost=EdgeTimeCost(traveltime,travelcost))
     

#global infeasible_edge
#infeasible_edge=Edge(Inf,Inf,Inf)
model_inf=1000000
Model_.infeasible_edge=Edge("depot","depot",model_inf,0,0)
        

class Vehicle(Vehicle_):
    def __init__(self,name,**kwargs):
        '''
        Parameters
        ----------
        name : str
            客の名前
        kwargs : dictionary
            "capacity" : tuple
                車両の容量
            "timewindow" : int,float,tuple,Piecewise,default None
                デポへの帰還時刻に対する時間枠
            "max_distance" : float,default 10000000
                車両の最大移動距離
        '''
        
        args={"timewindow":None,"dummy":False,"max_distance":10000000}
        self.coefs={"freight_1M1":1.0,"distance":1.0,"timecost":1.0}
        

        args.update(kwargs)
        self.data=kwargs
        
        super().__init__(name,                         freight_1M1=VehicleFreight(capacity=args["capacity"],coef=self.coefs["freight_1M1"]),                         distance=VehicleDistance(coef=self.coefs["distance"],ub=args["max_distance"]),                         timecost=VehicleTimeCost(timewindow=args["timewindow"],coef=self.coefs["timecost"])                        )
        
        self.kwargs["freight_1M1_dim"]=len(kwargs["capacity"])
        self.kwargs["distance_dim"]=1
        self.kwargs["timecost_dim"]=1


# In[4]:

class Model(Model_):
    def __init__(self,name):
        '''
        使用可能な機能
            distance
                距離
            freight_1M1
                pickup and delivery type: One-Many-One
            timecost
                時間枠
        
        Parameters
        ----------
        name : str
            モデルの名前
        '''
        super().__init__(name,("distance","freight_1M1","timecost"))
        self.feasible_cost.update({"freight_1M1":0,"timecost":"","distance":""})
        self.exefile="vrp_d_1m1_t"


# In[ ]:



