# 主問題を解く関数の定義
## 与えられた定数を元にLPのモデルを作成した上でそれを解き、最適解を返す関数
def solve_primal(As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq, op, oq, instance_name, num_vars):
    import gurobipy as gp
    from gurobipy import GRB
    import numpy as np
    import time
    
    # インスタンスの生成
    m = gp.Model("LP_for_VRP" + instance_name)
    # 定数を設定　←　入力として与えられる
    # 変数を設定
    """
    s_i : 顧客iへ車両が到着する時刻を表す変数
    r_i : 顧客 i における車両の燃料補充時間を表す変数
    c_i : 顧客 i に到着した時の燃料残量を表す変数
    p_i : 顧客iの時間枠の違反度を表す変数
    q_i : 顧客 i の荷物を配達するまでの制限時間に関する違反量を表す変数
    """
    s = m.addMVar(shape=num_vars, vtype=GRB.CONTINUOUS, name="s")
    r = m.addMVar(shape=num_vars, vtype=GRB.CONTINUOUS, name="r")
    c = m.addMVar(shape=num_vars, vtype=GRB.CONTINUOUS, name="c")
    p = m.addMVar(shape=num_vars, vtype=GRB.CONTINUOUS, name="p")
    q = m.addMVar(shape=num_vars, vtype=GRB.CONTINUOUS, name="q")

    # モデルのアップデート
    m.update()
    
    # 目的関数を設定
    ## 各制約の違反度を最小化する
    m.setObjective(op.T @ p + oq.T @ q, sense=gp.GRB.MINIMIZE)
    
    # 制約条件を設定
    ## 各係数行列のサイズを合わせる
    m.addConstr(As @ s + Ac_leq @ c + Ar_leq @ r + Ap @ p + Aq @ q <= b_leq, name="c_leq")
    m.addConstr(Ac_eq @ c + Ar_eq @ r == b_eq, name="c_eq")

    # モデルのアップデート
    m.update()
    
    # 時間計測スタート
    start = time.time()
    
    # パラメータ
    m.Params.Presolve = 0
    m.Params.Method = 0
    
    # 最適化
    m.optimize()
    
    # 時間計測ストップ
    elapsed_time = time.time() - start
    
    # 解の表示
    """if m.Status == gp.GRB.OPTIMAL:
        for i in range(num_vars):
            print(f"車両が顧客{i}に到着する時刻は、{x[i].X}")
        print("最適値 : ", m.ObjVal)
    print('\033[34m'+f"実時間\t{elapsed_time}"+'\033[0m')"""
    
    # モデルをテキストファイルにする
    m.write("out"+instance_name+".json")
        
    return m

# 双対問題を解く関数の定義
def solve_dual(As, Ac_eq, Ac_leq, Ar_eq, Ar_leq, Ap, Aq, b_eq, b_leq, op, oq, instance_name, num_vars_1, num_vars_2, PStarts, DStarts):
    import gurobipy as gp
    from gurobipy import GRB
    import numpy as np
    import time
    
    # インスタンスの生成
    m = gp.Model("LP_for_VRP" + instance_name)
    
    # 変数を設定
    """
    y1 : 主問題における不等式制約式iの潜在価値
    y2 : 主問題における等式制約式iの潜在価値
    """
    y1 = m.addMVar(shape=num_vars_1, lb=0.0, ub=float('inf'), vtype=GRB.CONTINUOUS, name="y1")
    y2 = m.addMVar(shape=num_vars_2, lb=-1000, ub=float('inf'), vtype=GRB.CONTINUOUS, name="y2")

    # モデルのアップデート
    m.update()
    
    # 目的関数を設定
    m.setObjective(-1 * b_leq.T @ y1 + -1 * b_eq.T @ y2, sense=gp.GRB.MAXIMIZE)
    
    # 制約条件を設定
    m.addConstr(As.T @ y1 >= 0, name="c1")
    m.addConstr(Ap.T @ y1 >= -op, name="c2")
    m.addConstr(Aq.T @ y1 >= -oq, name="c3")
    m.addConstr(Ac_leq.T @ y1 + Ac_eq.T @ y2 >= 0, name="c4")
    m.addConstr(Ar_leq.T @ y1 + Ar_eq.T @ y2 >= 0, name="c5")

    # モデルのアップデート
    m.update()
    
    # 時間計測スタート
    start = time.time()
    
    # ホットスタートの使用
    for i, var in enumerate(m.getVars()):
        var.PStart = PStarts[i]
    for i, constr in enumerate(m.getConstrs()):
        constr.DStart = DStarts[i]
    
    # パラメータの設定
    m.Params.Presolve = 0
    m.Params.Method = 0
    #m.Params.Crossover = 4
    #m.Params.Displayinterval = 2**31-1
    
    # 最適化
    m.optimize()
    
    # 時間計測ストップ
    elapsed_time = time.time() - start
    
    # 解の表示
    """if m.Status == gp.GRB.OPTIMAL:
        for i in range(num_vars):
            print(f"主問題における制約{i}の潜在価格は、{y[i].X}")
        print("最適値 : ", m.ObjVal)
    print('\033[34m'+f"実時間\t{elapsed_time}"+'\033[0m')"""
    
    # モデルをテキストファイルにする
    m.write("out"+instance_name+".mst")
        
    return m