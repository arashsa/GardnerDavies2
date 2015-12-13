from cg3 import read_lbk
import codecs
import os
import operator


def run_coverage(n, academic_list, save_file):
    # TO RUN:
    # Remember to change nr_of_words and file names

    # For running the academic part of lbk
    academic_dir_name = ['/Users/arashsaidi/Work/Corpus/lbk_22.04.14/Sakprosa/SA02',
                                                   '/Users/arashsaidi/Work/Corpus/lbk_22.04.14/Sakprosa/SA04',
                                                   '/Users/arashsaidi/Work/Corpus/lbk_22.04.14/Sakprosa/SA05',
                                                   '/Users/arashsaidi/Work/Corpus/lbk_22.04.14/Sakprosa/SA22']

    # To run this script, make changes for which corpus to run as comparison
    print('Running Coverage on lbk...')
    lbk = 'Skjonnlitt/'
    # Number of words to include in academic list
    nr_of_words = n
    duo_words = []
    words_checked = 0
    coverage = 0

    # Words list to check for coverage
    with open('/Users/arashsaidi/PycharmProjects/GardnerDavies2/lists/' + academic_list) as duo:
        for word in duo.readlines():
            if words_checked < nr_of_words:
                word = word.split(' ')[0].replace('\n', '')
                duo_words.append(word)
                words_checked += 1

    found_count = 0.
    word_counts = dict()
    total_word_count = 0.
    for dir_name, dir_names, file_names in os.walk('/Users/arashsaidi/Work/Corpus/lbk_22.04.14/' + lbk):
        for f in file_names:
            # ADD LINE BELOW TO JUST CHECK ACADEMIC PART OF LBK SAKPROSA
            # and dir_name in academic_dir_name
            if f.endswith('.okl'):
                cg3_data = read_lbk.read_cg3(codecs.open(os.path.join(dir_name, f), 'r', 'ISO-8859-1'))
                for sentence in cg3_data:
                    for word in sentence:
                        # Check if list
                        if not isinstance(word, str):
                            if '$' not in word[1]:
                                total_word_count += 1.
                                current_word = word[1].replace('"', '')
                                if current_word in duo_words:
                                    found_count += 1
                                    if current_word in word_counts:
                                        word_counts[current_word] += 1.
                                    else:
                                        word_counts[current_word] = 1.

    print(total_word_count)

    for word, count in word_counts.items():
        word_counts[word] = count / total_word_count

    sorted_x = sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)

    directory = '/Users/arashsaidi/PycharmProjects/GardnerDavies2/coverage/'
    with open(directory + str(nr_of_words) + '_words_checked_lbk_' + save_file + '.txt', 'w') as f:
        f.write('Total words in comparison: ' + str(total_word_count) + '\n')
        for word in sorted_x:
            coverage += word[1]
        f.write('Coverage: ' + str(coverage * 100) + '\n\n')
        for word in sorted_x:
            f.write(word[0] + ' ' + str(word[1]) + '\n')

    return coverage
