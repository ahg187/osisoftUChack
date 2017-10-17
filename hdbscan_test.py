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

import data_loader
from anomaly_detector import get_outliers



# get data for production sites
df, path_list = data_loader.get_qual_data(level='site', resolution='12H', history=1000)
outliers = get_outliers(df.loc[df.location==df.location.unique()[0], :], plot=True, min_cluster=15, min_sample=15)
# run anomaly detection on all sites
outlier_list = []
for location in df.location.unique():
    df_tmp = df.loc[df.location==location, :]
    outliers = get_outliers(df_tmp, plot=False, min_cluster=15, min_sample=15)
    outlier_list.append(outliers)



# get data for Intellitect locations
df, path_list = data_loader.get_qual_data(level='intellitect', resolution='10T', history=300)
outliers = get_outliers(df.loc[df.location==df.location.unique()[4], :], plot=True, min_cluster=2500, min_sample=2500)
# run anomaly detection on all sites
outlier_list = []
for location in df.location.unique():
    df_tmp = df.loc[df.location==location, :]
    outliers = get_outliers(df_tmp, plot=False, min_cluster=2500, min_sample=2500)
    outlier_list.append(outliers)



# get data for nano locations
df, path_list = data_loader.get_qual_data(level='nano', resolution='10T', history=200)
outliers = get_outliers(df.loc[df.location==df.location.unique()[9], :], plot=True, min_cluster=1200, min_sample=1200)
# run anomaly detection on all sites
outlier_list = []
for location in df.location.unique():
    df_tmp = df.loc[df.location==location, :]
    outliers = get_outliers(df_tmp, plot=False, min_cluster=1200, min_sample=1200)
    outlier_list.append(outliers)

