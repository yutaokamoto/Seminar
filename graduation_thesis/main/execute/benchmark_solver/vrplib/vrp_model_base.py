
# coding: utf-8

# In[10]:

class Customer_():
    """客オブジェクトを生成するクラス
    
        
    Attributes
    ----------
    stat : dictionary
        得られた解での客の情報     
    """
    __ID=0
    def __init__(self,name,**kwargs):
        '''
        Parameters
        ----------
        name : str
            客の名前('depot'は使用不可)
        kwargs : dictionary
            客の資源等        
       
       '''
        if name=="" or name==None:
            name ="__r{0}".format(Customer_.__ID)
            Customer_.__ID +=1
        self.name=name
        self.kwargs=kwargs
        self.stat=None
    def resource(self,rsrc):
        if rsrc in self.kwargs:
            return self.kwargs[rsrc]
        else:
            return ""
    def __str__(self):
        s="Customer "+self.name+": "
        s+= str(self.data) + "\n"
        if self.stat != None:
            s += str(self.stat)
        return s        
 
    
class Edge_():
    """枝オブジェクトを生成するクラス"""    
    def __init__(self,nfrom,nto,**kwargs):
        '''
        Parameters
        ----------
        nfrom : str
            枝の始点の名前
        nto : str
            枝の終点の名前
        kwargs: dictionary
            枝の資源等        
        '''
        self.nfrom=nfrom
        self.nto=nto
        self.kwargs=kwargs
    def resource(self,rsrc):
        if rsrc in self.kwargs:
            return self.kwargs[rsrc]
        else:
            return ""         
    def __str__(self):
        s="Edge "+str((self.nfrom,self.nto))+": "
        s+= str(self.data)
        return s   
    
class Vehicle_():
    """車両オブジェクトを生成するクラス
        
        Attributes
        ----------
        routing : list
            得られた巡回路
        consumed : dictionary
            得られた巡回路の情報
    """      
    def __init__(self,name,**kwargs):
        '''
        Parameters
        ----------
        name : str
            車両の名前
        kwargs: dictionary
            車両の資源等

        '''
        self.name=name
        self.kwargs=kwargs
        self.routing=None
        self.consumed={}
    def resource(self,rsrc):
        if rsrc in self.kwargs:
            return self.kwargs[rsrc]
        else:
            return ""      
    def __str__(self):
        s="Vehicle "+self.name+": "
        s+= str(self.data) + "\n"
        if self.routing != None:
            s += str(self.cost)+" = "
            s += str(self.consumed)
        return s        


# In[16]:

class Solver():
    def __init__(self,**kwargs):
        import platform
        import os
        exefile=kwargs["exefile"]
                
        if platform.system() == "Windows":
            self.program = os.path.dirname(__file__)+"/"+exefile+"-win"
        elif platform.system() == "Darwin":
            self.program = os.path.dirname(__file__)+"/"+exefile+"-mac"
        elif platform.system() == "Linux":
            self.program = os.path.dirname(__file__)+"/"+exefile+"-linx"
        else:
            print(platform.system(),"may not be supported.")
           
        if platform.system() != "Windows" and not os.access(self.program,os.X_OK):
            print(self.program,"is not executable")
            print("Change the permission by the following command:", "chmod +x",self.program)            
            raise Exception
            
        self.vrpargs={"TimeLimit":5,"RandomSeed":0,"IterLimit":100,"InitSol":"","OutputFlag":False,"Solcsv":"vrp_solution.csv",                     "Verbose":False,"TwoOpt":0,"NCross":3,"Logfile":exefile+".log"}
        self.vrpargs.update({r:1.0 for r in kwargs["resources"]})
                
        self.vrpargs.update(kwargs)
        self.vrpargs["Verbose"]=" -v" if self.vrpargs["Verbose"] == True else ""
        
        self.alphabet={"instance":" -I","TimeLimit":" -T","TwoOpt":" -Nt",                       "RandomSeed":" -S","IterLimit":" -l","Verbose":" ","InitSol":" -i","Solcsv":" -c",                      "NCross":" -Nc","Logfile":" -L"}
        self.alphabet.update({r:" -C "+r for r in kwargs["resources"]})
        
#        print()
#        print(self.vrpargs)
#        print(self.alphabet)
        
        
    def evaluate(self,instance,solution_file):
        self.vrpargs["TimeLimit"]=0
        self.vrpargs["InitSol"]=solution_file
        r,feasible_flag=self.optimize(instance)
        
        return (r,feasible_flag)

    def optimize(self,instance):
        self.vrpargs["instance"]=instance

        cmd = self.program
        for k in self.alphabet:
            if str(self.vrpargs[k]) !="":
                cmd += self.alphabet[k] + " " + str(self.vrpargs[k])
        
        if self.vrpargs["OutputFlag"]:
            print(cmd)
        
        import subprocess
        import platform
        try:
            if platform.system() == "Windows":
                pipe = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE, shell=True)
            else:
                pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE, shell=True)
