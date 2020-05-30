import pandas as pd
import urllib.request
import json
import datetime

def get_IN_DF(filename):

    df = pd.read_csv(filename, delimiter=',')
    df_confirmed = df[df['Status'] == 'Confirmed']
    df_deceased = df[df['Status'] == 'Deceased']

    dates = []

    for d in list(df['Date']):
        dt = datetime.datetime.strptime(d, '%d-%b-%y')
        s = f'{dt.month}/{dt.day}/{dt.year % 100}'
        dates.append(s)

    start = dates[0]
    end = dates[-1]
    date_range = pd.date_range(start=start, end=end)
    columns = ['Province_State'] + [i for i in range(0, len(date_range))]

    df_confirmed = df_confirmed.drop(
        columns=['Status', 'Date', 'TT']).transpose()
    df_confirmed = df_confirmed.cumsum(axis=1)
    df_confirmed.insert(loc=0, column='Province_State',
                        value=df_confirmed.index)
    df_confirmed.columns = columns


    df_deceased = df_deceased.drop(
        columns=['Status', 'Date', 'TT']).transpose()
    df_deceased = df_deceased.cumsum(axis=1)
    df_deceased.insert(loc=0, column='Province_State', value=df_deceased.index)
    df_deceased.columns = columns


    return [df_confirmed, df_deceased, start, end, dates]


def update():
    url_confirmed = 'https://api.covid19india.org/csv/latest/state_wise_daily.csv'
    filename_confirmed = '../data/raw/IN/time_series_covid19_confirmed_and_deaths.csv'
    print(f'Downloading {url_confirmed}')
    filename_confirmed, headers_confirmed = urllib.request.urlretrieve(
        url_confirmed, filename=filename_confirmed)
    print("download complete!")
    print("download file location: ", filename_confirmed)
    print("Processing")


def prepare():
    filename = '../data/raw/in/time_series_covid19_confirmed_and_deaths.csv'

    [df_confirmed, df_deceased, start, end, dates] = get_IN_DF(filename)
    df_confirmed.to_csv('../data/processed/in/confirmed.csv', index=False)
    with open('../data/processed/in/confirmed.json', 'w', encoding='utf-8') as f:
        json.dump({'start': start, 'end': end, 'dates': dates},
                  f, ensure_ascii=False, indent=4)

    df_deceased.to_csv('../data/processed/in/deaths.csv', index=False)
    with open('../data/processed/in/deaths.json', 'w', encoding='utf-8') as f:
        json.dump({'start': start, 'end': end, 'dates': dates},
                  f, ensure_ascii=False, indent=4)

