import pandas as pd
import urllib.request
import json

def get_resultant_DF(countryList, df):
    dfList =[]
    for country in countryList:
        tdf = df[(df['Country/Region']==country) & (df['Province/State'].isnull())]
        dfList.append(tdf)
    df = pd.concat(dfList)
    df = df.drop(columns=['Province/State', 'Lat', 'Long'])
    columns = df.columns.tolist()
    dates = columns[1:]
    start = dates[0]
    end = dates[-1]
    date_range = pd.date_range(start=start, end=end)
    df.columns = ['Province_State'] + [i for i in range(0,len(date_range))]
    return [df, start, end, dates]


def get_OTH_Confirmed_DF(filename,countryList):
    df = pd.read_csv(filename, delimiter=',')
    return get_resultant_DF(countryList, df)

def get_OTH_Death_DF(filename,countryList):
    df = pd.read_csv(filename, delimiter=',')
    return get_resultant_DF(countryList, df)


def update():
    url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    filename_confirmed = '../data/raw/global/time_series_covid19_confirmed_global.csv'
    url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    filename_deaths = '../data/raw/global/time_series_covid19_deaths_global.csv'

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
    filename_confirmed = '../data/raw/global/time_series_covid19_confirmed_global.csv'
    filename_deaths = '../data/raw/global/time_series_covid19_deaths_global.csv'

    countryList = ["France", "Italy", "Spain", "Germany", "Iran", "Sweden", "Brazil", "Russia", "United Kingdom", "Turkey", "Belgium", "Netherlands"]

    [df, start, end, dates] = get_OTH_Confirmed_DF(filename_confirmed,countryList)
    df.to_csv('../data/processed/other/confirmed.csv', index=False)
    with open('../data/processed/other/confirmed.json', 'w', encoding='utf-8') as f:
        json.dump({'start':start, 'end': end, 'dates': dates}, f, ensure_ascii=False, indent=4)

    [df, start, end, dates] = get_OTH_Death_DF(filename_deaths,countryList)
    df.to_csv('../data/processed/other/deaths.csv', index=False)
    with open('../data/processed/other/deaths.json', 'w', encoding='utf-8') as f:
        json.dump({'start':start, 'end': end, 'dates': dates}, f, ensure_ascii=False, indent=4)



