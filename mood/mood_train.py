#from svmutil import *
from sklearn import svm

import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join

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
x = neg + pos
y = [0 if i < 1000 else 1 for i in range(2000)]
print "x", len(x)
print "y", len(y)

clf = svm.SVC(kernel='rbf', gamma=0.1, C=10.)
clf.fit(x,y)


# plt.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=80,
#             facecolors='none', zorder=10)
# plt.scatter(y,x)

fp = 0 #false pos
fn = 0 #false neg
tn = 0 #true neg
tp = 0 #true pos

for pvec in pos:
    p = clf.predict(pvec)[0]
    if p:
        tp += 1
    else:
        fn += 1

for nvec in neg:
    p = clf.predict(nvec)[0]
    if p:
        fp += 1
    else:
        tn += 1

precision = tp / float(tp+fp)
recall    = tp / float(tp+fn)

print fp, tp, fn, tn
f1 = 2 * ((precision*recall)/(precision + recall))
print "f1:", round(f1*100,3), "%"

# no more libsvm fucks
# aight ... #
#prob = svm_prob(y,x)
#param = svm_parameter()
#param.kernel_type = LINEAR
#param.C = 10
#svm_train(prob,param)

#out = []
#svm_predict(out, [False for i in range(1000)])

