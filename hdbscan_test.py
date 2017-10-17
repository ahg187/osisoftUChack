# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:24:12 2017

@author: hacker22
"""

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import data_loader
import data_sender
from anomaly_detector import get_outliers


# get data for production sites
df, path_list = data_loader.get_qual_data(level='site', resolution='12H', history=500)
# outliers = get_outliers(df.loc[df.location==df.location.unique()[0], :], plot=True, min_cluster=15, min_sample=15)
# run anomaly detection on all sites
outlier_list = []
for location in df.location.unique():
    print(location)
    df_tmp = df.loc[df.location==location, :]
    outliers = get_outliers(df_tmp, plot=False, min_cluster=15, min_sample=15)
    outlier_list.append(outliers)
data_sender.send_outlier_values(outlier_list=outlier_list, path_list=path_list)



# get data for Intellitect locations
df, path_list = data_loader.get_qual_data(level='intellitect', resolution='15M', history=100)
# outliers = get_outliers(df.loc[df.location==df.location.unique()[0], :], plot=True, min_cluster=350, min_sample=350)
# run anomaly detection on all sites
outlier_list = []
for location in df.location.unique():
    df_tmp = df.loc[df.location==location, :]
    outliers = get_outliers(df_tmp, plot=False, min_cluster=350, min_sample=350)
    outlier_list.append(outliers)
data_sender.send_outlier_values(outlier_list=outlier_list, path_list=path_list)



# get data for nano locations
df, path_list = data_loader.get_qual_data(level='nano', resolution='15M', history=100)
# outliers = get_outliers(df.loc[df.location==df.location.unique()[6], :], plot=True, min_cluster=450, min_sample=450)
# run anomaly detection on all sites
outlier_list = []
for location in df.location.unique():
    df_tmp = df.loc[df.location==location, :]
    outliers = get_outliers(df_tmp, plot=False, min_cluster=450, min_sample=450)
    outlier_list.append(outliers)
data_sender.send_outlier_values(outlier_list=outlier_list, path_list=path_list)



