
# coding: utf-8

# In[ ]:

# freight
class CustomerFreight():
    def __init__(self,*args):
        self.args=args
    def __str__(self):
        return ' '.join(map(str,self.args))
    
class VehicleFreight():
    def __init__(self,**kwargs):
        self.kwargs=kwargs
    def __str__(self): # vehicle data: coef, (lb_start,...), (ub_start,...), (lb_end,...), (ub_end,...), capa
        ndim=len(self.kwargs["capacity"])
        s = str(self.kwargs["coef"]) + " "
        s += ndim*"0 " # lb_start
#        s += ndim*"0 " # ub_start
        s +=  ' '.join(map(str,self.kwargs["capacity"])) + " " #ub_start
        s += ndim*"0 " # lb_end
        s +=  ' '.join(map(str,self.kwargs["capacity"])) + " " #ub_end
        s +=  ' '.join(map(str,self.kwargs["capacity"])) # capa
        return s    


# In[ ]:



