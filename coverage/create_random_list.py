import cg3.read_lbk as lbk
import os
import codecs
import random

word_list = []

for subdir, dirs, files in os.walk('/Users/arashsaidi/Work/Corpus/lbk_22.04.14/TV'):
    for f in files:
        if f.endswith('.okl'):
            for sentence in lbk.read_cg3(codecs.open(os.path.join(subdir, f), 'r', 'ISO-8859-1')):
                for word in sentence:
                    if not isinstance(word, str):
                        if '$' not in word[1]:
                            current_word = word[1].replace('"', '')
                            if random.randint(0, 1000) > 980:
                                if current_word not in word_list:
                                    word_list.append(current_word)
                if len(word_list) > 750:
                    break
    if len(word_list) > 750:
                    break

with open('random_lbk.txt', 'w') as f:
    for w in word_list[0:750]:
        f.write(w + '\n')

# 46.12788739668003 67.80671117032298