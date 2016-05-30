from sklearn import svm

import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join

from random import shuffle

def get_vectors(pth):
    vecs = []
    data_files = [f for f in listdir(pth) if isfile(join(pth, f))]
    for fname in data_files:
        with open(pth + "/" + fname) as f:
            vec = []
            for l in f:
                for x in l.split():
                    vec.append(int(x))
            vecs.append(vec)
    return vecs

# [[0, 1, 1, ...], [...], [...]] 1000 x 1000 bool vectors
neg = get_vectors("negative")
pos = get_vectors("positive")
shuffle(neg)
shuffle(pos)

cv_size = int(len(neg)*0.2)
gamma = 0.001
C = 100
kernel = 'rbf'
print "Cross validation size", cv_size
print "gamma                ", gamma
print "C                    ", C
print "Kernel function      ", kernel

neg_cv = neg[:cv_size]
pos_cv = pos[:cv_size]
neg = neg[cv_size:]
pos = pos[cv_size:]

X = neg + pos
y = [0 if i < len(neg) else 1 for i in range(len(neg) + len(pos))]
print "X", len(X)
print "y", len(y)

clf = svm.SVC(kernel=kernel, gamma=gamma, C=C)
clf.fit(X,y)

fp = 0 #false pos
fn = 0 #false neg
tn = 0 #true neg
tp = 0 #true pos

for pvec in pos_cv:
    p = clf.predict(pvec)[0]
    if p:
        tp += 1
    else:
        fn += 1

for nvec in neg_cv:
    p = clf.predict(nvec)[0]
    if p:
        fp += 1
    else:
        tn += 1

precision = tp / float(tp+fp)
recall    = tp / float(tp+fn)

print fp, tp, fn, tn
print "False negatives: %s, False positives: %s" % (fn, fp)
f1 = 2 * ((precision*recall)/(precision + recall))
print "F1 score:", round(f1*100,3)

# no more libsvm fucks
# aight ... #
#prob = svm_prob(y,X)
#param = svm_parameter()
#param.kernel_type = LINEAR
#param.C = 10
#svm_train(prob,param)

#out = []
#svm_predict(out, [False for i in range(1000)])

