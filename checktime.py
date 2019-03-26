#!/usr/bin/python3

import sys
import signal
import getpass
import os
import subprocess
import re

#usage: checktime.py <ngramversion> 
#This script checks to see how long the ngramversion takes
#to produce output using the input file shakespeareAllLines
#It first uses the make utility to create the ngram version 
#with the -pg flag so that profiling will be performed
#when the program is executed.
#It then invokes the ngram version
#like this: ./ngram -b shakespeareAllLines
#After that, it uses gprof to generate profiling information.
#Then, it examines the gprof output file to get the 
#execution time.
#
#location of the input file
shakeFile = "/u/css/classes/3482/191/lab3/shakespeareAllLines"
#location of the temp directory used by the script 
tmpdir = "/var/tmp/toollab." + getpass.getuser();

#If the ngram code runs for more than 30 seconds, this 
#handler will execute, which will kill the ngram process.
def handler(signum, frame):
    global ngramProc;
    print("\n" u'\u166D' + " Program is taking more than 30.0 seconds to complete.");
    print("Aborting execution.");
    ngramProc.kill();
    sys.exit(0);

#Prints information about how to use the script.
def printUsage():
    print("\nUsage: checktime.py <ngram version>");
    print("<ngram version>:  version of ngram to use, for example, ngramfast");
    print("       checktime.py will use the makefile to create the executable")
    print("       checktime.py uses shakespeareAllLines as input to the ngram code");
    sys.exit(0);

#Creates the temp directory.  Creates the ngram version by
#using make and the makefile. Moves executable to the
#temp directory.  Changes to the temp directory.
#Creates a link to the inputfile.
def setup(version):
    global shakeFile;
    global tmpdir;
    #remove old temp file and create a new one 
    if (os.path.isdir(tmpdir)):
        subprocess.call(["rm", "-f", "-r", tmpdir]);
    subprocess.call(["mkdir", tmpdir]);
    #create the version using the -pg option so that
    #the executable can be profiled
    subprocess.call(["make", "clean"]);
    os.system("make PFLAG=-pg " + version);
    if (not os.path.exists(version)):
        print("\nmake failed: unable to create " + version);
        print("Exiting.");   
        sys.exit(0);
    #move executable to temp directory
    subprocess.call(["mv", version, tmpdir]);
    #change to temp directory and add a link to the shakespeareAllLine file
    os.chdir(tmpdir);
    subprocess.call(["ln", "-s", shakeFile, "shakespeareAllLines"]);

#Runs the ngram version on shakespeareAllLine directing the output to 
#shakespeareAllLine.output.  Then it runs gprof to produce the profiling
#information. Finally, it calls getTime to obtain the execution time
#from gprof.output
def runCode(version):
    global ngramProc;
    version = "./" + version;
    print("Running: " + version + " -b shakespeareAllLines > shakespeareAllLines.output");
    signal.alarm(30);
    #Run code on shakespeareAllLines
    with open(version + ".output", "wb", 0) as out:
        ngramProc = subprocess.Popen([version, "-b", "shakespeareAllLines"], stdout=out);
    out.close();
    ngramProc.wait();
    print("Profiling: " + "gprof " + version + " > gprof.output");
    #Run gprof to get profiling information. Direct output to gprof.output
    with open("gprof.output", "wb", 0) as out:
        profProc = subprocess.Popen(["gprof", version], stdout=out);
    profProc.wait();
    out.close();
    #Get execution time from gprof.output
    return getTime("gprof.output");

#open the file that contains the gprof output and read it, looking
#for the line that begins with granularity.  This line contains
#the execution time of the code.
def getTime(gprofFilename):
    fileHandle = open(gprofFilename, "r");
    lines = fileHandle.readlines();
    for line in lines:
       #the line that begins with granularity contains the execution time
       match = re.match(r"^granularity: .+ of (.+) seconds$", line);
       if match: 
          return match.group(1);
    print("\n" u'\u166D' + " Unable to find execution time in " + gprofFilename);
    print("Result can be found in " + tmpdir);
    return 0;
    
#Calls the functions that perform each step of the process.
def main():
    if (len(sys.argv) != 2):
        printUsage()   
    version = sys.argv[1];
    #create the temp directory, compile code, copy files to temp directory
    setup(version);
    #run the code and gprof and get the profiling information
    time = runCode(version);
    print("\n" + version + " takes " + time + " seconds to complete.\n");

#install the alarm signal handlerr
#transfer control to main
if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    main()

