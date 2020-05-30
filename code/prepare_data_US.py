import pandas as pd
import urllib.request
import json

def get_US_Confirmed_DF(filename):
    df = pd.read_csv(filename, delimiter=',')
    df = df.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Country_Region','Lat','Long_','Combined_Key'])
    df = df.groupby(['Province_State'],as_index=False).sum()
    columns = df.columns.tolist()
    dates = columns[1:]
    start = dates[0]
    end = dates[-1]
    date_range = pd.date_range(start=start, end=end)
    df.columns = ['Province_State'] + [i for i in range(0,len(date_range))]
    return [df, start, end, dates]

def get_US_Death_DF(filename):
    df = pd.read_csv(filename, delimiter=',')
    df = df.drop(columns=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Country_Region', 'Lat', 'Long_','Combined_Key','Population'])
    df = df.groupby(['Province_State'], as_index=False).sum()
    columns = df.columns.tolist()
    dates = columns[1:]
    start = dates[0]
    end = dates[-1]
    date_range = pd.date_range(start=start, end=end)
    df.columns = ['Province_State'] + [i for i in range(0, len(date_range))]
    return [df, start, end, dates]

def update():
    url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
    filename_confirmed = '../data/raw/us/time_series_covid19_confirmed_US.csv'
    url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
    filename_deaths = '../data/raw/us/time_series_covid19_deaths_US.csv'

    print(f'Downloading {url_confirmed}')
    filename_confirmed, headers_confirmed = urllib.request.urlretrieve(url_confirmed, filename=filename_confirmed)
    print("download complete!")
    print("download file location: ", filename_confirmed)
    print("Processing")

    print(f'Downloading {url_deaths}')
    filename_deaths, headers_deaths = urllib.request.urlretrieve(url_deaths, filename=filename_deaths)
    print("download complete!")
    print("download file location: ", filename_deaths)
    print("Processing")

def prepare():
    filename_confirmed = '../data/raw/us/time_series_covid19_confirmed_US.csv'
    filename_deaths = '../data/raw/us/time_series_covid19_deaths_US.csv'

    [df, start, end, dates] = get_US_Confirmed_DF(filename_confirmed)
    df.to_csv('../data/processed/us/confirmed.csv', index=False)
    with open('../data/processed/us/confirmed.json', 'w', encoding='utf-8') as f:
        json.dump({'start':start, 'end': end, 'dates': dates}, f, ensure_ascii=False, indent=4)

    [df, start, end, dates] = get_US_Death_DF(filename_deaths)
    df.to_csv('../data/processed/us/deaths.csv', index=False)
    with open('../data/processed/us/deaths.json', 'w', encoding='utf-8') as f:
        json.dump({'start':start, 'end': end, 'dates': dates}, f, ensure_ascii=False, indent=4)