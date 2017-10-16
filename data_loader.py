# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:24:12 2017

@author: hacker22
"""

import pandas as pd
import datetime as dt
import numpy as np
from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient

client = PIWebApiClient("https://proghackuc2017.osisoft.com/piwebapi", False, "hacker24", "blueAleDoor#4", True)


def get_data_frame_for_level(base_path, element_names, attributes, resolution, history):
    out = pd.DataFrame()

    for site in element_names:
        paths = [base_path + site + attribute for attribute in attributes]
        df = pd.DataFrame()

        for path in paths:
            df_tmp = client.data.get_recorded_values(path, None, None, "*-" + str(history) + "d", None, None, 100000,
                                                     None, "*-10d", None)
            df_tmp = df_tmp.loc[:, ['Timestamp', 'Value']]
            is_numeric = lambda x: type(x) in [int, np.int64, float, np.float64]
            parser = lambda x: dt.datetime.strptime(x[:19], "%Y-%m-%dT%H:%M:%S")

            df_tmp.Timestamp = df_tmp.Timestamp.apply(parser)
            df_tmp = df_tmp[df_tmp.Value.apply(is_numeric)]

            df_tmp.index = df_tmp.Timestamp
            df_tmp = df_tmp.drop('Timestamp', axis=1)

            name = path.split('|')[-1]
            df_tmp.columns.values[0] = name

            df = df.merge(right=df_tmp, how='outer', left_index=True, right_index=True)

        df = df.astype(np.float32)
        df = df.resample(resolution).mean()

        df['location'] = site

        return pd.concat([out, df])


def get_qual_data(level='site', resolution='12H', history=2000):
    if level == 'site':
        base_path = "af:\\\\SATURN024\\Vitens\\Vitens\\Friesland province\\01 Production sites\\"
        prod_sites = ["Production Site Noordbergum", "Production Site Oldeholtpade", "Production Site Spannenburg",
                      "Production Site Terwisscha"]

        qual_signals = ["\\Distribution\\Quality|pH", "\\Distribution\\Quality|Conductivity",
                        "\\Distribution\\Quality|Turbidity"]

        out = get_data_frame_for_level(base_path, prod_sites, qual_signals, resolution, history)

    elif level == 'intellitect':
        base_path = "af:\\\\SATURN024\\Vitens\\Vitens\\Friesland province\\03 Peripheral measurements\\Intellitect " \
                    "Intellisonde\\"

        prod_intellitects = ["Location FR-OWIR1", "Location FR-PNB_1", "Location FR-PNB_2", "Location FR-RFNK1",
                             "Location FR-RLWG1"]

        measurements = ["|Conductivity", "|ORP", "|pH", "|Temperature"]

        out = get_data_frame_for_level(base_path, prod_intellitects, measurements, resolution, history)

    elif level == 'stations':
        base_path = "af:\\\\SATURN024\\Vitens\\Vitens\\Friesland province\\03 Peripheral measurements\\s::can " \
                    "nano::station\\"

        prod_stations = ["Location FR-MDKM", "Location FR-MFRI", "Location FR-MLAB", "Location FR-MLWU",
                             "Location FR-MNBU", "Location FR-MRGR", "Location FR-MRSH", "Location FR-MRSJ",
                             "Location FR-MSBA", "Location FR-MWIA"]

        measurements = ["|COLORapp", "|COLORtru", "|Conductivity", "|DOCeq", "|DOCeq2", "|Flow", "|pH", "|Temperature",
                        "|TOCeq2", "|Turb_EPA", "|Turb_ISO", "|UV254"]

        out = get_data_frame_for_level(base_path, prod_stations, measurements, resolution, history)
            
    return out


df = get_qual_data(level='stations')
