from sklearn.decomposition import PCA

from mpl_toolkits.mplot3d import Axes3D

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
X = neg + pos
y = [0 if i < 1000 else 1 for i in range(2000)]
print "X", len(X)
print "y", len(y)

p_comps = 3

pca = PCA(n_components=p_comps)
#pca.fit(X)
#PCA(copy=True, n_components=p_comps, whiten=False)
#print(pca.explained_variance_ratio_) 

X_r = pca.fit(X).transform(X)
# Percentage of variance explained for each components
print('explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))

tx = []
ty = []
tc = []
for i in range(len(X_r)):
    tx.append(X_r[i][0])
    ty.append(X_r[i][1])
    tc.append('r' if y[i] else 'b')

plt.figure()
plt.scatter(tx,ty,c=tc)
plt.legend()
plt.title('PCA of dataset')






# 3D
t3x = []
t3y = []
t3z = []
t3c = []
t3m = []
for i in range(len(X_r)):
    t3x.append(X_r[i][0])
    t3y.append(X_r[i][1])
    t3z.append(X_r[i][2])
    t3c.append('r' if y[i] else 'b')
    #t3m.append('o' if y[i] else '^')


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(t3x,t3y,t3z,c=t3c)
plt.legend()
plt.title('PCA 3D of dataset')

plt.show()
