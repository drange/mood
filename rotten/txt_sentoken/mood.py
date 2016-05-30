#from nltk import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from os import listdir
from os.path import isfile, join

punct = "\t!\"$%&'()*+,-./0123456789:;?@[\\]^_{}~`"

trans = {"'ve":" have", "'nt": " not", "n't": " not", "'s": " is", "'ll": " will"}
stop_words = []

#portstem = PorterStemmer().stem_word
portstem = WordNetLemmatizer().lemmatize

def increase(dic, key):
    if key not in dic:
        dic[key] = 0
    nv = 1 + dic[key]
    dic[key] = nv

def translate(line):
    global trans
    for k,v in trans.iteritems():
        while k in line:
            line = line.replace(k,v)
    return line

def stem(word):
    return portstem(word)

def sentences(fname, stop = set()):
    global punct, trans
    s = []
    with open(fname, 'r') as fil:
        for line in fil:
            sent = []
            line = translate(line) # replaces doesn't with does not i'll with i will
            for p in punct:
                while p in line:
                    line = line.replace(p, " ")
            l = line.strip()
            lst = line.lower().split()
            for w in lst:
                w = stem(w)
                if w and w not in stop:
                    sent.append(w)
            if sent:
                s.append(sent)
    return s


def words(fname, stop = set()):
    """Returns the set of (lemmatized) words in file fname ignoring stop words"""
    sents = sentences(fname, stop)
    wrds = set()
    for l in sents:
        for w in l:
            if w:
                wrds.add(w)
    return wrds

def populate(rev_path, stop = set()):
    """
    Takes a path to a folder with txt files and a set of stop words.

    Returns a dictionary containing the number of txt files words occur in in
    the folder, not counting stop words.
    """
    word_count = {}
    rev_files = [f for f in listdir(rev_path) if isfile(join(rev_path, f))]
    for fname in rev_files:
        wrds = words(rev_path+"/"+fname, stop)
        for w in wrds:
            increase(word_count,w)
    return word_count

def replace_words(rev_path, word_list, stop = set()):
    """
    Takes a path to a folder with txt files and a word-to-id dictionary

    writes new files with each word replaces with id
    """
    rev_files = [f for f in listdir(rev_path) if isfile(join(rev_path, f))]
    for fname in rev_files:
        wrds = words(rev_path+"/"+fname, stop)
        vector = ["1" if w in wrds else "0" for w in word_list]
        with open("ids"+rev_path+"/"+fname, "w") as f:
            f.write(" ".join(vector))
            f.write("\n")


#
# Getting stop words
#
stop = set()
with open("stop_words_full.txt") as f:
    for line in f:
        line = line.strip().lower()
        ws = line.split()
        for w in ws:
            if w:
                stop.add(w)
stop = list(stop)


#
# Most occurring words in pos and neg reviews
#
print "Populating negatives ..."
neg = populate("neg", stop)
print "done"
print "Populating positives ... "
pos = populate("pos", stop)
print "done"

print "Evaluating importance ...."
neglist = sorted(neg, key=neg.get, reverse=True)
poslist = sorted(pos, key=pos.get, reverse=True)

num = 30

maxlen = 0
for i in range(num):
    maxlen = max([maxlen, len(neglist[i]), len(poslist[i])])

# for i in range(num):
#     wn = neglist[i]
#     wp = poslist[i]
#     sp = maxlen - len(wn) + 2
#     negstr = 'negative %s\t%s (%s)' % (i+1, wn, neg[wn])
#     posstr = 'positive %s \t%s (%s)' % (i+1, wp, pos[wp])
#     print negstr, (" "*sp), posstr


num_words = 1000 # take 1000 most used words
tot = {}
for w in neglist:
    if w in pos:
        tot[w] = neg[w] + pos[w]
    else:
        tot[w] = neg[w]

for w in poslist:
    if w not in neg:
        tot[w] = pos[w]

word_list = sorted(tot, key=tot.get, reverse=True)[:1000]
#for i in range(num_words):
#    print word_list[i]


print "Writing words ... "
with open("words.txt", "w") as f:
    for i in range(len(word_list)):
        f.write(word_list[i] + "\n")
print "done", len(word_list)


print "Replacing negatives ... "
replace_words("neg", word_list, stop)
print "done"

print "Replacing positives ... "
replace_words("pos", word_list, stop)
print "done"
