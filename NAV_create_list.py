import os
from cg3 import read_cg3, read_lbk
import json
import codecs
import operator
import math
from extras import *
from coverage import coverage_fast
import shutil


class AVL:
    def __init__(self):
        # TODO: read in the counts automatically
        """
        Set the paths to corpus.
        :return:
        """
        # Directory to corpus
        self.corpus_directory = '/Users/arashsaidi/Work/Corpus/DUO_LBK_Academic/'
        self.academic_corpus_length = 91223188
        self.academic_departments = [
            'Det_humanistiske_fakultet',
            'Det_juridiske_fakultet',
            'Det_matematisk-naturvitenskapelige_fakultet',
            'Det_medisinske_fakultet',
            'Det_odontologiske_fakultet',
            'Det_samfunnsvitenskapelige_fakultet',
            'Det_teologiske_fakultet',
            'Det_utdanningsvitenskapelige_fakultet'
        ]
        self.department_lengths = [39676161, 4399816, 5563306, 9418080, 292826, 12690717, 3261491, 15920791]
        self.non_academic_corpus = ''
        self.non_academic_corpus_length = 587469476

    @staticmethod
    def store_dict(counts, file_name):
        """
        Stores count files as Json stream.
        :return:
        """
        json.dump(counts, open(file_name, 'w'))

    @staticmethod
    def add_count_to_dict(d, w):
        """
        Add words to dictionary for count.
        :param d: dictionary
        :param w: words
        :return:
        """
        if w in d:
            d[w] += 1
        else:
            d[w] = 1

    @staticmethod
    def remove_threshold(dictionary):
        for k in list(dictionary):
            if dictionary[k] < 2:
                del dictionary[k]

    def setup_academic(self):
        """
        Creates the counts for Words (lemmas) in the academic corpus.
        Json count files for the whole corpus and million intervals.
        :return:
        """
        # Counts for academic corpus
        # Total count
        total_dict = {}
        total_count = 0

        # Word (lemma) each 1.000.000 count
        million_filename = 1
        million_counter = 0
        million_dict = {}

        for department in self.academic_departments:
            print('Reading files in: ' + department)

            # Word (lemma) counts for each department
            department_dict = {}
            department_counter = 0

            for subdir, dirs, files in os.walk(self.corpus_directory + department):
                for f in files:
                    if f.endswith('.obt') and os.stat(os.path.join(subdir, f)).st_size > 0:
                        # Document as list
                        document = read_cg3.read_cg3(os.path.join(subdir, f))
                        for w in document:
                            self.add_count_to_dict(total_dict, w)  # Add words to total dictionary
                            self.add_count_to_dict(million_dict, w)  # Add words to million dictionary
                            self.add_count_to_dict(department_dict, w)  # Add words to department dictionary
                            million_counter += 1  # Increment million count
                            department_counter += 1  # Increment department count
                            total_count += 1  # Increment total count

                            # Million words, write dict to file, reset
                            if million_counter > 1000000:
                                self.remove_threshold(million_dict)
                                self.store_dict(million_dict, 'counts/millions/' + str(million_filename) + '.txt')
                                million_filename += 1
                                million_counter = 0
                                million_dict = {}

            # Storing department dictionaries
            self.remove_threshold(department_dict)
            self.store_dict(department_dict, 'counts/' + department)
            with open('counts/word_count_departments.txt', 'a') as f:
                f.write(department + ' ' + str(department_counter) + '\n')

        # Storing academic dictionaries
        self.remove_threshold(total_dict)
        self.store_dict(total_dict, 'counts/dictionary_academic.txt')
        with open('counts/word_count_academic', 'w') as f:
            f.write(str(total_count))

    def setup_non_academic(self):
        """
        Setup for LBK. Json count files are produced.
        :return:
        """
        # Total count non-academic
        total_dict = {}
        total_count = 0
        print('Reading files in: non-academic corpus')
        for subdir, dirs, files in os.walk(self.corpus_directory + self.non_academic_corpus):
            for f in files:
                if f.endswith('.okl'):
                    for sentence in read_lbk.read_cg3(codecs.open(os.path.join(subdir, f), 'r', 'ISO-8859-1')):
                        for word in sentence:
                            if not isinstance(word, str):
                                if '$' not in word[1]:
                                    current_word = word[1].replace('"', '')
                                    self.add_count_to_dict(total_dict, current_word)
                                    total_count += 1

        # Storing non-academic dictionaries
        self.remove_threshold(total_dict)
        self.store_dict(total_dict, 'counts/dictionary_non_academic.txt')
        with open('counts/word_count_non_academic', 'w') as f:
            f.write(str(total_count))

    def setup_non_academic_nowac(self):
        """
        Setup for LBK. Json count files are produced.
        :return:
        """
        # Total count non-academic
        total_dict = {}
        total_count = 0
        print('Reading files in: non-academic corpus')
        with open('/Users/arashsaidi/Work/Corpus/nowac-1.1', errors='ignore') as f:
            for obt in f:
                word = obt.replace('\n', '').split('\t')
                if len(word) > 2:
                    if '$' not in word[1] and word[2] != 'ukjent':
                        current_word = word[1]
                        self.add_count_to_dict(total_dict, current_word)
                        total_count += 1

        print(total_count)
        print(len(total_dict))
        # Storing non-academic dictionaries
        self.remove_threshold(total_dict)
        self.store_dict(total_dict, 'counts/dictionary_non_academic.txt')
        with open('counts/word_count_non_academic', 'w') as f:
            f.write(str(total_count))

    def store_included_excluded(self, included, excluded, name):
        """
        Stores two dictionaries as json objects and as lists for retrieval.
        :param included: dictionary of words included
        :param excluded: dictionary of words excluded
        :param name: name of file to store in
        :return:
        """
        self.store_dict(included, 'lists/' + name + '_included.txt')
        self.store_dict(excluded, 'lists/' + name + '_excluded.txt')
        sorted_included = sorted(included.items(), key=operator.itemgetter(1), reverse=True)
        sorted_excluded = sorted(excluded.items(), key=operator.itemgetter(1), reverse=True)

        with open('lists/' + name + '_included_sorted.txt', 'w') as f:
            for w in sorted_included:
                f.write('{} {}\n'.format(w[0], w[1]))
        with open('lists/' + name + '_excluded_sorted.txt', 'w') as f:
            for w in sorted_excluded:
                f.write('{} {}\n'.format(w[0], w[1]))

    @staticmethod
    def store_included(included, name):
        """
        Stores two dictionaries as json objects and as lists.
        :param included: dictionary of words included
        :param name: name of file to store in
        :return:
        """
        sorted_included = sorted(included.items(), key=operator.itemgetter(1), reverse=True)

        with open('lists/' + name + '_included_sorted.txt', 'w') as f:
            for w in sorted_included:
                f.write('{} {}\n'.format(w[0], w[1]))

    def ratio(self, rate):
        """
        Words (lemmas) must have 50% higher freq in academic part of corpus than non-academic.
        This excludes words that are frequent in a regular corpus.
        :return:
        """
        included = {}
        excluded = {}
        academic = json.load(open('counts/dictionary_academic.txt'))
        non_academic = json.load(open('counts/dictionary_non_academic.txt'))

        # Iterates through academic dictionary
        for key, value in academic.items():
            # Checks if word in academic corpus is in non_academic corpus
            if key in non_academic:
                # Checks if frequency is higher in academic vs non_academic determined by rate (between 1 and 3)
                if (value / self.academic_corpus_length) > (non_academic[key] / self.non_academic_corpus_length) * rate:
                    included[key] = value
                else:
                    excluded[key] = value
            else:
                excluded[key] = value

        # Stores the two dictionaries
        self.store_included_excluded(included, excluded, 'ratio')

    def range(self, rate, number_of_faculties):
        """
        Words (lemmas) must have at least rate% of expected frequency in at least x of 8 academic disciplines.
        :param rate: The rate at which we check expected frequency.
        :param number_of_faculties: Number of faculties to check in
        :return:
        """
        included = {}
        excluded = {}
        academic = json.load(open('lists/ratio_included.txt'))
        departments = []
        # Get each
        for dep in self.academic_departments:
            departments.append(json.load(open('counts/' + dep)))

        # Checking if word (lemma) is in at least x of 8, and has at least rate% expected freq
        for key, value in academic.items():
            count = 0
            word_freq = value / self.academic_corpus_length
            for i in range(len(departments)):
                expected = (word_freq * self.department_lengths[i]) * rate
                if key in departments[i]:
                    if departments[i][key] >= expected:
                        count += 1
            # Found in at least number of x with rate% of expected freq
            if count >= number_of_faculties:
                included[key] = value
            else:
                excluded[key] = value
        self.store_included_excluded(included, excluded, 'range')

    def dispersion(self, rate):
        """
        Words (lemmas) in the core must have a Dispersion of at least 0.80. This uses Juilland et al.
        http://www.linguistics.ucsb.edu/faculty/stgries/research/2008_STG_Dispersion_IJCL.pdf
        :param rate: the dispersion rate to exclude words
        :return:
        """
        academic = json.load(open('lists/range_included.txt'))
        included = {}
        excluded = {}
        parts = []
        v = []
        f = 0.
        n = 100.

        for subdir, dirs, files in os.walk('counts/millions/'):
            for f_ in files:
                parts.append(json.load(open('counts/millions/' + f_)))

        # Get each word, go through corpus and get counts for each million tokens
        for key, value in academic.items():
            for i in range(len(parts)):
                if key in parts[i]:
                    v.append(parts[i][key])
                    f += parts[i][key]
                else:
                    v.append(0)

            v_ = f / n
            v_sum = 0.
            for i in range(len(v)):
                v_sum += (v[i] - v_) ** 2

            sd = math.sqrt(v_sum / (n - 1))
            vc = sd / v_
            j_measure = 1 - (vc / math.sqrt(n - 1))

            # Julliand measure of at least rate
            if j_measure >= rate:
                included[key] = value
            else:
                excluded[key] = value

            # reset
            v = []
            f = 0

        self.store_included_excluded(included, excluded, 'dispersion')

    def discipline_measure(self, rate, save_file='', allfiles=False):
        """
        It states that the word cannot occur more than three times the expected frequency
        (per million words) in any of the nine disciplines.
        :param allfiles:
        :param save_file:
        :param rate:
        :return:
        """
        academic = json.load(open('lists/dispersion_included.txt'))
        included = {}
        excluded = {}

        departments = []
        for dep in self.academic_departments:
            departments.append(json.load(open('counts/' + dep)))

        for word, value in academic.items():
            n = value / self.academic_corpus_length
            discipline = False
            d_count = 0
            found_in_department = []
            for i in range(len(self.department_lengths)):
                expected = n * self.department_lengths[i]
                if word in departments[i]:
                    # Exclude words based on their frequency compared to expected frequency
                    if departments[i][word] > expected * rate:
                        discipline = True
                        d_count += 1
                        found_in_department.append(i)
                        # print(word, departments[i][word], expected)

            if discipline:
                excluded[word] = value
            else:
                included[word] = value

        if allfiles:
            self.store_included_excluded(included, excluded, 'discipline_measure')
        else:
            self.store_included(included, save_file)

    def multiple_lists(self, ratio, range_, dispersion, discipline, x_of_y=6):
        """
        Creates lists by running all the methods at once.
        :param ratio:
        :param range_:
        :param dispersion:
        :param discipline:
        :param x_of_y:
        :return:
        """
        self.ratio(ratio)
        self.range(range_, x_of_y)
        self.dispersion(dispersion)
        self.discipline_measure(discipline, str(ratio + ' ' + range_ + ' ' + dispersion + ' ' + discipline))

    def make_lists_and_run_coverage(self):
        """
        Creates a selection of lists and returns their coverage.
        :return:
        """
        coverage = coverage_fast.Coverage()
        count = 0
        all_data = {}
        all_data_list = []
        for a in my_range(1, 4, 0.1):
            self.ratio(a)
            for b in my_range(0.1, 0.7, 0.1):
                self.range(b, 6)
                for c in my_range(0.5, 0.9, 0.1):
                    self.dispersion(c)
                    for d in my_range(2, 5, 0.1):
                        self.discipline_measure(d, allfiles=True)
                        print('Checking coverage: ' + str(count))
                        kiap = coverage.run_kiap(
                            'lists/discipline_measure_included_sorted.txt', 750)
                        lbk = coverage.run_lbk(
                            'lists/discipline_measure_included_sorted.txt', 750)
                        with open('lists/coverage_all_range_6_8.txt', 'a') as f:
                            f.write('\nNr: ' + str(count))
                            f.write('\nCoverage KIAP: ' + str(kiap))
                            f.write('\nCoverage LBK-Skjonn: ' + str(lbk))
                            f.write('\nDifference: ' + str(kiap - lbk))
                            f.write('\nData: ' + str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d))
                            all_data[kiap - lbk] = [kiap - lbk, kiap, lbk, a, b, c, d]
                            all_data_list.append(kiap - lbk)
                        count += 1

                        # Copy files to directories with each value appended to first name in file
                        # This is to check the files later so to get the best values
                        save_file = '_' + str(round(float(kiap - lbk), 3)) + '_' + str(round(float(kiap), 3)) \
                                    + '_' + str(round(float(lbk), 3)) + '_' + str(a) + '_' + str(b) + '_' \
                                    + str(c) + '_' + str(d)
                        shutil.copy('lists/discipline_measure_included_sorted.txt',
                                    'lists_diff/' + str(round(float(kiap - lbk), 3)) + save_file + '.txt')
                        shutil.copy('lists/discipline_measure_included_sorted.txt',
                                    'lists_kiap/' + str(round(float(kiap), 3)) + save_file + '.txt')
                        shutil.copy('lists/discipline_measure_included_sorted.txt',
                                    'lists_lbk/' + str(round(float(lbk), 3)) + save_file + '.txt')
                        shutil.copy('lists/discipline_measure_included_sorted.txt',
                                    'lists_ratio/' + str(a) + save_file + '.txt')
                        shutil.copy('lists/discipline_measure_included_sorted.txt',
                                    'lists_range/' + str(b) + save_file + '.txt')
                        shutil.copy('lists/discipline_measure_included_sorted.txt',
                                    'lists_dispersion/' + str(c) + save_file + '.txt')
                        shutil.copy('lists/discipline_measure_included_sorted.txt',
                                    'lists_discipline/' + str(d) + save_file + '.txt')

        all_data_list.sort(reverse=True)
        with open('final_coverages.txt', 'w') as f:
            f.write('Difference, kiap, lbk, ratio, range, dispersion, discipline\n')
            for w in all_data_list:
                f.write(str(all_data[w]) + '\n')

    def make_multiple_lists(self):
        """
        Make lists from a file
        :return:
        """
        with open('final_coverages_6_8.txt') as f:
            f.readline()
            text = f.readlines()
            for data in text:
                d = data.replace('[', '').replace(']', '').replace(',', '').replace('\n', '').split(' ')
                self.ratio(float(d[3]))
                self.range(float(d[4]), 6)
                self.dispersion(float(d[5]))
                self.discipline_measure(float(d[6]), str(d) + '.txt')
                print('Created list: ' + str(d))

if __name__ == '__main__':
    test = AVL()
    test.make_lists_and_run_coverage()

    # test.setup_academic()
    # test.setup_non_academic_nowac()

    # Test from 1 - 5
    # test.ratio(2.8)

    # range, number of faculties (x of 8)
    # test.range(0.2, 6)

    # Test from 0.6
    # test.dispersion(0.8)

    # Test from 3
    # test.discipline_measure(3, allfiles=True)

    # Coverage
    # coverage = coverage_fast.Coverage()
    # kiap = coverage.run_kiap('lists/discipline_measure_included_sorted.txt', 750)
    # lbk = coverage.run_lbk('lists/discipline_measure_included_sorted.txt', 750)
    # print(kiap)
    # print(lbk)