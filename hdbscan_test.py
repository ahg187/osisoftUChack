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



# get data
df = data_loader.get_qual_data(level='nano', resolution='12H', history=40)

outliers = get_outliers(df.loc[df.location==df.location.unique()[0], :], plot=True, min_cluster=2, min_sample=1)




# run anomaly detection on all sites
for site in df.location.unique():
    df_tmp = df.loc[df.location==site, :]
    outliers = get_outliers(df_tmp, plot=True)
