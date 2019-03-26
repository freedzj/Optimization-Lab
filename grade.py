#!/usr/bin/python3

import getpass
import os
import subprocess
import sys
import signal
import re

#usage: grade.py <ngramversion> 
#This program uses checkmem.py, checkcorrect.py, and checktime.py to
#grade the ngram version.  Specifically, it calls:
#
# ./checkcorrect.py <ngramversion> shakespeare1000Lines                     
# ./checkmem.py <ngramversion> 
#       checkmem.py always checks for memory errors using shakespeare1000Lines
# ./checktime.py <ngramversion>
#       checktime.py always checks for timing using shakespeareAllLines
#
# The grade is calculated out of 50 points.
# If the progam doesn't produce correct output, the grade is 0.
# +40 if time is less than 1 second
# +20 if the time is more than 1 second but less than 30 seconds
# +10 if the program does not contain memory errors
#
labdir="/u/css/classes/3482/191/lab3/"
tmpdir = "/var/tmp/toollab." + getpass.getuser();

#print usage information
def printUsage():
    print("\nUsage: grade.py <ngram version>");
    print("grade.py runs the following scripts:");
    print("./checkcorrect.py <ngram version> shakespeare1000Lines");                     
    print("./checkmem.py <ngram version>");
    print("     -checkmem.py uses shakespeare1000Lines");
    print("./checktime.py <ngram version>");
    print("     -checktime.py uses shakespeareAllLines");
    print("\nThe grade is calculated out of 50 points.");
    print("      0 - <ngram version> produced incorrect results.");
    print("    If the output is correct:");
    print("    +10 - <ngram version> has no memory errors");
    print("    +20 - <ngram version> completes in less than 30 seconds, but more than 1 second");
    print("    +40 - <ngram version> completes in less than 1 second");
    sys.exit(0);

#Check if ngram version produces the correct output on shakespeare1000Lines
#Use the checkcorrect.py script to perform the check.
def checkCorrectness(version):
    inputFile = "shakespeare1000Lines"
    with open("grade.output", "wb", 0) as out:
        corrProc = subprocess.Popen(["./checkcorrect.py", version, inputFile], stdout=out);
    corrProc.wait();
    out.close();
    fileHandle = open("grade.output", "r");
    lines = fileHandle.readlines();
    os.remove("grade.output");
    for line in lines:
       match = re.match(r".+ produces correct output.$", line)
       if (match):
          print(u'\N{check mark}' + " " + version + " -b " + inputFile + " produces correct output.");
          return 1;
    print(u'\u166D' + " " + version + " -b " + inputFile + " does not produce correct output.");
    return 0;

#Check if ngram version generates memory errors on shakespeare1000Lines
#Use the checkmem.py script to perform the check.
def checkMemoryErrors(version):
    inputFile = "shakespeare1000Lines"
    with open("grade.output", "wb", 0) as out:
        corrProc = subprocess.Popen(["./checkmem.py", version], stdout=out);
    corrProc.wait();
    out.close();
    fileHandle = open("grade.output", "r");
    lines = fileHandle.readlines();
    os.remove("grade.output");
    for line in lines:
       match = re.match(r".+ produces no memory errors.$", line)
       if (match):
          print(u'\N{check mark}' + " " + version + " -b " + inputFile + " produces no memory errors.");
          return 0;
    print(u'\u166D' + " " + version + " -b " + inputFile + " produces memory errors.");
    return 1;

#Check the time of ngram version on shakespeareAllLines
#Use the checktime.py script to perform the check.
def checkTime(version):
    inputFile = "shakespeareAllines"
    with open("grade.output", "wb", 0) as out:
        corrProc = subprocess.Popen(["./checktime.py", version], stdout=out);
    corrProc.wait();
    out.close();
    fileHandle = open("grade.output", "r");
    lines = fileHandle.readlines();
    os.remove("grade.output");
    for line in lines:
       match = re.match(r".+ (\d+\.\d+) seconds to complete.$", line)
       if (match):
          xtimeStr = match.group(1);
          xtime = float(xtimeStr);
          if (xtime < 1.0):
              print(u'\N{check mark}' + " " + version + " -b " + inputFile + " completes in " + xtimeStr + " seconds.");
          elif (xtime < 30.0):
              print(u'\u166D' + " " + version + " -b " + inputFile + " completes in " + xtimeStr + " seconds.");
          else:
              print(u'\u166D' + " " + version + " -b " + inputFile + " completes in over " + xtimeStr + " seconds.");
          return xtime;
    return 1000.0;   

#calculate the grade
def calculateGrade(correct, memerr, time):
    if (correct == 0):
       print("Correctness: -50");
       return 0;
    grade = 50; 
    if (time >= 30.0):
       print("Timing: -40");
       grade = grade - 40;
    elif (time >= 1.0):
       print("Timing: -20");
       grade = grade - 20;
    if (memerr):
       print("Memory Error: -10");
       grade = grade - 10;
    return grade;

#invokes the functions that perform each step of the process
def main():
    if (len(sys.argv) != 2):
        printUsage()
    #get the ngram version
    version = sys.argv[1];
    #check if it produces correct output
    correct = checkCorrectness(version);
    #check if it produces memory errors
    memerr = checkMemoryErrors(version);
    #check how long it takes to execute on shakespeareAllLines
    time = checkTime(version);
    #calculate the grade
    grade = calculateGrade(correct, memerr, time);
    print("Grade: " + str(grade) + "/50");

#transfer control to main
if __name__ == "__main__":
    main()

