def sort(f, tag1, tag2, n1, n2, w):
    """
    Takes a file to read, to tags, and a file to write.
    Creates a file with tag1-tag2 only trigrams.
    :param n2: second tag place in original trigrams
    :param n1: first tag place in original trigrams
    :param f: the file to read
    :param tag1: tag1
    :param tag2: tag2
    :param w: file to write to
    :return: None
    """
    html_file = open(w, 'w', encoding='utf-8')
    style = '<style>table, td, th {border: 1px solid #ddd; text-align: left;} ' \
            'table {border-collapse: collapse;width: 100%;} th, td {padding: 15px;}</style>'
    html = '<html><head><meta charset="utf-8">' + style + '</head><body>\n<table>'
    header = '<th>NR</th><th>ord1</th><th>ord2</th><th>ord3</th><th>tag1</th><th>tag2</th><th>tag3</th>' \
             '<th>frekvens</th>'
    html_file.write(html)
    html_file.write(header)
    with open(f, 'r', encoding='utf-8') as t:
        prev = ' '
        trigrams = t.readlines()
        for tri in trigrams:
            tri = tri.replace('<td>', ' ').replace('</td>', ' ')
            if tri.startswith('<tr>'):
                prev = tri
            else:
                words = prev.split()
                tags = tri.split()
                if tag2 and len(tags) > 2:
                    if tags[n1] == tag1 and tags[n2] == tag2:
                        html_file.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>\n'.format(words[1], words[2],
                                                                                                    words[3], words[4]))
                        html_file.write('<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(tags[0], tags[1],
                                                                                                     tags[2], tags[3]))
                elif len(tags) > 2:
                    if tags[n1] == tag1:
                        html_file.write('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>\n'.format(words[1], words[2],
                                                                                                    words[3], words[4]))
                        html_file.write('<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n'.format(tags[0], tags[1],
                                                                                                     tags[2], tags[3]))

    html_file.write('</table></body></html>')

if __name__ == '__main__':
    sort('trigram_PoS.html', 'verb', False, 2, 1, 'verb_3.html')