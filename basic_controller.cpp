#include <iostream>
#include <queue>
#include <list>
#include <map>
//#include <json/value.h>

#include "json.hpp"

// for convenience
using json = nlohmann::json;



#include <fstream>
#include <iostream>

using namespace std;

class Move{
    public:
    int ii,jj,i,j;
    Move (): ii(-1),jj(-1),i(-1),j(-1){}
    Move(int ii,int jj, int i, int j):ii(ii),jj(jj),i(i),j(j) { }
};

class State{
public:

    int table[8][8];
    int opponent_at[8][8];
    int player_at[8][8];

    map< pair<int,int>, int > actions;
    
    
    State(){
        for(int i=0;i<8;i++)
            for(int j=0;j<8;j++) {
              table[i][j]=0;
              player_at[i][j]=0;
              opponent_at[i][j]=0;
            }

        actions[make_pair(1,2)]=1;
        actions[make_pair(2,1)]=0;
        actions[make_pair(1,-2)]=6;
        actions[make_pair(-2,1)]=3;

        actions[make_pair(2,-1)]=7;
        actions[make_pair(-1,2)]=2;
        actions[make_pair(-1,-2)]=5;
        actions[make_pair(-2,-1)]=4;
    }

    void invert_players(){
        for(int i=0;i<8;i++)
            for(int j=0;j<8;j++) {
              table[i][j] = -table[i][j];
              int aux=player_at[i][j];
              player_at[i][j]=opponent_at[i][j];
              opponent_at[i][j]=aux;
            }
    }

    void update_attacks(int i, int j, int player, int val){
        for(auto a: actions){
            int ii=i+a.first.first;
            int jj=j+a.first.second;
            if(ii >=8 || ii<0) continue;
            if(jj >=8 || jj<0) continue;
            if(player==1) player_at[ii][jj]+=val;
            else opponent_at[ii][jj]-=val;
        }
    }
    
    void add_knight(int i, int j, int player){
        table[i][j]=player;
        update_attacks(i, j, player, player);
    }

    void rem_knight(int i, int j){
        update_attacks(i, j, table[i][j], -table[i][j]);
        table[i][j]=0;
    }

    void apply_move(Move m){
        if (table[m.i][m.j]!=0) rem_knight(m.i,m.j);
        add_knight(m.i,m.j,table[m.ii][m.jj]);
        rem_knight(m.ii,m.jj);
    }

    Move suggest_move(){
        //if we can eat then eat
        int attract_i=-1, attract_j=-1;
         for(int i=0;i<8;i++)
            for(int j=0;j<8;j++) {
                if(table[i][j] == -1) {attract_i=i; attract_j=j;} 
                if(player_at[i][j]>0 && table[i][j]==-1){
                    for(auto a: actions){
                        int ii=i+a.first.first;
                        int jj=j+a.first.second;
                        if(ii >=8 || ii<0) continue;
                        if(jj >=8 || jj<0) continue;
                        if(table[ii][jj] == 1)
                            return Move(ii,jj,i,j);
                        
                    }
                }
            }
        
        
        //knights move to advanced regions with attack >+1
        int best_eval=-1000;
        Move best_move;
        for(int i=0;i<8;i++)
            for(int j=0;j<8;j++)
                if(player_at[i][j] > 0 && table[i][j]==0){
                    int eval=player_at[i][j]-opponent_at[i][j];
                    for(auto a: actions){
                        int ii=i+a.first.first;
                        int jj=j+a.first.second;
                        if(ii >=8 || ii<0) continue;
                        if(jj >=8 || jj<0) continue;
                        if(table[ii][jj] == 1){
                            if(player_at[i][j]-opponent_at[i][j]>=1){
                                eval = 100 - (abs(i-attract_i)-abs(j-attract_j));
                                if(rand()%10==0) return Move(ii,jj,i,j);
                            }
                            //if(player_at[i][j]-opponent_at[i][j]>1) eval = 100 + (ii-i); //movidas que avanzan
                            if (eval>best_eval){
                                best_eval = eval;
                                best_move = Move(ii,jj,i,j);
                            }
                        }
                    }
                }
        return best_move;
    }


};

std::ostream &operator<<(std::ostream &os, const State &s) { 
    for(int i=0;i<8;i++){
        for(int j=0;j<8;j++){
                os << s.table[i][j] << " ";
        }
        os << endl;
    } 

    for(int i=0;i<8;i++){
        for(int j=0;j<8;j++){
                os << s.player_at[i][j] << " ";
        }
        os << endl;
    } 

        for(int i=0;i<8;i++){
        for(int j=0;j<8;j++){
                os << s.opponent_at[i][j] << " ";
        }
        os << endl;
    } 
}

std::ostream &operator<<(std::ostream &os, const Move &m) { 
    os << "(" <<m.ii << "," << m.jj << ") -->  ";
    os << "(" << m.i << "," << m.j << ")";
}

#include <sstream> 
#include<ctime>

int main(int argc, char **argv){
    std::stringstream jsonfile;
    //std::ifstream jsonfile("current_state.json");
    json json_object;
    
    jsonfile << argv[1];

    jsonfile >> json_object;
    
    char player = json_object["my_knights_dict"].items().begin().key()[0];
    srand(time(0));

    //cout<<json_object; //This will print the entire json object.

    //The following lines will let you access the indexed objects.
    //cout<<json_object["ids"][0]; //Prints the value for "Anna"

    //int initial_state[8][8] = {{-1,-1,-1,-1,-1,-1,-1,-1},{-1,-1,-1,-1,-1,-1,-1,-1},{0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0},
    //                            {0,0,0,0,0,0,0,0},{0,0,0,0,0,0,0,0},{1,1,1,1,1,1,1,1},{1,1,1,1,1,1,1,1}};

    State s;
    for(int i=0;i<8;i++){
        for(int j=0;j<8;j++){
            json id = json_object["ids"][i][j];
            string id_str = id.dump();
            if (id_str!="null"){
                if(id_str[0]==player)
                   s.add_knight(i,j,1);
                else 
                   s.add_knight(i,j,-1);
            }
        }
    }

    //cout << s << endl;


    
    Move m;
    m=s.suggest_move();


    cout << "{" << endl;
    cout << "    \"knight_id\": "  << json_object["ids"][m.ii][m.jj] << "," << endl;
    cout << "    \"knight_movement\": " << s.actions[make_pair(m.i-m.ii,m.j-m.jj)] << endl;
    cout << "}" << endl;
    //cout << m.i-m.ii << ","<< m.j-m.jj << endl;
    exit(1);

    
    while(true){
        m=s.suggest_move();
        cout << m << endl;
        s.apply_move(m);

        cout << s << endl; 
        cin.get();

        s.invert_players();
        m = s.suggest_move();
        cout << m << endl;
        s.apply_move(m);
        s.invert_players();
        cout << s << endl;  

        cin.get();
    }


}