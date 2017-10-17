# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:24:12 2017

@author: hacker22
"""

import pandas as pd
import datetime as dt
import numpy as np
from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient

client = PIWebApiClient("https://proghackuc2017.osisoft.com/piwebapi", False, "hacker23", "sickElephantHome#4", True)


def get_sub_element_names(base_path):
    base_element = client.element.get_by_path(base_path, None)
    elements = client.element.get_elements(base_element.web_id, None, None, None, None, None, None, None, None,
                                           None, None, None)

    element_list = []

    for item in elements.items:
        element_list.append(item.name)

    return element_list


def get_sub_attribute_names(base_path, sub_path=""):
    base_element = client.element.get_by_path(base_path + sub_path, None)
    attributes = client.element.get_attributes(base_element.web_id, None, None, None, None, None, None, None, None,
                                               None, None, None, "Double")

    attribute_list = []

    for item in attributes.items:
        if item.name not in ['Latitude', 'Longitude', 'Qual_anomaly_trg']:
            attribute_list.append(item.name)

    return attribute_list


def get_data_frame_for_level(base_path, resolution, history, sub_path=""):
    af_base_path = "af:" + base_path + "\\"
    element_names = get_sub_element_names(base_path)
    out = pd.DataFrame()
    for element_name in element_names:

        attribute_names = get_sub_attribute_names(base_path + "\\" + element_name, sub_path)
        paths = [af_base_path + element_name + sub_path + "|" + attribute for attribute in attribute_names]

        # dfs_tmp = client.data.get_multiple_recorded_values(paths, None, None, None, None, 50000, None, "*-" + str(history) + "d", None)

        df = client.data.get_multiple_interpolated_values(paths, start_time="*-" + str(history) + "d", interval=resolution, end_time='*-20d', filter_expression=None, include_filtered_values=False, selected_fields=None, time_zone=None)

        # df = pd.DataFrame()
        #
        # for path in paths:
        #     df_tmp = dfs_tmp[path].loc[:, ['Timestamp', 'Value']]
        #     is_numeric = lambda x: type(x) in [int, np.int64, float, np.float64]
        #     parser = lambda x: dt.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S")
        #
        #     df_tmp.Timestamp = df_tmp.Timestamp.apply(parser)
        #     df_tmp = df_tmp[df_tmp.Value.apply(is_numeric)]
        #
        #     df_tmp.index = df_tmp.Timestamp
        #     df_tmp = df_tmp.drop('Timestamp', axis=1)
        #
        #     name = path.split('|')[-1]
        #     df_tmp.columns.values[0] = name
        #
        #     df = df.merge(right=df_tmp, how='outer', left_index=True, right_index=True)
        #
        # df = df.astype(np.float32)
        # df = df.resample(resolution).mean()


        parser = lambda x: dt.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S")
        is_numeric = lambda x: type(x) in [int, np.int64, float, np.float64]
        df = df.loc[:,['Timestamp1'] + ['Value'+str(i) for i in range(1,len(attribute_names)+1)]]
        df.Timestamp1 = df.Timestamp1.apply(parser)
        df.index = df.Timestamp1
        df = df.drop('Timestamp1', axis=1)
        # df = df[df.apply(is_numeric)]
        df.columns = attribute_names

        for col in df.columns.values:
            df = df[pd.to_numeric(df[col], errors='coerce').notnull()]

        df['location'] = element_name

        out = pd.concat([out, df])


    return out, element_names




def get_qual_data(level='site', resolution='12H', history=2000):
    if level == 'site':
        base_path = "\\\\SATURN023\\Vitens\\Vitens\\Friesland province\\01 Production sites"
        sub_path = "\\Distribution\\Quality"
        out, elements = get_data_frame_for_level(base_path, resolution, history, sub_path)

    elif level == 'intellitect':
        base_path = "\\\\SATURN023\\Vitens\\Vitens\\Friesland province\\03 Peripheral measurements\\Intellitect " \
                    "Intellisonde"

        sub_path = ""
        out, elements = get_data_frame_for_level(base_path, resolution, history)

    elif level == 'nano':
        base_path = "\\\\SATURN023\\Vitens\\Vitens\\Friesland province\\03 Peripheral measurements\\s::can " \
                    "nano::station"

        sub_path = ""
        out, elements = get_data_frame_for_level(base_path, resolution, history)

    path_list = [base_path + '\\' + element + sub_path for element in elements]

    return out, path_list

