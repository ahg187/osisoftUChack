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


def get_qual_data(level='site', resolution='12H', history=2000):
    if level == 'site':
        base_path = "af:\\\\SATURN024\\Vitens\\Vitens\\Friesland province\\01 Production sites\\"
        prod_sites = ["Production Site Noordbergum", "Production Site Oldeholtpade", "Production Site Spannenburg",
                      "Production Site Terwisscha"]

        out = pd.DataFrame()

        for site in prod_sites:
            qual_signals = ["\\Distribution\\Quality|pH", "\\Distribution\\Quality|Conductivity", "\\Distribution\\Quality|Turbidity"]
            paths = [base_path + site + qual_signal for qual_signal in qual_signals]
            df = pd.DataFrame()

            for path in paths:
                df_tmp = client.data.get_recorded_values(path, None, None, "*-"+str(history)+"d", None, None, 100000, None, "*-10d", None)
                df_tmp = df_tmp.loc[:,['Timestamp','Value']]
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

            out = pd.concat([out,df])

    elif level == 'intellitect':
        base_path = "af:\\\\SATURN024\\Vitens\\Vitens\\Friesland province\\03 Peripheral measurements\\Intellitect " \
                    "Intellisonde\\"

        prod_intellitects = ["Location FR-OWIR1", "Location FR-PNB_1", "Location FR-PNB_2", "Location FR-RFNK1",
                             "Location FR-RLWG1"]

        out = pd.DataFrame()

        for intellitect in prod_intellitects:
            measurements = ["|Conductivity", "|ORP", "|pH", "|Temperature"]
            paths = [base_path + intellitect + measurement for measurement in measurements]
            df = pd.DataFrame()

            for path in paths:
                df_tmp = client.data.get_recorded_values(path, None, None, "*-" + str(history) + "d", None, None,
                                                         100000, None, "*-10d", None)
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

            df['location'] = intellitect

            out = pd.concat([out, df])
            
    return out


df = get_qual_data(level='intellitect')
