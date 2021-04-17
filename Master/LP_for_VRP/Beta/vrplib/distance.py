
# coding: utf-8

# In[ ]:

#distance
class VehicleDistance():
    def __init__(self,**kwargs):
        self.ub=kwargs["ub"]
        self.coef=kwargs["coef"]
    def __str__(self):
        return str(self.coef) + " " + str(self.ub) 

