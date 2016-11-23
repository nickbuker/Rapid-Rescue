import random
import numpy as np
from geopy.distance import vincenty
from collections import defaultdict


def clusterer(X, k=5, max_iter=1000):
    """
    Inputs:
    X = 2 x m dataframe of latitude and longitude (float)
    k = number of centroids to use (int)
    max_iter = maximum number of iteratations (int)
    Return:
    centoids = dataframe latitude and longitude of centroids (float)
    clusters = dict mapping centoids to observations
    """

    if k == 0:
        centroids = []
        clusters = {}
        return centroids, clusters

    # Zip data latitude and longitude into tuples for Vincenty distance
    lats = [lat for lat in X.Latitude]
    longs = [long_ for long_ in X.Longitude]
    X_list = zip(lats, longs)

    # Zip centroid latitude and longitude into tuples for Vincenty distance
    lats_cent = [lat for lat in random.sample(X.Latitude, k)]
    longs_cent = [long_ for long_ in random.sample(X.Longitude, k)]
    centroids = zip(lats_cent, longs_cent)

    for i in xrange(max_iter):
        clusters = defaultdict(list)
        # Assign each point to nearest cluster for nearest centroid
        for x in X_list:
            distances = [vincenty(x, centroid) for centroid in centroids]
            centroid = centroids[np.argmin(distances)]
            clusters[centroid].append(x)

        # Move centroids to center of their clusters
        new_centroids = []
        for centroid, pts in clusters.iteritems():
            new_centroid = np.mean(pts, axis=0)
            new_centroids.append(tuple(new_centroid))

        # Stop iterating if optimized else use new centroids for next iter
        if set(new_centroids) == set(centroids):
            break
        else:
            centroids = new_centroids

    return centroids, clusters
