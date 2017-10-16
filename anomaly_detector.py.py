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


def get_outliers(df):

    for location in df.location.unique():

        cols = df.columns.values[df.columns.values != 'location']
        data = df.loc[df.location==location, cols].dropna()
        time = data.index
        data = data.values
        scaler = StandardScaler()
        data_scl = scaler.fit_transform(X=data)

        clusterer = hdbscan.HDBSCAN(min_cluster_size=15).fit(data_scl)
        clusterer.outlier_scores_

        #sns.distplot(clusterer.outlier_scores_[np.isfinite(clusterer.outlier_scores_)], rug=True)

        threshold = pd.Series(clusterer.outlier_scores_).quantile(0.9)
        idx_outliers = np.where(clusterer.outlier_scores_ > threshold)[0]

        outliers = np.zeros((data.shape[0],1))
        outliers[idx_outliers] = 1

        outliers = pd.DataFrame(data=outliers, index=time, columns=[location + ' outlier'])


        return outliers



if __name__ == main():

    plt.scatter(np.arange(data.shape[0]), data[:,0].T, s=50, linewidth=0, c='gray', alpha=0.25)
    plt.scatter(outliers, data[outliers,0].T, s=50, linewidth=0, c='red', alpha=0.5)
    plt.scatter(np.arange(data.shape[0]), data[:,1].T, s=50, linewidth=0, c='gray', alpha=0.25)
    plt.scatter(outliers, data[outliers,1].T, s=50, linewidth=0, c='red', alpha=0.5)
    plt.scatter(np.arange(data.shape[0]), data[:,2].T, s=50, linewidth=0, c='gray', alpha=0.25)
    plt.scatter(outliers, data[outliers,2].T, s=50, linewidth=0, c='red', alpha=0.5)
