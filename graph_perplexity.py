#!/usr/bin/python
# File Name : perplexity2.py
# Purpose : Generates a perplexity score based on test train split
# Creation Date : 03-04-2012
# Last Modified : Fri 09 Mar 2012 04:19:46 PM MST
# Created By : Nathan Gilbert
#
import sys
import random

import nltk.data
from ngram import NgramModel
from nltk.probability import LidstoneProbDist, WittenBellProbDist
from nltk.corpus import PlaintextCorpusReader

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: %s <train_dir> <train_docs> <test_dir> <test_docs> +s" % (sys.argv[0])
        sys.exit(1)

    INCREMENT = 100

    if "+s" in sys.argv:
        SENTENCE = True
    else:
        SENTENCE = False

    train_file = open(sys.argv[2], 'r')
    train_files = []
    for line in train_file:
        train_files.append(line.strip())

    #shuffle the training files
    random.shuffle(train_files)

    #print train_files
    print len(train_files)

    if SENTENCE:
        sentence_splitter = nltk.data.load('tokenizers/punkt/english.pickle')

    test_file = open(sys.argv[4], 'r')
    test_files = []
    for line in test_file:
        test_files.append(line.strip())

    test_text = []
    test_words = 0
    for f in test_files:
        txt_file = open(sys.argv[3]+"/"+f, 'r')
        txt = ''.join(txt_file.readlines())
        txt_file.close()
        if SENTENCE:
            sentences = sentence_splitter.tokenize(txt.strip())
            test_text.extend(sentences)
        else:
            test_text.append(txt)

    #print test_files
    print len(test_files)

    total_train_files = []
    TOTAL = INCREMENT
    UPPER_LIMIT = 500

    while len(total_train_files) < UPPER_LIMIT:
        total_train_files = train_files[:TOTAL]
        data_set_corpus = PlaintextCorpusReader(sys.argv[1], total_train_files)
        estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
        lm = NgramModel(3, data_set_corpus.words(), estimator)
        #lm = NgramModel(2, data_set_corpus.words(), estimator)

        P=[]
        for s in test_text:
            s_tokens = nltk.word_tokenize(s)
            if SENTENCE:
                #if len(s_tokens) > 3:
                if len(s_tokens) > 10:
                    p = lm.perplexity(s_tokens)
                    P.append(p)
            else:
                p = lm.perplexity(s_tokens)
                P.append(p)
        TOTAL += INCREMENT

        print "%d %f" % (len(total_train_files), sum(P)/len(P))
