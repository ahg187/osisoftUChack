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
import datetime as dt
from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient

client = PIWebApiClient("https://proghackuc2017.osisoft.com/piwebapi", False, "hacker23", "sickElephantHome#4", True)
# client = PIWebApiClient("https://proghackuc2017.osisoft.com/piwebapi", False, "hacker24", "blueAleDoor#4", True)


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

        df = client.data.get_multiple_interpolated_values(paths, start_time="*-" + str(history) + "d",
                                                          interval=resolution, end_time='*-20d', filter_expression=None,
                                                          include_filtered_values=False, selected_fields=None,
                                                          time_zone=None)

        parser = lambda x: dt.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S")
        df = df.loc[:,['Timestamp1'] + ['Value'+str(i) for i in range(1,len(attribute_names)+1)]]
        df.Timestamp1 = df.Timestamp1.apply(parser)
        df.index = df.Timestamp1
        df = df.drop('Timestamp1', axis=1)
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
    else:
        raise ValueError('the specified level %s is not a valid level' % level)

    path_list = [base_path + '\\' + element + sub_path for element in elements]

    return out, path_list

