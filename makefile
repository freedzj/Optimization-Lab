CC = g++ 
#CFLAGS = $(PFLAG) -O2 -c -std=c++11
#If you want to use the debugger, uncomment the CFLAGS below
#and comment out the one above.
CFLAGS = $(PFLAG) -g -c -std=c++11
OBJS = Ngrams.o WordList.o main.o
LFLAGS = $(PFLAG) -pg

.C.o:
	$(CC) $(CFLAGS) $< -o $@

#You can modify this makefile to support more 
#ngram version.  You will need to give it
#a name (for example, NGRAMV3) that is used in
#main.C.  Use the examples in this makefile as
#your guide.
#Don't forget to also add the name
#of the target to the clean command.
#Also, you will need to change the main.C so that it
#will include the header file for your new ngram
#version.

ngramfast: WordList.o NgramFast.o
	$(CC) $(CFLAGS) -DNGRAMFAST main.C -o main.o
	$(CC) $(LFLAGS) WordList.o NgramFast.o main.o -o ngramfast

ngramslow: WordList.o NgramSlow.o
	$(CC) $(CFLAGS) -DNGRAMSLOW main.C -o main.o
	$(CC) $(LFLAGS) WordList.o NgramSlow.o main.o -o ngramslow

ngramstl: WordList.o NgramSTL.o
	$(CC) $(CFLAGS) -DNGRAMSTL main.C -o main.o
	$(CC) $(LFLAGS) WordList.o NgramSTL.o main.o -o ngramstl

WordList.o: WordList.h

NgramFast.o: NgramFast.h WordList.h

NgramSlow.o: NgramSlow.h WordList.h

NgramSTL.o: NgramSTL.h WordList.h

clean:
	-rm -f *.o ngramfast ngramslow ngramstl gmon.out 

