#!/usr/bin/python3

import getpass
import os
import subprocess
import sys
import signal
import re

#usage: checkmem.py <ngramversion> 
#This script uses the valgrind tool to see if your program
#contains memory errors. It will first use make to
#create the ngram version.  Then, it will run the program
#using valgrind.  Finally, it will examine the 
#output file for evidence of memory errors.
#
#Location of input file
labdir="/u/css/classes/3482/191/lab3/"
#Temp directory used to hold the executable and valgrind files
tmpdir = "/var/tmp/toollab." + getpass.getuser();
#name of input file
inputFile = "shakespeare1000Lines"

#If the ngram code runs for more than 30 seconds, this 
#handler will execute, which will kill the ngram process.
def handler(signum, frame):
    global ngramProc;
    print("\n" u'\u166D' + " Program is taking more than 30.0 seconds to complete.");
    print("Aborting execution.\n");
    ngramProc.kill();
    sys.exit(0);

#Prints information about how to use the script.
def printUsage():
    print("\nUsage: checkmem.py <ngram version>");
    print("<ngram version>:  version of ngram to use, for example, ngramfast");
    print("       checkmem.py will use the makefile to create the executable")
    print("       checkmem.py uses shakespeare1000Lines as input to the ngram code");
    sys.exit(0);

#Creates the temp directory.  Creates the ngram version by
#using make and the makefile. Moves executable to the
#temp directory.  Changes to the temp directory.
#Creates a link to the inputfile.
def setup(version, inputFile):
    #delete old temp directory and create a new one
    if (os.path.isdir(tmpdir)):
        subprocess.call(["rm", "-f", "-r", tmpdir]);
    subprocess.call(["mkdir", tmpdir]);
    #compile the code
    if (not os.path.exists(version)):
        subprocess.call(["make", "clean"]);
        os.system("make " + version);
        if (not os.path.exists(version)):
            print("\nmake failed: unable to create " + version);
            print("Exiting.");   
            sys.exit(0);
    #move code to temp directory
    subprocess.call(["mv", version, tmpdir]);
    #change to temp directory and add a symbolic link to the input file
    os.chdir(tmpdir);
    subprocess.call(["ln", "-s", labdir + inputFile, inputFile]);

#Runs the ngram version using valgrind on the input file, directing the output
#to inputfile.output. 
def runCode(version, inputFile):
    global ngramProc;
    version = "./" + version;
    #use valgrind to run the process
    print("Running: valgrind --tool=memcheck --leak-check=full " +\
          version + " -b " + inputFile + " > " + inputFile + ".output 2> valgrind.output");
    signal.alarm(30);
    command = ["valgrind", "--tool=memcheck", "--leak-check=full", version, "-b", inputFile];
    with open(inputFile + ".output", "wb", 0) as pout, open("valgrind.output", "wb", 0) as vout:
        ngramProc = subprocess.Popen(command, stdout=pout, stderr=vout);
    ngramProc.wait();
    pout.close();
    vout.close();

#Checks the output file produced by valgrind for memory errors
def checkForMemError(version, inputFile):
    fileHandle = open("valgrind.output", "r");
    lines = fileHandle.readlines();
    #the number after ERROR SUMMARY: should be 0 if no errors
    for line in lines:
        match = re.match(r"^==\d+== ERROR SUMMARY: (\d+) errors", line);
        if (match and (int(match.group(1)) != 0)):
            print("\n" + u'\u166D' + " " + version + " produced " + match.group(1) + " memory errors.");
            print("Result can be found in " + tmpdir);
            sys.exit(0);

#Calls the functions that perform each step of the process.
def main():
    global inputFile
    if (len(sys.argv) != 2):
        printUsage()   
    version = sys.argv[1];
    #create the temp directory, compile code, copy files to temp directory
    setup(version, inputFile);
    #run the code using valgrind
    runCode(version, inputFile);
    #check the valgrind output file for memory errors
    checkForMemError(version, inputFile);
    print("\n" + u'\N{check mark}' + " " + version + " produces no memory errors.");

#install the alarm signal handlerr
#transfer control to main
if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    main()

