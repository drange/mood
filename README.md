# mood, in a sentimental

This program takes two folders "pos" and "neg" containing positive
(resp. negative) text files and learn to predict the mood of a new text file.

The algorithm proceeds as follows:
* Tokenize, lemmatize and remove stop words for every data point
* Pick up 1000 "good" words (how?)
* Create a vector consisting of 1000 words
* For each input data file, construct a 1000 dimensional boolean vector being the characteristic function of the words vector
* Train an SVM (with radial basis function (Gaussian) kernel) on the dataset
* ???
* Predict.

Using 20% cross validation (will update to 10-fold CV later) the predictor today
(with the given words.txt file) achieves ~80% correctness.

There is also a PCA implementation which maps the dataset to a 2 and 3
dimensional hyperplane and visualizes that using matplotlib.

The PCA in 2D (here is a [visualization of the 3D plot](https://gfycat.com/SingleVerifiableDiscus)):

![2D PCA](http://i.stack.imgur.com/4Uxya.png)
