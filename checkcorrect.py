#!/usr/bin/python3

import getpass
import os
import subprocess
import sys
import signal
import re

#usage: checkcorrect.py <ngramversion> [<inputfile>]
#if no inputfile provided, it defaults to shakespeareAllLines
#This script checks to see if your program produces
#correct output on the input file, forming ngrams of length two.
#It does not check execution time.  It first uses the make utility
#to create the ngram version and then invokes the ngram version
#like this: ./ngram -b <filename>
#
# possible inputs are: shakespeare100Lines, shakespeare500Lines
#                      shakespeare1000Lines, shakespeareAllLines
#
#location of the input files
labdir="/u/css/classes/3482/191/lab3/"
#location of the temp directory used by the script
tmpdir = "/var/tmp/toollab." + getpass.getuser();

#If the ngram code runs for more than 30 seconds, this 
#handler will execute, which will kill the ngram process.
def handler(signum, frame):
    global ngramProc;
    print("\n" u'\u166D' + " Program is taking more than 30.0 seconds to complete.");
    print("Aborting execution.");
    print("Result can be found in " + tmpdir);
    ngramProc.kill();
    sys.exit(0);

#Prints information about how to use the script.
def printUsage():
    print("\nUsage: checkcorrect.py <ngram version> [<input file>]");
    print("<ngram version>:  version of ngram to use, for example, ngramfast");
    print("       checkcorrect.py will use the makefile to create the executable");
    print("<input file> should be either: shakespeare100Lines, shakespeare500Lines,");
    print("       or shakespeare1000Lines or shakespeareAllLines");
    print("       <input file> defaults to shakespeareAllLines");
    sys.exit(0);

#Creates the temp directory.  Creates the ngram version by
#using make and the makefile. Moves executable to the
#temp directory.  Changes to the temp directory.
#Creates a link to the inputfile.
def setup(version, inputFile):
    #remove old temp directory
    if (os.path.isdir(tmpdir)):
        subprocess.call(["rm", "-f", "-r", tmpdir]);
    #make new temp directory
    subprocess.call(["mkdir", tmpdir]);
    #make the ngram version
    if (not os.path.exists(version)):
        subprocess.call(["make", "clean"]);
        os.system("make " + version);
        if (not os.path.exists(version)):
            print("\nmake failed: unable to create " + version);
            print("Exiting.");   
            sys.exit(0);
    #move ngram version to temp directory
    subprocess.call(["mv", version, tmpdir]);
    #change to temp directory and add a link to the input file
    os.chdir(tmpdir);
    subprocess.call(["ln", "-s", labdir + inputFile, inputFile]);

#Runs the ngram version on the input file, directing the output
#to inputfile.output.
def runCode(version, inputFile):
    global ngramProc;
    version = "./" + version;
    print("Running: " + version + " -b " + inputFile + " > " + inputFile + ".output");
    signal.alarm(30);
    with open(inputFile + ".output", "wb", 0) as out:
        ngramProc = subprocess.Popen([version, "-b", inputFile], stdout=out);
    out.close();
    ngramProc.wait();

#Check to see if the output file is ordered properly.  The first
#half of the file needs to contain the ngrams in increasing order.
#The second half of the file needs to contain the ngrams in
#decreasing order.
def checkIfSorted(inputFile):
    increasing = True;
    fileHandle = open(inputFile + ".output", "r");
    lines = fileHandle.readlines();
    prevCount=0;
    print("Checking order of ngrams in " + inputFile + ".output");
    for line in lines:
        match = re.match(r"^(.+), (\d+)$", line);
        if match:
            nextCount = int(match.group(2));
            if (increasing):
                if (nextCount < prevCount):
                    print("\n" + u'\u166D' + " First half of output file not in increasing order by count");
                    print("Result can be found in " + tmpdir);
                    sys.exit(0);
            else:   #decreasing
                if (nextCount > prevCount):
                    print("\n" + u'\u166D' + " Second half of output file not in decreasing order by count");
                    print("Result can be found in " + tmpdir);
                    sys.exit(0);
            prevCount = nextCount;
        else:
            #when the word Decreasing is found, change from increasing to
            #looking for decreasing
            match = re.match(r"^Decreasing", line);
            if match:
                increasing = False;
    fileHandle.close();

#This function sorts the output and compares the sorted output
#to the equivalent sorted output in the instructor's directory.
#The two files should be identical.
def checkForMissingLines(inputFile):
    studentfile = inputFile + ".output.sorted"
    instructorfile = labdir + inputFile + ".output.sorted"
    #sort the student's output file
    with open(studentfile, "wb", 0) as out:
        sortProc = subprocess.Popen(["sort", inputFile + ".output"], stdout=out);
    sortProc.wait();
    out.close();
    #use diff command to compare the instructor and the student output
    print("Running: diff " + studentfile + " " + instructorfile + " > diffFile");
    with open("diffFile", "wb", 0) as out:
        diffProc = subprocess.Popen(["diff", studentfile, instructorfile], stdout=out);
    diffProc.wait();
    out.close();
    #if identical, the size should be 0
    size = os.path.getsize("diffFile");
    if (size != 0):
       print("\n" u'\u166D' + " Output is incorrect.");
       print("Result can be found in " + tmpdir);
       sys.exit(0);

#Calls the functions that perform each step of the process.
def main():
    if (len(sys.argv) < 2 or len(sys.argv) > 3):
        printUsage()   
    #get name of executable
    version = sys.argv[1];
    #get name of input file
    if (len(sys.argv) < 3):
       inputFile = "shakespeareAllLines"
    else:
       inputFile = sys.argv[2];
    #make sure input file is one of the files provided by instructor
    if (inputFile != "shakespeare100Lines" and inputFile != "shakespeare500Lines" and\
        inputFile != "shakespeare1000Lines" and inputFile != "shakespeareAllLines"):
        printUsage();   
    #create the temp directory, compile code, copy files to temp directory
    setup(version, inputFile);
    #run the code
    runCode(version, inputFile);
    #check to see if the first half of the file is in increasing order
    #and the second half of the file is in decreasing order
    checkIfSorted(inputFile);
    #check to make sure no lines are missing
    checkForMissingLines(inputFile);
    print("\n" + u'\N{check mark}' + " " + version + " -b " + inputFile + " produces correct output.");

#install the alarm signal handlerr
#transfer control to main
if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    main()

