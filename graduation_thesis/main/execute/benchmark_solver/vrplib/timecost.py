
# coding: utf-8

# In[15]:

# timecost
from piecewise_linear_function import *
Inf = 1000000.0

class TimeWindow():
    '''時間枠を区分線形関数で表現する
    
    Attributes
    ----------
    piecewise : Piecewise
        区分線形関数
    
    Example
    -------
    >>> t = TimeWindow((3,5,1,10))
    >>> t.piecewise.drawGraph()        
    '''
    def __init__(self,timewindow):
        '''
        Parameters
        ----------
        timewindow : int,float,tuple,Piecewise,None
            int,float
                締め切り時刻
            tuple
                サイズ2のタプル(x1,x2)の場合は時間枠[x1,x2]
                サイズ4のタプル(x1,x2,a1,a2)の場合は早着違反係数がa1,遅延違反係数a2のソフトな時間枠[x1,x2]
            Piecewise
                区分線形関数
            None
                時間枠制約なし
        '''
        if isinstance(timewindow,(int,float)):# due date: piecewise
            if timewindow < 0.001:
                self.piecewise = Piecewise(x=[0,Inf],y=[Inf,Inf])
            elif timewindow >= Inf - 0.001:
                self.piecewise = Piecewise(x=[0,Inf],y=[0,0])
            else:
                self.piecewise = Piecewise(x=[0,timewindow,timewindow,Inf],y=[0,0,Inf,Inf])
        elif isinstance(timewindow,tuple):
            length = len(timewindow)
            if length == 2:
                x1,x2 = timewindow
                if x1 < 0.0001 and x2 >= Inf-0.0001:
                    self.piecewise = Piecewise(x=[0,Inf],y=[0,0])
                elif x1 < 0.0001:
                    self.piecewise = Piecewise(x=[0,x2,x2,Inf],y=[0,0,Inf,Inf])
                elif x2 >= Inf-0.0001:
                    self.piecewise = Piecewise(x=[0,x1,x1,Inf],y=[Inf,Inf,0,0])
                else:
                    self.piecewise = Piecewise(x=[0,x1,x1,x2,x2,Inf],y=[Inf,Inf,0,0,Inf,Inf])
            elif length == 4:
                x1, x2, a1, a2 = timewindow
                if a1 < 0 or a2 < 0:
                    raise Exception
                
                if x1<0.0001 and x2>=Inf-0.0001:
                    self.piecewise = Piecewise(x=[0,Inf], y = [0,0])
                elif x1 < 0.0001:
                    self.piecewise = Piecewise(x=[0,x2,Inf], y = [0,0,a2*(Inf-x2)])
                elif x2 >= Inf-0.0001:
                    self.piecewise = Piecewise(x=[0,x1,Inf], y = [a1*x1,0,0])
                else:
                    self.piecewise = Piecewise(x=[0,x1,x2,Inf], y = [a1*x1,0,0,a2*(Inf-x2)])
            else:
                raise Exception
        elif isinstance(timewindow,Piecewise):
            self.piecewise=timewindow            
        elif timewindow is None:
            self.piecewise = Piecewise(x=[0,Inf], y = [0,0])
        else:
            raise Exception
            
    def __str__(self):
        return str(self.piecewise)
    
class EdgeTimeCost():
    def __init__(self,traveltime,travelcost):
        if isinstance(traveltime,(int,float)):# due date: piecewise
            self.traveltime = Piecewise(x=[0,Inf],y=[traveltime,traveltime])
        elif isinstance(traveltime,Piecewise):
            self.traveltime=traveltime
        else:
            raise Exception
        if isinstance(travelcost,(int,float)):# due date: piecewise
            self.travelcost = Piecewise(x=[0,Inf],y=[travelcost,travelcost])
        elif isinstance(travelcost,Piecewise):
            self.travelcost=travelcost
        elif travelcost is None:
            self.travelcost = Piecewise(x=[0,Inf], y = [0,0])            
        else:
            raise Exception
    
    def __str__(self):
        return str(self.traveltime) + " " + str(self.travelcost)

class VehicleTimeCost():
    def __init__(self,**kwargs):
        self.timewindow=TimeWindow(kwargs["timewindow"])
        self.coef=kwargs["coef"]
    def __str__(self):
        return str(self.coef) + " " + str(self.timewindow)

class CustomerTimeCost():
    def __init__(self,**kwargs):
        self.timewindow=TimeWindow(kwargs["timewindow"])
        self.servicetime=kwargs["servicetime"]
    def __str__(self):
        return str(self.servicetime) + " " + str(self.timewindow)


# In[ ]:



