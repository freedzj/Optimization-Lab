#ifndef NGRAM_H_
#define NGRAM_H_
#include <map>

using namespace std;

class Ngrams 
{
   private:
      int ngramSz;
      std::string getNextNgram(WordList::const_iterator start, 
                               WordList::const_iterator end);
      void insertNgram(std::string s);
      map<string,int> nGrams;
      multimap<int,string> nGramsSorted;
      void sortMap();      
   public:
      Ngrams(int ngramSz, const WordList & wl);
      ~Ngrams();
      void printIncreasing();
      void printDecreasing();
};



#endif
