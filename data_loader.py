# -*- coding: utf-8 -*-

import pandas as pd
import datetime as dt
import numpy as np
from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient

client = PIWebApiClient("https://proghackuc2017.osisoft.com/piwebapi", False, "hacker22", "orangeTigerGlas#7", True)  

def get_qual_data(level='site', resolution='12H' history=2000):

    if level == 'site':
        
        base_path = "af:\\\\SATURN022\\Vitens\\Vitens\\Friesland province\\01 Production sites\\"
        prod_sites = ["Production Site Noordbergum", "Production Site Oldeholtpade", "Production Site Spannenburg", "Production Site Terwisscha"]
        
        out = pd.DataFrame()

        for site in prod_sites:
            qual_signals = ["\\Distribution\\Quality|pH", "\\Distribution\\Quality|Conductivity", "\\Distribution\\Quality|Turbidity"]
            paths = [base_path + site + qual_signal for qual_signal in qual_signals]
            df_dict = client.data.get_multiple_recorded_values(paths, None, "*", None, None, None, None, "*-"+str(history)+"d", None)
            
            df = pd.DataFrame()
            
            for path in paths:
                
                df_tmp = client.data.get_recorded_values(path, None, None, "*-"+str(history)+"d", None, None, 100000, None, "*-10d", None)
                df_tmp = df_tmp.loc[:,['Timestamp','Value']]
                is_numeric = lambda x: type(x) in [int, np.int64, float, np.float64]
                parser = lambda x: dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
                
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
            
    return out
