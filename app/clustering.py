import numpy as np
import random
from geopy.distance import vincenty
from collections import defaultdict


def clusterer(data, max_iter=1000, limit=True):
    """
    Inputs:
    X = 2 x m dataframe of latitude and longitude (float)
    k = number of centroids to use (int)
    max_iter = maximum number of iteratations (int)
    Return:
    centoids = dataframe latitude and longitude of centroids (float)
    clusters = dict mapping centoids to observations
    """
    X = data[0]
    k = data[1]
    rand_state = 42
    # Loop for checking lost centroids due key duplications in dict
    while True:
        if k == 0:
            centroids = []
            clusters = {}
            return centroids, clusters

        # Limit size of history for faster clustering
        if limit ==  True and len(X) > 500:
            X = X.sample(n=500, random_state=rand_state)

        # Zip data latitude and longitude into tuples for Vincenty distance
        lats = [lat for lat in X.Latitude]
        longs = [long_ for long_ in X.Longitude]
        X_list = zip(lats, longs)

        # Zip centroid latitude and longitude into tuples for Vincenty distance
        cent_df = X.sample(n=k, random_state=rand_state)
        lats_cent = cent_df.Latitude
        longs_cent = cent_df.Longitude
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

        # Check for lost centroids due to key duplicatiosn in dict
        if len(centroids) == k:
            return centroids, clusters

        # Change random state to avoid infinite loop
        rand_state += 1
