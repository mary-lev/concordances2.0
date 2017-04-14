#!/usr/bin/env python
# coding: utf8
from gluon import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.manifold import MDS
import pandas as pd
import numpy as np

def draw(array, names, filename):
    num_clusters = 4
    km = KMeans(n_clusters=num_clusters)
    km.fit(array)
    dist = 1 - cosine_similarity(array)
    clusters = km.labels_.tolist()
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    pos = mds.fit_transform(dist)  # shape (n_components, n_samples)
    xs, ys = pos[:, 0], pos[:, 1]
    df = pd.DataFrame(dict(x=xs, y=ys, label=clusters, title=names))
    groups = df.groupby('label')
    # set up plot
    fig, ax = plt.subplots(figsize=(14, 8)) # set size
    ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
    for name, group in groups:
        ax.plot(group.x, group.y, marker='o', linestyle='', ms=12, mec='none')
        ax.set_aspect('auto')
        ax.tick_params(\
                       axis= 'x',          # changes apply to the x-axis
                       which='both',      # both major and minor ticks are affected
                       bottom='off',      # ticks along the bottom edge are off
                       top='off',         # ticks along the top edge are off
                       labelbottom='off')
        ax.tick_params(\
                       axis= 'y',         # changes apply to the y-axis
                       which='both',      # both major and minor ticks are affected
                       left='off',      # ticks along the bottom edge are off
                       top='off',         # ticks along the top edge are off
                       labelleft='off')

    ax.legend(numpoints=1)  #show legend with only 1 point

    #add label in x,y position with the label as the film title
    for i in range(len(df)):
        ax.text(df.ix[i]['x'], df.ix[i]['y'], df.ix[i]['title'], size=10)
    f = '/home/concordance/web2py/applications/test/static/' + filename
    plt.savefig(f) #show the plot
