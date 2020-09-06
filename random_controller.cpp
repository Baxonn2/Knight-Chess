#include <iostream>
#include <queue>
#include <list>
#include <map>
#include <fstream>
#include <iostream>
#include <sstream>

//#include <json/value.h>

#include "json.hpp"

// for convenience
using json = nlohmann::json;





using namespace std;

class State{
public:

    int table[8][8];
    
    State(){
        for(int i=0;i<8;i++)
            for(int j=0;j<8;j++) {
              table[i][j]=0;
            }
    }

    
    void add_knight(int i, int j, int knight){
        table[i][j]=knight;
    }

    void rem_knight(int i, int j){
        table[i][j]=0;
    }

};

std::ostream &operator<<(std::ostream &os, const State &s) { 
    for(int i=0;i<8;i++){
        for(int j=0;j<8;j++){
                if (s.table[i][j]!=0)
                    os << s.table[i][j] << " ";
                else 
                    os << "000 ";
        }
        os << endl;
    } 
}



#include <sys/time.h>

int main(int argc, char **argv){
    struct timeval time; 
    gettimeofday(&time,NULL);

     // microsecond has 1 000 000
     // Assuming you did not need quite that accuracy
     // Also do not assume the system clock has that accuracy.
    srand((time.tv_sec * 1000) + (time.tv_usec / 1000));

    std::stringstream jsonfile;
    json json_object;
    
    jsonfile << argv[1];
    jsonfile >> json_object;
    
    // if current_player='1' is white
    // else is black
    char current_player = json_object["my_knights_dict"].items().begin().key()[0];

    //a state is created
    State s;
    for(int i=0;i<8;i++){
        for(int j=0;j<8;j++){
            json id = json_object["ids"][i][j];
            string id_str = id.dump();
            if (id_str!="null")
                s.add_knight(i,j,stoi(id_str));
            
        }
    }

    //cout << s << endl; //for printing the table

    int size = json_object["my_knights_dict"].size();
    auto it = json_object["my_knights_dict"].items().begin();
    advance(it,rand()%size);

    cout << "{" << endl;
    cout << "    \"knight_id\": "  << stoi(it.key()) << "," << endl;
    cout << "    \"knight_movement\": " << rand()%7 << endl;
    cout << "}" << endl;

}