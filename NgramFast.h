//You will need to add one or more typedefs and
//declarations for whatever structure you use to hold
//your ngrams.
class Ngrams 
{
    private:
        int ngramSz;
        std::string getNextNgram(WordList::const_iterator start, 
                WordList::const_iterator end);
        void insertNgram(std::string s);
        void insert(std::string key, int val);     
        int hash(std::string key);
        int find(std::string key);
        void sort();
    public:
        Ngrams(int ngramSz, const WordList & wl);
        ~Ngrams();
        void printIncreasing();
        void printDecreasing();
};

