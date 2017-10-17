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

import datetime as dt
from osisoft.pidevclub.piwebapi.models.pi_stream_values import PIStreamValues
from osisoft.pidevclub.piwebapi.models.pi_timed_value import PITimedValue
from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient

client = PIWebApiClient("https://proghackuc2017.osisoft.com/piwebapi", False, "hacker23", "sickElephantHome#4", True)


def send_outlier_values(outlier_list, path_list):
    stream_values_list = []
    for i, outliers in enumerate(outlier_list):
        stream_values = PIStreamValues()
        parser = lambda x: dt.datetime.strftime(x, "%Y-%m-%dT%H:%M:%SZ")
        values = []
        for j in range(len(outliers)):
            pi_value = PITimedValue()
            timestamp = parser(outliers.index[j])
            value = outliers.iloc[j, 0]
            pi_value.value = value
            pi_value.timestamp = timestamp
            values.append(pi_value)

        stream_values.items = values
        path = path_list[i] + '|Qual_anomaly_trg'
        stream_values.web_id = client.attribute.get_by_path(path, None).links['Point'].split('/')[-1]
        #stream_values_list.append(stream_values)
        stream_values_list = [stream_values]

        response = client.streamSet.update_values_ad_hoc_with_http_info(stream_values_list, None, None)
        return response





