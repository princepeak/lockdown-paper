import pandas as pd
import urllib.request
import json
import datetime



def get_resultant_DF(df, columns):
    df = df.rename(columns={'TT' : 'Total',
                            'AN' : 'Andaman and Nicobar Islands',
                            'AP' : 'Andhra Pradesh',
                            'AR' : 'Arunachal Pradesh',
                            'AS' : 'Assam',
                            'BR' : 'Bihar',
                            'CH' : 'Chandigarh',
                            'CT' : 'Chhattisgarh',
                            'DN' : 'Dadra and Nagar Haveli',
                            'DD' : 'Daman and Diu',
                            'DL' : 'Delhi',
                            'GA' : 'Goa',
                            'GJ' : 'Gujarat',
                            'HR' : 'Haryana',
                            'HP' : 'Himachal Pradesh',
                            'JK' : 'Jammu and Kashmir',
                            'JH' : 'Jharkhand',
                            'KA' : 'Karnataka',
                            'KL' : 'Kerala',
                            'LA' : 'Ladakh',
                            'LD' : 'Lakshadweep',
                            'MP' : 'Madhya Pradesh',
                            'MH' : 'Maharashtra',
                            'MN' : 'Manipur',
                            'ML' : 'Meghalaya',
                            'MZ' : 'Mizoram',
                            'NL' : 'Nagaland',
                            'OR' : 'Orissa',
                            'PY' : 'Pondicherry',
                            'PB' : 'Punjab',
                            'RJ' : 'Rajasthan',
                            'SK' : 'Sikkim',
                            'TN' : 'Tamil Nadu',
                            'TG' : 'Telangana',
                            'TR' : 'Tripura',
                            'UP' : 'Uttar Pradesh',
                            'UT' : 'Uttarakhand',
                            'WB' : 'West Bengal',
                            'UN' : 'Unassigned'})
    df = df.drop(
        columns=['Status', 'Date']).transpose()
    df = df.cumsum(axis=1)
    df.insert(loc=0, column='Province_State',
                        value=df.index)
    df.columns = columns
    return df

def get_tests_DF(filename):
    pass

def get_IN_DF(filename):

    df = pd.read_csv(filename, delimiter=',')
    df_confirmed = df[df['Status'] == 'Confirmed']
    df_deceased = df[df['Status'] == 'Deceased']

    dates = []
    dfdates = list(dict.fromkeys(list(df['Date'])))

    for d in dfdates:
        dt = datetime.datetime.strptime(d, '%d-%b-%y')
        s = f'{dt.month}/{dt.day}/{dt.year % 100}'
        dates.append(s)

    start = dates[0]
    end = dates[-1]
    date_range = pd.date_range(start=start, end=end)
    columns = ['Province_State'] + [i for i in range(0, len(date_range))]

    df_confirmed = get_resultant_DF(df_confirmed, columns)
    df_deceased = get_resultant_DF(df_deceased, columns)
    return [df_confirmed, df_deceased, start, end, dates]



def update():
    url_confirmed = 'https://api.covid19india.org/csv/latest/state_wise_daily.csv'
    filename_confirmed = '../data/raw/IN/time_series_covid19_confirmed_and_deaths.csv'
    
   
    print(f'Downloading {url_confirmed}')
    filename_confirmed, headers_confirmed = urllib.request.urlretrieve(
        url_confirmed, filename=filename_confirmed)
    print("download complete!")
    print("download file location: ", filename_confirmed)


    url_tests = 'https://api.covid19india.org/csv/latest/statewise_tested_numbers_data.csv'
    filename_tests = '../data/raw/IN/time_series_covid19_tests.csv'

    print(f'Downloading {url_tests}')
    filename_tests, headers_confirmed = urllib.request.urlretrieve(
        url_tests, filename=filename_tests)
    print("download complete!")
    print("download file location: ", filename_tests)

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

if __name__ == "__main__":
    # update()
    filename = '../data/raw/in/time_series_covid19_tests.csv'
    df = pd.read_csv(filename, delimiter=',')
    df = df.drop(columns=df.columns[3:])
    start,end = df['Updated On'].min(), df['Updated On'].max()
    dates = []
    date_range = pd.date_range(start=datetime.datetime.strptime(start,'%d/%m/%Y'), end=datetime.datetime.strptime(end,'%d/%m/%Y'))
    
    for d in date_range:
        dt = d#datetime.datetime.strptime(d, '%d/%m/%Y')
        s = f'{dt.month}/{dt.day}/{dt.year % 100}'
        dates.append(s)
    myDF= pd.DataFrame(columns=['State'] + dates)