import multiprocessing as mp
import os
import itertools


def wordCounter(qIn, qOut):
    answer = {}
    for fname, words in iter(qIn.get, None):
        for word in words:
            if fname not in answer:
                answer[fname] = {}
            if word not in answer[fname]:
                answer[fname][word] = 0
            answer[fname][word] += 1
    qOut.put(answer)


def getLines(corpusPath, qIn, numProcs):
    for fname in os.listdir(corpusPath):
        with open(os.path.join(corpusPath, fname)) as infile:
            for i, (k,lines) in enumerate(itertools.groupby((l.strip() for l in infile), lambda line : bool(line) and not line.startswith('"<') and "$" not in line.split(None,1)[0])):
                if not k:
                    continue
                qIn.put((fname, [line.split(None,1)[0].strip('"').strip().lower() for line in lines]))

    for _ in range(numProcs):
        qIn.put(None)


def cg3(corpusPath):
    qIn, qOut = [mp.Queue() for _ in range(2)]
    procs = [mp.Process(target=wordCounter, args=(qIn, qOut)) for _ in range(mp.cpu_count() -1)]

    lineGetter = mp.Process(target=getLines, args=(corpusPath, qIn, len(procs)))
    lineGetter.start()

    for p in procs:
        p.start()

    answer = {}
    for _ in range(len(procs)):
        for fname, wdict in qOut.get().items():
            if fname not in answer:
                answer[fname] = {}
            for word,count in wdict.items():
                if word not in answer[fname]:
                    answer[fname][word] = 0
                answer[fname][word] += count

    for fname in sorted(answer):
        for word in sorted(answer[fname]):
            print("{} appeared in {} {} times".format(word, fname, answer[fname][word]))

    for p in procs:
        p.terminate()
    lineGetter.terminate()