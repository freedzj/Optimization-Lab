#include <string>
using namespace std;

class HashNode 
{      
    public:
    //key: ngram string
    //value: string count
    int value; 
    string key; 
    
    //Constructor of hashnode
    HashNode(string key, int value) 
    { 
        this->value = value; 
        this->key = key; 
    } 
    
}; 