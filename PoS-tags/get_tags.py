import os
import cg3.read_cg3


def get_pos(file_name, n):
    """
    Gets pos tags for NAV files
    :param n: number of words from NAV to get tags for
    :param file_name: NAV filename
    :return:
    """
    n -= 1
    counts = 0
    checked = []
    tags = {}

    with open(file_name) as f:
        lines = f.readlines()
        for w in lines:
            current_word = w.split(' ')[0]
            tags[current_word] = 0
            counts += 1
            if counts > n:
                break

    counts = 0
    for subdir, dirs, files in os.walk('/Users/arashsaidi/Work/Corpus/DUO_LBK_Academic/'):
        if counts > n:
            break
        for f in files:
            if counts > n:
                break
            if f.endswith('.obt'):
                for w in cg3.read_cg3.read_cg3_tags(os.path.join(subdir, f)):
                    current_word = w.split(' ')
                    if counts > n:
                        break
                    if len(current_word) > 1:
                        if current_word[0] in tags:
                            if current_word[0] not in checked:
                                print(current_word)
                                tags[current_word[0]] = current_word[1]
                                checked.append(current_word[0])
                                counts += 1

    counts = 0
    with_tags = open(file_name.replace('.txt', '_PoS.txt'), 'w')
    with open(file_name) as f:
        lines = f.readlines()
        for w in lines:
            current_word, freq = w.split(' ')[0], w.split(' ')[1].replace('\n', '')
            tag = tags[current_word]
            with_tags.write(current_word + ' ' + str(tag) + ' ' + str(freq) + '\n')
            counts += 1
            if counts > n:
                break

get_pos('akademisk-ordlist-g-og-d-sammenslått-siste.txt', 750)