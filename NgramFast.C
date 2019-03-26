#include <iostream>
#include <string>
//The vector template class is used by WordList
//You don't need to change that, but the other code you
//add cannot use vector or any other STL template classes
#include <vector>
#include "WordList.h"
#include "NgramFast.h"

using namespace std;

//Each index in the map is a linked lists of StringNodes
typedef struct StringNode{
    string key = "";
    int value = 0;
    StringNode *next = NULL;
} StringNode;

StringNode *table[500000] = {}; // Hash table, initialize to null

StringNode *sortedTable[500000] = {}; // Hash table, initialize to null

//void Ngrams::insert(string key, int val)
//{	
	
	//Hash the key and get the index
  //  int index = hash(key);

	//Create the new StringNode
//	StringNode * elem = new StringNode;

	//Assign the members
//	elem->key = key;
//	elem->value = val;
//	elem->next = NULL;  	
	
	//Detect if there is a collision
//	if(table[index] != NULL) { 
		//Create a node to store the last node in the list
		//assign the node to point to the first node, then we
		//will traverse the list to find the last
//		StringNode *last;
//		last = table[index];	//last now points to the index where the collision linked list begins
	
		//Traverse the linked list to find the end
		//Stop traversing when the next node is empty / NULL
//		while(last->next != NULL) {
//			last = last->next;
			//When we break the while loop, last SHOULD equal the last node in the list
//		}
//		last->next = elem;		
//	} //else no collision
//	else {
//		table[index] = elem;
//	}
//}

void Ngrams::insert(string key, int val)
{
    int index = hash(key);
    StringNode * elem = new StringNode;
    elem->key = key;
    elem->value = val;
    elem->next = NULL;

    if(table[index] != NULL)
    {
        elem->next = table[index];
        table[index] = elem;
    }
    else
    {
        table[index] = elem;
    }
}

int Ngrams::hash(string key)
{
    unsigned long hash = 5381;

    for (int index = 0; index < key.length(); index++)
        hash = ((hash << 5) + hash) + (int)key[index]; 

    return (hash%500000);
}


int Ngrams::find(string key)
{
	// Find method.
    int findKey = hash(key);	
	StringNode * last = new StringNode;
	last = table[findKey];	//assign the node to the first index	
		while(last != NULL) {
			if(last->key == key) return 1;
			last = last->next;
	}	return 0;
}


/*
 * Ngrams
 *
 * takes as input the size of the ngrams to be built and the list  
 * of words to build the ngrams from and builds a linked list of 
 * ngrams.
 *
 * param: int ngramSz - size of the ngram
 * param: const WordList & wl - list of the words use
 */
Ngrams::Ngrams(int ngramSz, const WordList & wl)
{
    //ADD any code you need to initialize whatever structure
    //you use for your ngram

	for(int i = 0; i < 500000; i++) {
		table[i] = NULL;
		sortedTable[i] = NULL;
	}

    this->ngramSz = ngramSz;
    WordList::const_iterator p;
    p = wl.begin();
    while (p != wl.end())
    {
        std::string ngram = getNextNgram(p, wl.end());
        p++;
        if (!ngram.empty()) insertNgram(ngram);
    }
}


/*
 * Ngrams destructor
 *
 * automatically called when Ngrams object goes out of scope
 * should delete any space dynamically allocated for the ngram
 */
Ngrams::~Ngrams()
{

}

/*
 * getNextNgram
 *
 * takes as input an iterator that points to the word to start the
 * ngram and an iterator that points to the end of the word list
 * and builds and returns the ngram. returns empty string if no
 * ngram can be built, for example, if there are insufficient words
 * to build one.
 *
 * param: WordList::const_iterator start - points to first word in ngram
 * param: WordList::const_iterator end - points to end of word list
 * return: std::string - returns ngram or empty string
 */
std::string Ngrams::getNextNgram(WordList::const_iterator start, 
        WordList::const_iterator end)
{
    //DON'T modify any of this code
    int i, len;
    std::string ngram = "";
    for (i = 0; i < ngramSz && start != end; i++)
    {
        std::string word = (*start);
        //see if the string ends with punctuation
        //don't create ngrams that continue after punctuation
        if (!isalpha(word[word.length()-1]) && i < ngramSz - 1) return "";

        //take off all ending punctuation
        len = word.length() - 1;
        while (len >= 0 && !isalpha(word[len])) 
        {
            //remove last character
            word = word.substr(0, word.length() - 1);
            len--;
        }
        if (len < 0) return "";  //give up

        //is the first word in the ngram?
        if (ngram == "") ngram = word;
        else ngram = ngram + " " + word;

        start++;
    }

    //could we build a long enough ngram?
    if (i < ngramSz) return "";

    //take off beginning punctuation
    while (ngram.length() > 0 && !isalpha(ngram[0])) 
        ngram = ngram.substr(1, ngram.length());
    return ngram;
}


