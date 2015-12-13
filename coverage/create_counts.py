import os
from cg3 import read_cg3, read_lbk
import codecs
import json

directory_lbk = '/Users/arashsaidi/Work/Corpus/lbk_22.04.14/Skjonnlitt/'
directory_kiap = '/Users/arashsaidi/Work/Corpus/kiap-obt/'


def remove_threshold(dictionary):
    for k in list(dictionary):
        if dictionary[k] < 5:
            del dictionary[k]

counts = {}
words = 0
# lbk
for dir_name, d, file_names in os.walk(directory_lbk):
    for f in file_names:
        if f.endswith('.okl'):
                cg3_data = read_lbk.read_cg3(codecs.open(os.path.join(dir_name, f), 'r', 'ISO-8859-1'))
                for sentence in cg3_data:
                    for word in sentence:
                        # Check if list
                        if not isinstance(word, str):
                            if '$' not in word[1]:
                                words += 1
                                current_word = word[1].replace('"', '')
                                if current_word in counts:
                                    counts[current_word] += 1
                                else:
                                    counts[current_word] = 1

remove_threshold(counts)
json.dump(counts, open('lbk.txt', 'w'))
with open('count_lbk.txt', 'w') as f:
    f.write(str(words))

counts = {}
words = 0
# kiap
for dir_name, d_, file_names in os.walk(directory_kiap):
            for f in file_names:
                if f.endswith('.obt'):
                    cg3_data = read_lbk.read_cg3(codecs.open(os.path.join(dir_name, f), 'r', 'utf8'))
                    for word in cg3_data:
                        # Check if list
                        if not isinstance(word, str):
                            if isinstance(word[1], str):
                                current_word = word[1].replace('"', '')
                                if '$' not in current_word:
                                    words += 1
                                    if current_word in counts:
                                        counts[current_word] += 1
                                    else:
                                        counts[current_word] = 1

remove_threshold(counts)
json.dump(counts, open('kiap.txt', 'w'))
with open('count_kiap.txt', 'w') as f:
    f.write(str(words))
