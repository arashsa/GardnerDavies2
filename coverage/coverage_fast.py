import json
import sys


class Coverage:
    def __init__(self):
        # super().__init__()
        self.kiap = json.load(open('/Users/arashsaidi/PycharmProjects/GardnerDavies2/coverage/kiap.txt'))
        self.kiap_count = int(open('/Users/arashsaidi/PycharmProjects/GardnerDavies2/coverage/count_kiap.txt').readline())
        self.lbk = json.load(open('/Users/arashsaidi/PycharmProjects/GardnerDavies2/coverage/lbk.txt'))
        self.lbk_count = int(open('/Users/arashsaidi/PycharmProjects/GardnerDavies2/coverage/count_lbk.txt').readline())

    def run_kiap(self, list_to_check, n):
        """
        Reads in a list and checks coverage on KIAP
        :param list_to_check: the list to check
        :param n: number of words from list to check
        :return: None
        """
        coverage = 0
        with open(list_to_check, encoding='utf-8') as f:
            word_list = f.readlines()
            count = 1
            for word in word_list:
                w = word.split(' ')[0]
                if w in self.kiap:
                    coverage += self.kiap[w]
                if count == n:
                    break
                else:
                    count += 1
        return coverage / self.kiap_count * 100

    def run_lbk(self, list_to_check, n):
        """
        Coverage on lbk
        :param list_to_check:
        :param n:
        :return:
        """
        coverage = 0
        with open(list_to_check, encoding='utf-8') as f:
            word_list = f.readlines()
            count = 1
            for word in word_list:
                w = word.split(' ')[0]
                if w in self.lbk:
                    coverage += self.lbk[w]
                if count == n:
                    break
                else:
                    count += 1
        return coverage / self.lbk_count * 100

    def run_kiap_2(self, list_to_check, n):
        coverage = 0
        with open(list_to_check, encoding='utf-8') as f:
            word_list = f.readlines()
            count = 1
            for word in word_list:
                w = word.replace('\n', '').replace(' ', '')
                # print(w)
                if w in self.kiap:
                    coverage += self.kiap[w]
                if count == n:
                    break
                else:
                    count += 1
        return coverage / self.kiap_count * 100

    def run_lbk_2(self, list_to_check, n):
        coverage = 0
        with open(list_to_check, encoding='utf-8') as f:
            word_list = f.readlines()
            count = 1
            for word in word_list:
                w = word.replace('\n', '')
                if w in self.lbk:
                    coverage += self.lbk[w]
                if count == n:
                    break
                else:
                    count += 1
        return coverage / self.lbk_count * 100

    def run_kiap_3(self, list_to_check, n):
        coverage = 0
        with open(list_to_check, encoding='utf-8') as f:
            word_list = f.readlines()
            count = 1
            for word in word_list:
                w = word.split('\t')[1].replace(' ', '').replace('\n', '')
                if w in self.kiap:
                    coverage += self.kiap[w]
                if count == n:
                    break
                else:
                    count += 1
        return coverage / self.kiap_count * 100

    def run_lbk_3(self, list_to_check, n):
        coverage = 0
        with open(list_to_check, encoding='utf-8') as f:
            word_list = f.readlines()
            count = 1
            for word in word_list:
                w = word.split('\t')[1].replace(' ', '').replace('\n', '')
                if w in self.lbk:
                    coverage += self.lbk[w]
                if count == n:
                    break
                else:
                    count += 1
        return coverage / self.lbk_count * 100

if __name__ == '__main__':
    """
    Runs with argv.1 filename of list, argv.2 as nr of words to check
    """
    test = Coverage()
    if len(sys.argv) > 1:
        print(sys.argv[1])
        kiap = test.run_kiap(sys.argv[1], sys.argv[2])
        lbk = test.run_lbk(sys.argv[1], sys.argv[2])
        print(kiap, lbk)
    else:
        # kiap = test.run_kiap('lista.txt', 750)
        # lbk = test.run_lbk('lista.txt', 750)
        # print(kiap, lbk)
        print('To run file: python3 word_list_file_name nr_of_words_to_check')