
# coding: utf-8

# In[12]:

import matplotlib.pyplot as plt

class Piecewise():
    '''Piecewise linear function class.
    Domain [0,1000000.0]
    '''
    Inf = 1000000.0
    ID=0
    def __init__(self,name="", x=None, y=None):
        """
        Parameters
        ----------
        name: str
            Name of piecewise linear function.
        x : list
            List of x coordinates of breaking points.
        y : list
            List of y coordinates of breaking points.
             
        Attributes
        ----------
        segment : list
            List of piecewise linear information (left, right, slope, intersect) 
                
        Examples
        --------
        >>> f=Piecewise(x=[0,10,20],y=[5,0,0])
        2 0 10 -0.5 5.0 10 1000000.0 0.0 0.0
        >>> print(f)
        >>> f.drawGraph()
        """
        if x is None:
            x = []
        if y is None:
            y = []
                    
        for i in range(len(x)-1):
            if x[i] > x[i+1]:
                raise TypeError
        if len(x) != len(y):
            raise TypeError
            
        if name=="" or name==None:
            name ="__p{0}".format(Piecewise.ID)
            Piecewise.ID +=1
        self.name = name

        if x[0] > 0:
            x = [0,x[0]] + list(x)
            y = [self.Inf, self.Inf] + list(y)
        if x[-1] > self.Inf:
            raise TypeError
        elif x[-1] < self.Inf:
            x = list(x) + [x[-1],self.Inf]
            y = list(y) + [self.Inf, self.Inf]            

        self.segment = []
        for i in range( len(x)-2 ):
            if x[i+1]==x[i]:
                if y[i+1]==y[i] or x[i+2]==x[i]:
                    print(y[i+1],y[i])
                    print(x[i+2],x[i])
                    raise TypeError
                continue
            
            a = (y[i+1]-y[i])/(x[i+1]-x[i]) #slope 
            b = y[i]-a*x[i]
            self.segment.append( (str(x[i]), str(x[i+1]), str(a), str(b) ) )
            
        i = len(x)-2
        if x[i+1]==x[i]: # 最後のふたつのx座標が等しいとき, 
            a = 0
            b = min(y[i],y[i+1])
        else:
            a = (y[i+1]-y[i])/(x[i+1]-x[i]) #slope 
            b = y[i]-a*x[i]
        self.segment.append((str(x[i]), str(self.Inf), str(a), str(b)))
            
        self.x = x
        self.y = y
            
            
#        
    def __str__(self):
        ret= [ str(len(self.segment)) ]
        for s in self.segment:
            ret.append( " ".join(s) )
        return " " .join(ret)
    
    def drawGraph(self):
        if self.x in (None,[]) or self.y in (None,[]):
            pass
        else:
            plt.plot(self.x, self.y, "o-")
            flag = len(self.x) > 2
            if flag:
                if self.x[-2] >= self.Inf - 0.0001:
                    plt.xscale("symlog")
                if max(self.y[:-1]) >= self.Inf - 0.0001:
                    plt.yscale("symlog")
                
            else:
                plt.xscale("symlog")
                plt.yscale("symlog")
            
            
            plt.xlim(0,self.x[-2]*1.1 if flag else self.x[-1])
            plt.ylim(0,max(self.y[:-1])+0.0001)
            
            xtick = sorted(set([0] + self.x[:-1] if flag else self.x))
            ytick = sorted(set([0] + self.y[:-1] if flag else self.y))
            plt.xticks(xtick, [str(i) if i < self.Inf - 0.0001 else "Inf" for i in xtick])
            plt.yticks(ytick, [str(i) if abs(i) < self.Inf - 0.0001 else ("Inf" if i > -0.0001 else "-Inf") for i in ytick])
            plt.show()
        


# In[ ]:



