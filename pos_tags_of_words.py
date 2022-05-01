#!/usr/bin/env python3

"""POS(Part Of Speech) tags of words"""

import getopt
import os
import sys
import yaml
import csv
import nltk

ymlfile = "tagset.yml"

def usage():
    print("Usage: %s [OPTION]..." % (sys.argv[0]))
    print("  -t, --text=#")
    print("  -f, --file=#")
    print("  -o, --outfile=#")

if __name__ == '__main__':
    opts, _ = getopt.getopt(sys.argv[1:], '-t:-f:-o:-I', ['text=', 'file=', 'outfile=', 'help'])
    
    text = None
    file = None
    outfile = None
    
    for o, a in opts:
        if o in ("-I", "--help"):
            usage()
            sys.exit()
        elif o in ("-t", "--text"):
            text = a
        elif o in ("-f", "--file"):
            file = a
        elif o in ("-o", "--outfile"):
            outfile = a
        else:
            assert False, "unhandled option"
            
    if text is None and file is None:
        usage()
        sys.exit()
    
    if text is not None:
        words = nltk.word_tokenize(text)
    elif file is not None:
        with open(file, 'r') as f:
            text = f.read()
            words = nltk.word_tokenize(text)
    tags = nltk.pos_tag(words)
    
    with open(os.path.join(os.path.dirname(sys.argv[0]), ymlfile), 'r') as f:
        tagset = yaml.safe_load(f)
    
    new_tags = []
    for i in range(0, len(tags)):
        tag = []
        tag.append(tags[i][0])
        tag.append(tagset[tags[i][1]])
        new_tags.append(tag)

    if outfile is not None:
        with open(outfile, 'a') as f:
            writer = csv.writer(f)
            writer.writerows(new_tags)
    else:
        for new_tag in new_tags:
            print(new_tag)
