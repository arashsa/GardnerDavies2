import os
from cg3 import read_cg3
import json
import operator
import math
from coverage import coverage_fast


class AVL:
    def __init__(self):
        # TODO: read in the counts automatically
        """
        Set the paths to corpus.
        :return:
        """
        # Directory to corpus
        self.corpus_directory = '/Users/arashsaidi/Work/Corpus/DUO_LBK_Academic/'
        self.academic_corpus_length = 0
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
        self.department_lengths = []
        self.non_academic_corpus_length = 0

    def get_corpus_lengths(self):
        """
        Adds counts for corpus and sub-corpus
        :return:
        """
        f = open('counts_trigram/word_count_academic.txt')
        self.academic_corpus_length = int(f.readline())
        # print(self.academic_corpus_length)

        with open('counts_trigram/word_count_departments.txt') as f:
            for lines in f.readlines():
                self.department_lengths.append(int(lines.split(' ')[1]))
        # print(self.department_lengths)

        f = open('counts_trigram/word_count_non_academic.txt')
        self.non_academic_corpus_length = int(f.readline())
        # print(self.non_academic_corpus_length)


    @staticmethod
    def store_dict(counts, file_name):
        """
        :param counts:
        :param file_name:
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

    @staticmethod
    def write_to_file(f, w):
        """
        stores the list to file
        :param f: file
        :param w: word and frequency
        :return: None
        """
        f.write('{} {}\n'.format(w[0], w[1]))
        # try:
        #     f.write('{} {}\n'.format(w[0], w[1]))
        # except UnicodeEncodeError:
        #     f.write('{} {}\n'.format(w[0].encode('utf-8'), w[1]))

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
                        prev1 = '<doc>'
                        prev2 = '<doc>'
                        for w in document:
                            w_trigram = prev1 + ' ' + prev2 + ' ' + w
                            prev1 = prev2
                            prev2 = w
                            self.add_count_to_dict(total_dict, w_trigram)  # Add words to total dictionary
                            self.add_count_to_dict(million_dict, w_trigram)  # Add words to million dictionary
                            self.add_count_to_dict(department_dict, w_trigram)  # Add words to department dictionary
                            million_counter += 1  # Increment million count
                            department_counter += 1  # Increment department count
                            total_count += 1  # Increment total count

                            # Million words, write dict to file, reset
                            if million_counter > 1000000:
                                self.remove_threshold(million_dict)
                                self.store_dict(million_dict, 'counts_trigram/millions/' +
                                                str(million_filename) + '.txt')
                                million_filename += 1
                                million_counter = 0
                                million_dict = {}

            # Storing department dictionaries
            self.remove_threshold(department_dict)
            self.store_dict(department_dict, 'counts_trigram/' + department)
            with open('counts_trigram/word_count_departments.txt', 'a') as f:
                f.write(department + ' ' + str(department_counter) + '\n')

        # Storing academic dictionaries
        self.remove_threshold(total_dict)
        self.store_dict(total_dict, 'counts_trigram/dictionary_academic.txt')
        with open('counts_trigram/word_count_academic.txt', 'w') as f:
            f.write(str(total_count))

        print('Finished reading academic corpus')

    def setup_non_academic_nowac(self):
        """
        Setup for nowac. Json count files are produced.
        :return:
        """
        # Total count non-academic
        total_dict = {}
        total_count = 0
        print('Reading files in: non-academic corpus')
        with open('/Users/arashsaidi/Work/Corpus/nowac-1.1', errors='ignore') as f:
            prev1 = '<doc>'
            prev2 = '<doc>'
            for obt in f:
                word = obt.replace('\n', '').split('\t')

                if len(word) > 2:
                    if '$' not in word[1] and word[2] != 'ukjent':
                        w_trigram = prev1 + ' ' + prev2 + ' ' + word[1]
                        prev1 = prev2
                        prev2 = word[1]
                        self.add_count_to_dict(total_dict, w_trigram)
                        total_count += 1

                        # Removing trigrams with values less than 2
                        if total_count % 10000000 == 0:
                            # print(len(total_dict))
                            self.remove_threshold(total_dict)
                            # print(len(total_dict))

        print(total_count)
        print(len(total_dict))
        # Storing non-academic dictionaries
        self.remove_threshold(total_dict)
        self.store_dict(total_dict, 'counts_trigram/dictionary_non_academic.txt')
        with open('counts_trigram/word_count_non_academic.txt', 'w') as f:
            f.write(str(total_count))

        print('Finished reading non-academic corpus')

    def store_included_excluded(self, included, excluded, name):
        """
        Stores two dictionaries as json objects and as lists for retrieval.
        :param included: dictionary of words included
        :param excluded: dictionary of words excluded
        :param name: name of file to store in
        :return:
        """
        self.store_dict(included, 'lists_trigram/' + name + '_included.txt')
        self.store_dict(excluded, 'lists_trigram/' + name + '_excluded.txt')
        sorted_included = sorted(included.items(), key=operator.itemgetter(1), reverse=True)
        sorted_excluded = sorted(excluded.items(), key=operator.itemgetter(1), reverse=True)

        with open('lists_trigram/' + name + '_included_sorted.txt', 'w', encoding='utf-8') as f:
            for w in sorted_included:
                self.write_to_file(f, w)

        with open('lists_trigram/' + name + '_excluded_sorted.txt', 'w', encoding='utf-8') as f:
            for w in sorted_excluded:
                self.write_to_file(f, w)

    @staticmethod
    def store_included(included, name):
        """
        Stores two dictionaries as json objects and as lists.
        :param included: dictionary of words included
        :param name: name of file to store in
        :return:
        """
        sorted_included = sorted(included.items(), key=operator.itemgetter(1), reverse=True)

        with open('lists_trigram/' + name + '_included_sorted.txt', 'w') as f:
            for w in sorted_included:
                f.write('{} {}\n'.format(w[0], w[1]))

    def ratio(self, rate):
        """
        Words (lemmas) must have 50% higher freq in academic part of corpus than non-academic.
        This excludes words that are frequent in a regular corpus.
        :param rate:
        :return:
        """
        included = {}
        excluded = {}
        academic = json.load(open('counts_trigram/dictionary_academic.txt'))
        non_academic = json.load(open('counts_trigram/dictionary_non_academic.txt'))

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
        academic = json.load(open('lists_trigram/ratio_included.txt'))
        departments = []
        # Get each
        for dep in self.academic_departments:
            departments.append(json.load(open('counts_trigram/' + dep)))

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
        academic = json.load(open('lists_trigram/range_included.txt'))
        included = {}
        excluded = {}
        parts = []
        v = []
        f = 0.
        # TODO: get number of files
        n = 91.  # hardcoded value

        for subdir, dirs, files in os.walk('counts_trigram/millions/'):
            for f_ in files:
                parts.append(json.load(open('counts_trigram/millions/' + f_)))

        # Get each word, go through corpus and get counts for each million tokens
        for key, value in academic.items():
            for i in range(len(parts)):
                if key in parts[i]:
                    v.append(parts[i][key])
                    f += parts[i][key]
                else:
                    v.append(0)

            # Avoiding zero division. This will not affect result as values are so small.
            if f == 0:
                f = 1

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

    def discipline_measure(self, rate, save_file='discipline_measure', allfiles=False):
        """
        It states that the word cannot occur more than three times the expected frequency
        (per million words) in any of the nine disciplines.
        :param allfiles: Return both excluded and included.
        :param save_file:
        :param rate:
        :return:
        """
        academic = json.load(open('lists_trigram/dispersion_included.txt'))
        included = {}
        excluded = {}

        departments = []
        for dep in self.academic_departments:
            departments.append(json.load(open('counts_trigram/' + dep)))

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

    def run_all(self, ratio, range_, dispersion, discipline, x_of_y=6):
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

if __name__ == '__main__':
    """
    To run:
    1. test = AVL()
    2. test.setup_academic()
    3. test.setup_non_academic_nowac()
    4. test.get_corpus_lengths()

    Then you can create list by running the 4 measures:
    1. test.ratio(x)
    2. test.range(x, y)
    3. test.dispersion(x)
    4. test.discipline_measure(3, allfiles=True)
    """

    test = AVL()
    # test.setup_academic()
    # test.setup_non_academic_nowac()
    test.get_corpus_lengths()

    # Test from 1 - 5
    test.ratio(2)

    # range, number of faculties (x of 8)
    test.range(0.8, 6)

    # Test from 0.6
    test.dispersion(0.90)

    # Test from 3
    test.discipline_measure(3.5, allfiles=True)

    # Coverage
    # coverage = coverage_fast.Coverage()
    # kiap = coverage.run_kiap('lists/discipline_measure_included_sorted.txt', 750)
    # lbk = coverage.run_lbk('lists/discipline_measure_included_sorted.txt', 750)
    # print(kiap)
    # print(lbk)