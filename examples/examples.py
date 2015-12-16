import os
import cg3.read_cg3 as cg3
import random

words = []
with open('akademisk-ordlist-g-og-d-sammenslått_PoS.txt') as f:
    for line in f.readlines():
        current_word = line.split(' ')[0]
        words.append(current_word)

# add examples to dictionary
examples = {}
count = 0
number_of_words = len(words)  # the number of words in list to get examples
min_sentences_added_to_word = 10  # minimum number of words added to each example, is possible
added = []
for subdir, dirs, files in os.walk('/Users/arashsaidi/Work/Corpus/DUO_LBK_Academic/'):
    if count >= number_of_words:
            break
    for f in files:
        if count >= number_of_words:
            break
        if f.endswith('.obt'):
            for sentence in cg3.read_cg3_sentence(os.path.join(subdir, f)):
                for w in words:
                    if w in sentence:
                        if w in examples:
                            if len(examples[w]):
                                examples[w].append(sentence)
                        else:
                            examples[w] = []
                            examples[w].append(sentence)

                        if len(examples[w]) > min_sentences_added_to_word and w not in added:
                            count += 1
                            added.append(w)

# Scramble the list
for w in words:
    if w in examples:
        random.shuffle(examples[w])

max_sentence_length = 35
min_sentence_length = 8
sentences_added = 20
with open('nav_examples.txt', 'w') as f:
    for w, s in examples.items():
        count = 0
        f.write('$ ' + w + '\n')
        for sentence in s:
            count += 1
            if count > sentences_added:
                break
            if min_sentence_length < len(sentence) < max_sentence_length:
                first = True
                for word in sentence:
                    if word in '<>,.?/:;"{}[]|\\~`!@#$%^&*()_-+=':
                        f.write(word)
                    else:
                        if first:
                            f.write(word[0].upper() + word[1:])
                            first = False
                        else:
                            f.write(' ' + word)
                f.write('\n')