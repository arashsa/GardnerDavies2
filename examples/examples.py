import os
import cg3.read_cg3 as cg3

words = []
with open('akademisk-ordlist-g-og-d-sammenslått_PoS.txt') as f:
    for line in f.readlines():
        current_word = line.split(' ')[0]
        words.append(current_word)

examples = {}
count = 0
number_of_words = len(words)  # 824
max_sentences_added_to_word = 10
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
                        if w in examples and len(examples[w]) < max_sentences_added_to_word:
                            examples[w].append(sentence)
                        else:
                            examples[w] = []
                            examples[w].append(sentence)
                        if len(examples[w]) > 3 and w not in added:
                            count += 1
                            added.append(w)

with open('nav_examples.txt', 'w') as f:
    for w, s in examples.items():
        f.write('$ ' + w + '\n')
        for sentence in s:
            if len(sentence) < 21:
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