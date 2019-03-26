#include "HashNode.h"
#include <string>


#define p1 54059
#define p2 76963
#define p3 86969
#define p4 57

using namespace std;

class HashMap {

private int size;
private HashNode::HashNode[] table;

public HashTable(int s)
{
    size = s;
}

public int hash(HashNode::HashNode &n)
{
    unsigned h = p4
    while(*n.str){
        h = (h*p1)^(s[0] * p2);
        s++;
    }
    return h % p3;
}

public void put(HashNode::HashNode &n)
{
    int index = hash(n.str);
    table[index] = n;
}

public string get(int key)
{
    return table[key];
}

public bool containsValue(int key)
{
    if(table[key] != null)
    {
        return true;
    }
    else
    {
        return false
    }

}

}
