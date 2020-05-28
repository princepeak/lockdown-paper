import pandas as pd
import urllib.request

url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'
filename_confirmed = '../data/raw/us/time_series_covid19_confirmed_US.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv'
filename_deaths = '../data/raw/us/time_series_covid19_deaths_US.csv'


def get_US_Confirmed_DF():
    df = pd.read_csv(filename_confirmed, delimiter=',')
    df = df.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Country_Region','Lat','Long_','Combined_Key'])
    df = df.groupby(['Province_State'],as_index=False).sum()
    return df

def get_US_Death_DF():
    df = pd.read_csv(filename_deaths, delimiter=',')
    df = df.drop(columns=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Country_Region', 'Lat', 'Long_','Combined_Key','Population'])
    df = df.groupby(['Province_State'], as_index=False).sum()
    return df

print (f'Downloading {url_confirmed}')
filename_confirmed, headers_confirmed = urllib.request.urlretrieve(url_confirmed, filename=filename_confirmed)
print ("download complete!")
print ("download file location: ", filename_confirmed)
print ("Processing")
df = get_US_Confirmed_DF()
df.to_csv('../data/processed/us/confirmed.csv', index=False)


print (f'Downloading {url_deaths}')
filename_deaths, headers_deaths = urllib.request.urlretrieve(url_deaths, filename=filename_deaths)
print ("download complete!")
print ("download file location: ", filename_deaths)
print ("Processing")
df = get_US_Death_DF()
df.to_csv('../data/processed/us/deaths.csv', index=False)