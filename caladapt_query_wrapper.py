# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 11:10:31 2019

@author: 18479
"""

import requests
import pandas as pd
import numpy as np
import json
## Two functions to pull in census tract data
def api_pull_censustractID():
    api_pull_censustractID.ftract={}
    if not api_pull_censustractID.ftract:
        for x in range(81):
            url=f"https://api.cal-adapt.org/api/censustracts/?page={x+1}&pagesize=100"
            response=requests.get(url)
            r=response.json()
            for dat in r['features']:
                api_pull_censustractID.ftract[dat['properties']['tract']]=str(dat['id'])
        api_pull_censustractID.hbr=True
    return api_pull_censustractID.ftract
def load_fromfile_censustractID():
    with open('caladapt_census_tracts_dict_ID.txt', 'r') as file:
        data=json.load(file)
    load_fromfile_censustractID.ftract=data
    load_fromfile_censustractID.hbr=True
    return load_fromfile_censustractID.ftract
##saves the census tracts as a file
def write_censustractID():
    if api_pull_censustractID.hbr:
        ftract=api_pull_censustractID.ftract
    else:
        ftract=api_pull_censustractID()
    with open('caladapt_census_tracts_dict_ID.txt', 'w') as file:
         file.write(json.dumps(ftract))
         
##find daily model names
url="https://api.cal-adapt.org/api/series/?pagesize=501"
response=requests.get(url)
r=response.json()
fmodel={}
for dat in r['results']:
    fmodel[dat['name']]=dat['slug']
with open('caladapt_types.txt', 'w') as file:
    file.write(json.dumps(fmodel))
    
## Available Functions
def load_tractID():
    load_tractID.has_been_called=True
    
def get_tractID(tract_number):
    return ftract[tract_number]
def daily_ct(model_slug,tract_number):
    url = f'http://api.cal-adapt.org/api/series/{model_slug}/events'
    params = {'ref': f"/api/censustracts/{ftract[tract_number]}/", 'stat':'mean'}
    headers = {'ContentType': 'json'}
    response = requests.get(url, params=params, headers=headers)
    r=response.json()
    dates=pd.to_datetime(r['index'])
    data={'temp':r['data']}
    return pd.DataFrame(data,index=dates)

def daily_ct_timerange(model_slug,tract_number,begin,end):
    begin_time=pd.to_datetime(begin)
    end_time=pd.to_datetime(end)
    whole_data=daily_ct_temp(model_slug,tract_number)
    return whole_data.loc[begin_time:end_time]

def daily_ct_year(model_slug,tract_number,year):
    begin=pd.to_datetime(f"{year}0101")
    end=pd.to_datetime(f"{year}1231")
    return daily_ct_timerange(model_slug,tract_number,begin,end)

def hist_ct_year(model_slug,tract_number,year):
    dat=daily_ct_year(model_slug,tract_number,year)['temp'].tolist()
    maxdat=int(max(dat))+3
    mindat=int(min(dat))-3
    binned=np.arange(mindat,maxdat,1)
    x=np.histogram(dat,bins=binned)
    return x