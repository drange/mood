from sklearn.decomposition import PCA

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

filenames = []
def get_vectors(pth):
    global filenames
    vecs = []
    data_files = [f for f in listdir(pth) if isfile(join(pth, f))]
    for fname in data_files:
        with open(pth + "/" + fname) as f:
            vec = []
            for l in f:
                for x in l.split():
                    vec.append(int(x))
            vecs.append(vec)
            filenames.append(pth+"/"+fname)
    return vecs

# [[0, 1, 1, ...], [...], [...]] 1000 x 1000 bool vectors
neg = get_vectors("negative")
pos = get_vectors("positive")
X = neg + pos
y = [0 if i < 1000 else 1 for i in range(2000)]
print "X", len(X)
print "y", len(y)

least_variance = 1
p_comps = 1
while least_variance > 0.005:
    pca = PCA(n_components=p_comps)
    X_r = pca.fit(X).transform(X)
    least_variance=round(pca.explained_variance_ratio_[p_comps - 1],5)
    print least_variance
    p_comps += 1
    print '%f%% variance in the %d component' % (round(100*least_variance,3), (p_comps-1))

for i in range(len(X_r)):
    x_c, y_c = X_r[i][0],X_r[i][1]
    if (x_c < -1 and y_c < -2.3) or x_c < -5.5:
        print filenames[i]

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
