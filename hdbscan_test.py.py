# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:24:12 2017

@author: hacker22
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import mahalanobis
import hdbscan
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import seaborn as sns

from data_loader import get_qual_data




# get data
df = get_qual_data(level='site', resolution='12H', history=2000)


for site in df.location.unique():

    data = df.loc[df.location==site, ['pH', 'Conductivity', 'Turbidity']].dropna()
    time = data.index
    data = data.values
    scaler = StandardScaler()
    data_scl = scaler.fit_transform(X=data)

    clusterer = hdbscan.HDBSCAN(min_cluster_size=15).fit(data_scl)
    clusterer.outlier_scores_

    #sns.distplot(clusterer.outlier_scores_[np.isfinite(clusterer.outlier_scores_)], rug=True)

    threshold = pd.Series(clusterer.outlier_scores_).quantile(0.9)
    outliers = np.where(clusterer.outlier_scores_ > threshold)[0]


    plt.scatter(np.arange(data.shape[0]), data[:,0].T, s=50, linewidth=0, c='gray', alpha=0.25)
    plt.scatter(outliers, data[outliers,0].T, s=50, linewidth=0, c='red', alpha=0.5)
    plt.scatter(np.arange(data.shape[0]), data[:,1].T, s=50, linewidth=0, c='gray', alpha=0.25)
    plt.scatter(outliers, data[outliers,1].T, s=50, linewidth=0, c='red', alpha=0.5)
    plt.scatter(np.arange(data.shape[0]), data[:,2].T, s=50, linewidth=0, c='gray', alpha=0.25)
    plt.scatter(outliers, data[outliers,2].T, s=50, linewidth=0, c='red', alpha=0.5)
