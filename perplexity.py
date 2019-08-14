#!/usr/bin/python
# File Name : perplexity.py
# Purpose : Generate a perplexity measure for 5 fold x-val of a supplied data
# set. 
# Creation Date : 03-02-2012
# Last Modified : Wed 07 Mar 2012 03:26:13 PM MST
# Created By : Nathan Gilbert
#
import sys
import os
import glob
import random

import nltk.data
from ngram import NgramModel
from nltk.tokenize import *
from nltk.probability import LidstoneProbDist, WittenBellProbDist
from nltk.corpus import PlaintextCorpusReader

#TODO: left this with some issues regarding very high perplexity on a few
#select sentences 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <data dir> <folds>" % (sys.argv[0])
        sys.exit(1)

    #read in all the file names
    files=[]
    for infile in glob.glob(os.path.join(sys.argv[1], '*.txt')):
        files.append(infile.replace(sys.argv[1], ""))
    random.shuffle(files)

    #print len(files)
    #print files

    FOLD= int(sys.argv[2])
    start = 0
    holdOut = int(round(len(files) / FOLD))
    end = holdOut
    sentence_splitter = nltk.data.load('tokenizers/punkt/english.pickle')

    FOLD_P = []
    for i in range(0, FOLD):
        test = sorted(files[start:end])
        train = sorted(list(set(files) - set(test)))
        start += holdOut
        end += holdOut

        #make the corpus
        data_set_corpus = PlaintextCorpusReader(sys.argv[1], train)

        #print data_set_corpus.fileids()
        #print "Train %d (%d) Test %d " % (len(train),
                #len(data_set_corpus.fileids()),len(test))

        estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
        lm = NgramModel(3, data_set_corpus.words(), estimator)

        #print lm
        #text = lm.generate(200)
        #import textwrap
        #print '\n'.join(textwrap.wrap(' '.join(text)))

        #text1_file = open("0.txt", 'r')
        #text1 = ''.join(text1_file.readlines()).split()

        test_text = []
        test_words = 0
        for f in test:
            txt_file = open(sys.argv[1]+f, 'r')
            txt = ''.join(txt_file.readlines())
            test_words += len(nltk.word_tokenize(txt))
            #test_text.extend(''.join(txt_file.readlines()).split())
            txt_file.close()
            sentences = sentence_splitter.tokenize(txt.strip())
            test_text.extend(sentences)
        #print "Total sentences in test: %d" % (len(test_text))
        #print "Total documents in test: %d" % (len(test_text))

        P = []
        for s in test_text:
            s_tokens = nltk.word_tokenize(s)
            if len(s_tokens) > 3:
                p = lm.perplexity(s_tokens)
                #print "Perplexity: %f Words: %d" % (p, len(s_tokens))
                P.append(p)
        FOLD_P.append(sum(P)/len(P))
        print "FOLD %d Perplexity: %f Train words (%d) Test words (%d)" % (i,
                FOLD_P[i], len(data_set_corpus.words()), test_words)
    print "Final Perplexity: %f" % (sum(FOLD_P)/len(FOLD_P))
