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


# get data
df, path_list = data_loader.get_qual_data(level='site', resolution='12H', history=40)

outliers = get_outliers(df.loc[df.location==df.location.unique()[0], :], plot=True, min_cluster=2, min_sample=1)
outlier_list = [outliers]
path_list = [path_list[0]]

data_sender.send_outlier_values([outliers], [path_list[0]])
