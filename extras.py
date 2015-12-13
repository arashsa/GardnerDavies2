def print_counts(word, parts):
    """
    Print counts from a list of dicts
    :param word:
    :param parts:
    :return:
    """
    for i in range(len(parts)):
        if word in parts[i]:
            print(parts[i][word])
        else:
            print('NAN')


def my_range(start, stop, step):
    r = start
    while r < stop:
        yield round(r, 1)
        r += step