# -*- coding: utf-8 -*-

# Copyright 2017 Alexander Gleim, Christopher Schroepfer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import hdbscan
import matplotlib.pyplot as plt
from matplotlib import dates
plt.style.use('ggplot')


def get_outliers(df, min_cluster=10, min_sample=10, plot=False):

    # drop columns if values are constant
    # drop columns if too little non-nan values in column

    cols_delete = ['location']

    for i, col in enumerate(df.columns):
        if col == 'location':
            continue
        else:
            vals = df.iloc[:,i].values.astype(float)
            ratio_nan = np.sum(np.isnan(vals)) / len(vals)
            if np.nanstd(vals) == 0.0 or ratio_nan > 0.5:
                cols_delete.append(col)

    cols = df.columns.values[~np.in1d(df.columns.values, cols_delete)]
    location = df.location.unique()[0]
    data = df.loc[df.location==location, cols].dropna()
    time_idx = data.index
    data = data.values.astype(float)
    scaler = StandardScaler()
    data_scl = scaler.fit_transform(X=data)

    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster, min_samples=min_sample).fit(data_scl)
    threshold = pd.Series(clusterer.outlier_scores_).quantile(0.85)
    outliers_idx = np.where(clusterer.outlier_scores_ > threshold)[0]

    outliers = np.zeros((data.shape[0],1))
    outliers[outliers_idx] = 1
    outliers = pd.DataFrame(data=outliers, index=time_idx, columns=[location])

    if plot:
        dts = list(map(lambda x: x.to_pydatetime(), time_idx))
        fds = dates.date2num(dts)
        hfmt = dates.DateFormatter('%Y-%m-%d %H:%M')
        times = np.zeros(data.shape)

        for i in range(times.shape[1]):
            times[:,i] = fds

        fig, ax = plt.subplots(1,1)
        ax.scatter(times.T, data.T,  s=50, linewidth=0, c='gray', alpha=0.25)
        ax.scatter(times[outliers_idx,:].T, data[outliers_idx,:].T, s=50, linewidth=0, c='red', alpha=0.5)
        ax.xaxis.set_major_formatter(hfmt)

    return outliers
