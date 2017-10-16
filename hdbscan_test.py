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
df = data_loader.get_qual_data(level='nano', resolution='12H', history=200)
outliers = get_outliers(df.loc[df.location==df.location.unique()[0], :], plot=True)



# run anomaly detection on all sites
for site in df.location.unique():
    df_tmp = df.loc[df.location==site, :]
    outliers = get_outliers(df_tmp, plot=True)
