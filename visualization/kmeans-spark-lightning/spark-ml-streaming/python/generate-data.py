import time
import os
from numpy import asarray, array, vstack, hstack, size, random, argsort, ones, argmin, sin, cos, pi
from scipy.spatial.distance import cdist
from sklearn.datasets import make_blobs

#seed=0
ncenters=3
npoints=50
ndims=2
cluster_std=1
datain_dir="/tmp/mlstreaming-tmp/streamkmeans/input"
timestamp = int(time.time())

def writepoints( pts):
	filename = 'batch%i.txt' % timestamp
	filepath = os.path.join(datain_dir, filename)
	print("writing to fiel path: %s" % filepath)
	f = open(filepath, 'w')
	s = map(lambda p: ",".join(str(p).split()).replace('[,', '[').replace(',]', ']'), pts)
	tmp = "\n".join(s)
	f.write(tmp)
	f.close()


#random.seed(seed)
if size(ncenters) == 1:
	centers = random.randn(ncenters, ndims) * 2
else:
	centers = asarray(ncenters)
	ncenters = centers.shape[0]


# drift means the points will slowly drift by adding noise to the position
centers += random.randn(centers.shape[0], centers.shape[1]) * 0.15

# generate the points by sampling from the clusters and write to disk
pts, labels = make_blobs(npoints, ndims, centers, cluster_std=cluster_std)
writepoints(pts)