/*
 * insertNgram
 *
 * Inserts ngram into whatever structure you choose to hold
 * your ngrams.
 *
 * param: std::string s - ngram to be inserted
 * return: none
 */
void Ngrams::insertNgram(std::string s)
{
	//ADD code to insert ngram in whatever structure you choose
    if (find(s) == 0) {
		//The key is not found, so insert
        insert(s,1);
    } else {
		//The key is present already, so just increment it		
		StringNode *traverse = table[hash(s)];
        while(traverse != NULL)
        {
            if(traverse->key == s)
            {
                (traverse->value)++;
            }
			traverse = traverse -> next;
        }                                                    
    }
	
}

/*
 * printIncreasing
 *
 * prints the list of ngrams in increasing order
 *
 */
void Ngrams::printIncreasing()
{
    sort();
	std::cout << "\nIncreasing list of " << ngramSz << " word ngrams and counts\n";
    std::cout << "-------------------------------------------\n";
    //ADD code to print the ngrams in increasing order of count
    for (int i = 0; i < 500000; i++) 
    { 
		//Create a pointer to traverse the collision lists
		StringNode * last;
		last = sortedTable[i];	//assign the node to the first index
		
		while(last != NULL) {
			cout << last->key << ", " << last->value << endl;
			last = last->next;
		}
    }	
}
/*
 * printIncreasing
 *
 * prints the list of ngrams in decreasing order
 *
 */
void Ngrams::printDecreasing()
{
    //sort();
	std::cout << "\nDecreasing list of " << ngramSz << " word ngrams and counts\n";
    std::cout << "-------------------------------------------\n";
    //ADD code to print the ngrams in increasing order of count
	//For each index in the table
    for (int i = 500000-1; i >= 0; i--) 
    {
        //cout << i << endl;
		//Create a pointer to traverse the collision lists
		StringNode * last;
		last = sortedTable[i];	//assign the node to the first index
		
		if (last != NULL) {
			while(last != NULL) {
				cout << last->key << ", " << last->value << endl;
				last = last->next;
			}
		}
    }	
}

// Sorting is actually pretty simple.  You'll have a bunch of ngrams with the same count.  
// Those don't need to be in any particular order; they just need to be together in the sorted output.  
// After you've built the first set of linked lists, 
// you'll take all of those nodes in those linked lists and put each of them in another linked list based upon their count.  
// All nodes with a count of 1 will be in one linked list, all nodes in with a count of two will be in another linked list, etc.  
// You can just put the node in the front of the linked list since they can be in any order
//void Ngrams::sort()
//{
	
	//For each index in the table
//    for (int i = 500000-1; i >= 0; i--) 
//    {
        //Create a pointer to traverse the collision lists
//		StringNode * last = new StringNode;
//		StringNode * tv = new StringNode;
//		last = table[i];	//assign the node to the first index
		
//		if (last != NULL) {
			
//			while(last != NULL) {
//				if(sortedTable[last->value] == NULL) {
					//cout << "stored fresh element" << endl;
//					sortedTable[last->value] = last;
//				} else {
//					tv = sortedTable[last->value];
//					while(tv->next != NULL) {
//						tv = tv->next;
//					}
//					tv->next = last;
//				}
//				last = last->next;
//			}
//		}
  //  }	
//}
	
void Ngrams::sort()
{
    for(int i = 0; i < 500000;i++)
    {   
        StringNode * indexPtr = table[i];
		StringNode *temp;

        while(indexPtr != NULL)
        {
			
			temp = indexPtr->next;
			
			if(sortedTable[indexPtr->value] == NULL) {
				sortedTable[indexPtr->value] = indexPtr;
			} else {
				indexPtr->next = sortedTable[indexPtr->value];
				sortedTable[indexPtr->value] = indexPtr;
				
			}
			
			indexPtr = temp;
        }
    }
}
