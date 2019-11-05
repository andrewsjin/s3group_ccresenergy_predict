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
def api_pull_censustractID(writer=True):
    api_pull_censustractID.ftract={}
    if not api_pull_censustractID.ftract:
        for x in range(81):
            url=f"https://api.cal-adapt.org/api/censustracts/?page={x+1}&pagesize=100"
            response=requests.get(url)
            r=response.json()
            for dat in r['features']:
                api_pull_censustractID.ftract[str(dat['properties']['tract'])]=str(dat['id'])
        api_pull_censustractID.hbr=True
        if writer:
            with open('caladapt_census_tracts_dict_ID.txt', 'w') as file:
                file.write(json.dumps(api_pull_censustractID.ftract))
    return api_pull_censustractID.ftract
def load_fromfile_censustractID():
    with open('caladapt_census_tracts_dict_ID.txt', 'r') as file:
        data=json.load(file)
    load_fromfile_censustractID.ftract=data
    load_fromfile_censustractID.hbr=True
    return load_fromfile_censustractID.ftract
         
## Two functions to pull in model names
def api_pull_modelslugs(writer=True): 
    api_pull_censustractID.fmodel={}
    if not api_pull_censustractID.fmodel:
        url="https://api.cal-adapt.org/api/series/?pagesize=501"
        response=requests.get(url)
        r=response.json()
        for dat in r['results']:
            api_pull_censustractID.fmodel[dat['name']]=dat['slug']
            api_pull_censustractID.hbr=True 
        api_pull_modelslugs.hbr=True
        if writer:
            with open('caladapt_types.txt', 'w') as file:
                file.write(json.dumps(api_pull_censustractID.fmodel))
    return api_pull_censustractID.fmodel
def load_fromfile_modelslugs():
    with open('caladapt_census_tracts_dict_ID.txt', 'r') as file:
        data=json.load(file)
    load_fromfile_modelslugs.ftract=data
    load_fromfile_modelslugs.hbr=True
    return load_fromfile_censustractID.ftract       

    
## Available Functions    
def get_tractID(tract_number):
    tract=str(tract_number)
    try:
        return get_tractID.ftract[tract]
    except:
        try:
            get_tractID.ftract=load_fromfile_censustractID()
        except:
            get_tractID.ftract=api_pull_censustractID(True)
    return get_tractID.ftract[tract]



def daily_ct(model_slug,tract_number):
    url = f'http://api.cal-adapt.org/api/series/{model_slug}/events'
    params = {'ref': f"/api/censustracts/{get_tractID(tract_number)}/", 'stat':'mean'}
    headers = {'ContentType': 'json'}
    response = requests.get(url, params=params, headers=headers)
    r=response.json()
    dates=pd.to_datetime(r['index'])
    data={'temp':r['data']}
    return pd.DataFrame(data,index=dates)

def daily_ct_timerange(model_slug,tract_number,begin,end):
    begin_time=pd.to_datetime(begin)
    end_time=pd.to_datetime(end)
    whole_data=daily_ct(model_slug,tract_number)
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