import pandas as pd

metric = ['deaths', 'confirmed']

file1 = f'../data/processed/other/all_deaths.csv'
file2 = f'../data/processed/other/all_confirmed.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

places = df1['Province_State'].values.tolist()

for place in places:
    place_m1 = df1[df1['Province_State']==place]
    place_m1 = place_m1.drop(columns=['Province_State'])
    place_series_m1 = place_m1.values.tolist()[0]
    place_series_m1 = [v for v in place_series_m1 if v > 100]

    place_m2 = df2[df2['Province_State'] == place]
    place_m2 = place_m2.drop(columns=['Province_State'])
    place_series_m2 = place_m2.values.tolist()[0]
    place_series_m2 = [v for v in place_series_m2 if v > 100]
    pass