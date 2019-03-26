#include <iostream>
#include <string>
//The vector template class is used by WordList
//You can also include any other includes for other
//template classes that you want to use for this version.
#include <vector>
#include "WordList.h"
#include "NgramSTL.h"


using namespace std;

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
    this->ngramSz = ngramSz;
    WordList::const_iterator p;
    p = wl.begin();
    while (p != wl.end())
    {
        std::string ngram = getNextNgram(p, wl.end());
        p++;
        if (!ngram.empty()) insertNgram(ngram);
    }
    sortMap();
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
    //deternmine if the map already contains the value

    //Get an iterator to the element we need	
    auto contains = nGrams.find(s);

    if (contains != nGrams.end()) {
        //The key is present already
        ++(contains->second);
    }
    else {
        //The key is not present
        nGrams.insert({s,1});		
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
    std::cout << "\nIncreasing list of " << ngramSz << " word ngrams and counts\n";
    std::cout << "-------------------------------------------\n";
    //ADD code to print the ngrams in increasing order of count

    //Print the map
    for (auto elem : nGramsSorted)
    {
        cout << elem.second << ", " << elem.first << endl;
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
    std::cout << "\nDecreasing list of " << ngramSz << " word ngrams and counts\n";
    std::cout << "-------------------------------------------\n";
    //ADD code to print the ngrams in increasing order of count
    auto end = nGramsSorted.rend();
    //Print the map in reverse
    for (auto iter = nGramsSorted.rbegin(); iter != end; ++iter) {
        cout << iter->second << ", " << iter->first << endl;
    }
}

/*
 * sortMap
 *
 * Sorts the map by values
 *
 */
void Ngrams::sortMap()
{
    //multimap<int,string> nGramsSorted;
    for (auto elem : nGrams)
    {
        nGramsSorted.insert({elem.second,elem.first});
    }
}
