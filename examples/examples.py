import os
import cg3.read_cg3 as cg3

words = []
with open('akademisk-ordlist-g-og-d-sammenslått_PoS.txt') as f:
    for line in f.readlines():
        current_word = line.split(' ')[0]
        words.append(current_word)

examples = {}
for subdir, dirs, files in os.walk('/Users/arashsaidi/Work/Corpus/DUO_LBK_Academic/'):
    for f in files:
        if f.endswith('.obt'):
            for sentence in cg3.read_cg3_sentence(os.path.join(subdir, f)):
                for w in words:
                    if w in sentence:
                        examples[w] = sentence
                        print(len(examples))