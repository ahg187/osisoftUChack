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
from anomaly_detector import get_outliers



# get data
df = get_qual_data(level='site', resolution='12H', history=2000)
outliers = get_outliers(df.loc[df.location=='Production Site Oldeholtpade', :], plot=True)



# run anomaly detection on all sites
for site in df.location.unique():
    df_tmp = df.loc[df.location==site, :]
    outliers = get_outliers(df_tmp, plot=True)
