#include <bits/stdc++.h>
using namespace std;

const vector<int> Color = {0,1,2,3,4,5,6,7};
struct vertex{
    int name;
    int degree;
    vector<pair<int, int>> edges;
};

void graph_coloring(vector<int> V, vector<pair<int,int>> E, vector<int>& Colored);
vector<vertex> sort_by_degrees(vector<int>& V, vector<pair<int,int>>& E);
void combine(vector<int> V, vector<pair<int, int>> E, vector<vertex>& Descending, vector<int> Degree);
vector<int> domain(int node, vector<pair<int, int>> edges, vector<int> Colored);
void assign(int node, vector<int> Domain, vector<int>& Colored);

int main(){
    vector<int> V = {0,1,2,3,4,5,6,7};
    vector<pair<int,int>> E = {make_pair(0,1), make_pair(0,2), make_pair(0,3), make_pair(1,3), make_pair(3,4), make_pair(5,6)};
    vector<int> Colored(V.size(), -1);

    graph_coloring(V, E, Colored);

    for(auto&& node : Colored){
        cout << node << endl;
    }
}

void graph_coloring(vector<int> V, vector<pair<int,int>> E, vector<int>& Colored){
    //ノードを次数が高い順に並べ替える
    vector<vertex> Descending = sort_by_degrees(V, E);

    for(auto&& max_node : Descending){
        // 1. 最も次数の高いノードを見つける = max_node
        // 2. 1で選んだノードに色を割り当てる
        //// 2.1 ノードのドメインを求める
        vector<int> Domain = domain(max_node.name, max_node.edges, Colored);
        //// 2.2 ドメインから適当な色を選ぶ
        //// 2.3 ノードに色を割り当てる
        assign(max_node.name, Domain, Colored);
    }
}

vector<vertex> sort_by_degrees(vector<int>& V, vector<pair<int,int>>& E){
    //ノードの次数を調べる　(ベクトルの初期化，vec(3)->vec={0,0,0})
    vector<int> Degree(V.size());
    vector<vector<int>> edge;
    for(auto&& e : E){
        Degree[e.first]++;
        Degree[e.second]++;
    }

    //(あるノードv，その次数degree，ノードvが含まれる枝の集合)　を一括りにする
    vector<vertex> Descending(V.size());
    combine(V, E, Descending, Degree);

    //並べ替える
    sort(Descending.begin(), Descending.end(), [](vertex First, vertex Second){return First.degree > Second.degree;});
    
    return Descending;
}

void combine(vector<int> V, vector<pair<int, int>> E, vector<vertex>& Descending, vector<int> Degree){
    for(int i = 0; i < V.size(); i++){
        vector<pair<int, int>> edges;
        for(auto&& edge : E){
            if(edge.first == i || edge.second == i){
                edges.push_back(edge);
            }
        }
        Descending[i].name = V[i];
        Descending[i].degree = Degree[i];
        Descending[i].edges = edges;
    }
}

vector<int> domain(int node, vector<pair<int, int>> edges, vector<int> Colored){
    vector<int> Domain = Color;
    for(auto&& edge : edges){
        if(node == edge.first && Colored[edge.second] != -1){
            Domain.erase(remove(Domain.begin(), Domain.end(), Colored[edge.second]), Domain.end());
        }
        else if(node == edge.second && Colored[edge.first] != -1){
            Domain.erase(remove(Domain.begin(), Domain.end(), Colored[edge.first]), Domain.end());
        }
    }

    return Domain;
}

void assign(int node, vector<int> Domain, vector<int>& Colored){
    Colored[node] = Domain[0];
}