#!/usr/bin/python
# File Name : type_count.py
# Purpose : Count the "type" found in a corpus
# Creation Date : 03-09-2012
# Last Modified : Fri 09 Mar 2012 12:11:10 PM MST
# Created By : Nathan Gilbert
#
import sys
import os
import glob

import nltk

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <corpus_dir>" % (sys.argv[0])
        sys.exit(1)

    files = []
    counts = {}
    total_tokens = 0
    for infile in glob.glob(os.path.join(sys.argv[1], '*.txt')):
        files.append(infile.replace(sys.argv[1], ""))

    for f in files:
        txt_file = open(sys.argv[1]+"/"+f, 'r')
        lines = ''.join(txt_file.readlines())

        tokens = nltk.word_tokenize(lines)
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
            total_tokens += 1

    print "Total types: %d" % (len(counts.keys()))
    print "Total tokens: %d" % (total_tokens)

