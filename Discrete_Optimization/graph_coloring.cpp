#include <bits/stdc++.h>
using namespace std;

void graph_coloring(vector<int> V, vector<pair<int,int>> E, vector<int>& Colored);

void main(){
    vector<int> V = {0,1,2,3,4,5,6,7};
    vector<pair<int,int>> E = {make_pair(0,1), make_pair(0,2), make_pair(0,3), make_pair(1,3), make_pair(3,4), make_pair(5,6)};
    vector<int> Colored;

    graph_coloring(V, E, Colored);

    for(auto&& node : Colored){
        cout << node << endl;
    }
}

void graph_coloring(vector<int> V, vector<pair<int,int>> E, vector<int>& Colored){
    //最も次数の高いノードを見つける
    //それに色を割り当てる
}