import os
import cg3.read_cg3


def get_pos(file_name):
    """
    Gets pos tags for NAV files
    :param n: number of words from NAV to get tags for
    :param file_name: NAV filename
    :return:
    """
    checked = []
    tags = {}

    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for w in lines:
            w1 = w.split(' ')[0]
            w2 = w.split(' ')[1]
            w3 = w.split(' ')[2]
            tags[w1] = 0
            tags[w2] = 0
            tags[w3] = 0

    print(len(tags))

    n = 2618
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
                            if current_word[0] not in checked and '"' not in current_word[1]:
                                # print(current_word)
                                tags[current_word[0]] = current_word[1]
                                checked.append(current_word[0])
                                counts += 1

    counts = 0
    with_tags = open(file_name.replace('.txt', '_PoS.html'), 'w', encoding='utf-8')
    style = '<style>table, td, th {border: 1px solid #ddd; text-align: left;} ' \
            'table {border-collapse: collapse;width: 100%;} th, td {padding: 15px;}</style>'
    html = '<html><head><meta charset="utf-8">' + style + '</head><body>\n<table>'
    header = '<th>NR</th><th>ord1</th><th>ord2</th><th>ord3</th><th>tag1</th><th>tag2</th><th>tag3</th>' \
             '<th>frekvens</th>'
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        with_tags.write(html)
        with_tags.write(header)
        for w in lines:
            word_list = w.split(' ')
            w1 = word_list[0]
            w2 = word_list[1]
            w3 = word_list[2]
            freq = word_list[3].replace('\n', '')
            t1 = tags[w1]
            t2 = tags[w2]
            t3 = tags[w3]
            with_tags.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>\n'.format(counts + 1, w1, w2, w3))
            with_tags.write('<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(t1, t2, t3, freq))
            counts += 1
            if counts > n:
                with_tags.write('</table></body></html>')
                break


get_pos('trigram.txt')