#            print("\n ================ Now solving the problem ================ \n")
        except OSError:
            print("error: could not execute command '%s'" % cmd)
#            print("please check that the solver is in the path")
#            model.Status = 9 #execution failed
            return None

        out, err = pipe.communicate()                 #get the result

        import os
        if err!=None:
            err = str(err, encoding='utf-8')
            with open("error.txt","w") as file:
                file.write(err)
        out=str(out,encoding='utf-8')
        
        if self.vrpargs["OutputFlag"]==True:
            print(out)
            
        self.Status = pipe.returncode
        if self.Status !=0: #if the return code is not "optimal", then return
            Error={
                1:"ECTRC: 求解中にユーザがCtrl-Cを入力したことによって強制終了した",
                2:"EREADSOL: 初期解ファイルの読み込みに失敗した",
                3:"EWRITELOG: ログファイルの書き込みに失敗した",
                4:"EDATAFORMAT: 入力データの書式にエラーがある",
                5:"EMEMORY メモリの確保に失敗した",
                6:"EPARAMFORMAT: 実行ファイルのよび出しに失敗した",
                7:"ESCHEDULE スケジュールが決定できない",
                8:"EOPENFILE: ファイルを開けない",
                -1:"EOTHERS: その他のエラー"
            }
            print("Status=",self.Status,Error[self.Status])
            print("Output=",out)
            return None
        
        
        totalcost = None
        feasible_flag = False
        with open(self.vrpargs["Logfile"], "r") as logfile:
            for line in logfile:
                if line.startswith("Best Feasible Solution"):
                    totalcost = float(line.strip()[22:])
                    feasible_flag=True
                elif totalcost == None and line.startswith("Best Solution"):
                    totalcost = float(line.strip()[14:])
        if feasible_flag == False:
            print("Feasible solution is not found")
#            import sys
#            sys.exit()
        
        return (totalcost,feasible_flag)


# In[36]:

class Model_():
    '''配送計画モデルクラス'''
    infeasible_edge=None
    def __init__(self,name,resources):
        '''
        Parameters
        ----------
        name : str
            モデルの名前
        resources : tuple
            使用する機能
        '''
        import sys
        if int(sys.version_info[0]) != 3:
            print("Python 3 is required.")
            sys.exit(0)        
            
        self.name=name
        self.customers={}
        self.customersL=[]
        self.edges = {"depot":{}}
        self.vehicles={}
        self.vehiclesL=[]
        self.resources=resources
        self.coefs={r:1.0 for r in resources}
        self.__name_to_id={"depot":0}
        self.feasible_cost={}
    def __add_customer(self,customer):
        if customer.name=="depot":
            return NameError
        self.__name_to_id[customer.name]=len(self.customersL)+1
        self.customersL.append(customer)
        if customer.name in self.customers:
            raise NameError
        self.customers[customer.name]=customer
        self.edges[customer.name]={}
    def __add_vehicle(self,vehicle):
        self.vehiclesL.append(vehicle)
        if vehicle.name in self.vehicles:
            raise NameError        
        self.vehicles[vehicle.name]=vehicle
    def __add_edge(self,edge):        
        node1 = edge.nfrom
        node2 = edge.nto
        if node1 not in self.customers and node1 != "depot":
            raise KeyError
        if node2 not in self.customers and node2 != "depot":
            raise KeyError
        self.edges[node1][node2] = edge

            
    def __print_resource(self,rsrc):
        filename = self.name + "."+ rsrc
        form = str(self) +  "\n"
        form += "# filename: " + filename + "\n"        
        form += "# customer_number  vehicle_number  dimension feasible_cost\n"
        form += str(len(self.customers)) + " " + str(len(self.vehicles)) + " " + str(self.vehiclesL[0].kwargs[rsrc+"_dim"])                + " "+str(self.feasible_cost[rsrc])+ "\n"
            
        form += "# vehicle data\n"
        for i in range(len(self.vehiclesL)):
            v=self.vehiclesL[i]
            form += str(v.resource(rsrc)) +"\n"

        form += "# customer data\n"
        for i in range(len(self.customersL)):
            c=self.customersL[i]
            if c.resource(rsrc) != "":
                form += str(c.resource(rsrc)) + "\n"

        form += "# edge data\n"
        na_edge=Model_.infeasible_edge
        if na_edge == None:
            print("Error")
        edges = self.edges["depot"]
        for i in range(len(self.customersL)):
            node=self.customersL[i].name
            e = edges[node] if node in edges else na_edge
            if e.resource(rsrc) != "":
                form += str(e.resource(rsrc))+ "\n"
        
        for i in range(len(self.customersL)):
            ci=self.customersL[i]
            edges = self.edges[ci.name]
            e = edges["depot"] if "depot" in edges else na_edge
            if e.resource(rsrc) != "":
                form += str(e.resource(rsrc)) + "\n"   
            
            for j in range(len(self.customersL)):
                if i == j:
                    continue
                node=self.customersL[j].name
                e = edges[node] if node in edges else na_edge
                if e.resource(rsrc) != "":
                    form += str(e.resource(rsrc)) + "\n"     
