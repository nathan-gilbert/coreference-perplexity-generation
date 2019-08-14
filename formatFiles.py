#!/usr/bin/python
# File Name : formatFile.py
# Purpose : Add sentence markers to text files
# Creation Date : 03-07-2012
# Last Modified : Wed 07 Mar 2012 02:43:43 PM MST
# Created By : Nathan Gilbert
#
import sys
import glob
import os

import nltk.data
from nltk.tokenize import *


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <dir>" % (sys.argv[0])
        sys.exit(1)

    files=[]
    for infile in glob.glob(os.path.join(sys.argv[1], '*.txt')):
        files.append(infile.replace(sys.argv[1], ""))

    sentence_splitter = nltk.data.load('tokenizers/punkt/english.pickle')

    for f in files:
        infile = open(sys.argv[1]+"/"+f, 'r')
        lines = ''.join(infile.readlines())
        infile.close()

        outfile = open(sys.argv[1]+"/"+f, 'w')
        sentences = sentence_splitter.tokenize(lines)

        for s in sentences:
            outfile.write("<s> %s </s>\n" % (s.strip()))

        outfile.close()