#        print(form)
        with open(filename, "w") as file:
            file.write(form)
    def __write_instance_files(self):
        for r in self.resources:
            self.__print_resource(r)
    def optimize(self,**kwargs):
        '''
        最適化ソルバの実行
        Parameters
        ----------
        kwargs : dictionary
            "TimeLimit" : int
                タイムリミット(秒)
            "RandomSeed" : int
                乱数の種
            "IterLimit" : int
                局所探索法の最大実行回数
            "InitSol" : str
                初期解を与える場合，そのファイル名
            "OutputFlag" : boolean
            "Solcsv" : str
            "Verbose" : boolean
                詳細な出力をするか否か
            "TwoOpt" : 0,1
            "NCross" : int
            "Logfile" : str
                ログファイルの名前
        '''        
        solargs={"resources":self.resources}
        solargs["exefile"]=self.exefile
        solargs.update(self.coefs)
        solargs.update(kwargs)
        
        self.__write_instance_files()
        solver=Solver(**solargs)
        r=solver.optimize(self.name)

        self.__read_solution_file()
        return r
    
    def evaluate(self,**kwargs):
        for v in self.vehicles:
            if self.vehicles[v].routing == None:
                print("Routing is not specified")
                return None
        solution_file="tmp.routing"
        self.__write_instance_files()
        self.__write_routing(solution_file)
        
        solargs={"resources":self.resources}
        solargs["exefile"]=self.exefile        
        solargs.update(self.coefs)        
        solargs.update(kwargs)
        
        solver=Solver(**solargs)
        r=solver.evaluate(self.name,solution_file)
        return r
    
    
    def __write_routing(self,filename):
        with open(filename,"w") as f:
            for v in self.vehiclesL:
                s = "0 "
                for e in v.routing[1:-1]:                        
                    s += str(self.__name_to_id[e.name]) + " "
                f.write(s + "0\n")
    
    def __read_solution_file(self):
        filename="vrp_solution.csv"
        import os
        
        with open(filename,"r") as file:
            v=None
            cname=None
            for line in file:
                row = line.strip().split(",")
                if len(row)==1:
                    s_row=row[0].split(" ")
                    if s_row[-1] == "1000000000.000000":
                        self.feasible=False
                    else:
                        self.feasible=True
                elif row[0]=="vehicle":
                    v=self.vehiclesL[int(row[1])-1]
                    v.cost=float(row[2])
                    for k in range(len(self.resources)):
                        v.consumed[self.resources[k]]=float(row[3+k])
                    v.routing=[]
                elif row[0]=="customer" and cname==None:
                    cname=[e for e in row]
                elif row[0].isdigit():
                    cid=int(row[0])-1
                    if cid == -1:
                        v.routing.append("depot")

                        if len(v.routing) == 1:
                            v.stat={cname[i]:row[i] for i in range(len(row))}
                        else:
                            for i in range(len(row)):
                                if v.stat[cname[i]]=="":
                                    v.stat[cname[i]]=row[i]
                    else:
                        c=self.customersL[cid]
#                        v.routing.append(c.name)
                        v.routing.append(c)
                        c.stat={cname[i]:row[i] for i in range(len(row))}
                        del c.stat[""]
                        del c.stat["customer"]                            
                        
    
        return None
    
    def set_coefs(self,**kwargs):
        for r in kwargs:
            if r not in self.resources:
                print(r,"=",kwargs[r],"is not supported.")
            else:
                self.coefs[r]=kwargs[r]            
#    def print_coefs(self):
#        print(self.name,self.coefs)
#        for v in self.vehiclesL:
#            print(v.name,v.coefs)    
        
    def __iadd__(self, e):
        if isinstance(e,Customer_):
            self.__add_customer(e)
        elif isinstance(e,Vehicle_):
            self.__add_vehicle(e)
        elif isinstance(e,Edge_):
            self.__add_edge(e)
        else:
            raise TypeError
        return self        
            
            
    def __str__(self):
        s= "# Model: " + self.name + ", "
        s += "vehicle:"+str(len(self.vehicles)) + ", "
        s += "customer:"+str(len(self.customers)) + ", "
        s += " resource:"+str(self.resources)
        return s

