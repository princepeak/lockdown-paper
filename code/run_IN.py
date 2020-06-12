from prepare_data_IN import update, prepare
from mrsc_score import score_rsc, score_mrsc
from trend_analysis import trend_analysis
import json
import time
from events import get_events_between
import pandas as pd

"""
Phase 1: 25 March 2020 – 14 April 2020 (21 days)
Phase 2: 15 April 2020 – 3 May 2020 (19 days)
Phase 3: 4 May 2020 – 17 May 2020 (14 days)
Phase 4: 18 May 2020 – 31 May 2020 (14 days)
Phase 5: 1 June 2020 – ongoing (0 days); scheduled to end on 30 June 2020
"""
lockdown_state = [
    {'name':'Maharashtra','start': '4/15/20', 'end':'', 'control':['Delhi',
                                                                   'Gujarat',
                                                                   'Rajasthan',
                                                                   'Uttar Pradesh']},
    {'name':'Delhi','start': '4/15/20', 'end':'', 'control':None}
]

def main():
    update()
    prepare()
    metric = ['deaths', 'confirmed']
    file1 = f'../data/processed/in/{metric[0]}.csv'
    file2 = f'../data/processed/in/{metric[1]}.csv'

    d_cf = f'../data/processed/in/daily_confirmed.csv'
    d_df = f'../data/processed/in/daily_deceased.csv'

    daily_confirmed_df = pd.read_csv(d_cf)
    daily_deceased_df = pd.read_csv(d_df)

    metadata = None
    with open(f'../data/processed/in/{metric[0]}.json') as f:
        metadata = json.load(f)

    for state in lockdown_state:
        name = state['name']
        lockdown_date = state['start']
        lockdown_date_index = metadata['dates'].index(lockdown_date)
        end_date_index = len(metadata['dates'])

        trend_analysis(file1, 'in', name, metric[0], metadata['dates'])
        trend_analysis(file2, 'in', name, metric[1], metadata['dates'])

        confirmed_daily = daily_confirmed_df[daily_confirmed_df['Province_State']==name]
        confirmed_daily = confirmed_daily.drop(columns=['Province_State'])
        confirmed_daily = confirmed_daily.values.tolist()[0]

        deceased_daily = daily_deceased_df[daily_deceased_df['Province_State'] == name]
        deceased_daily = deceased_daily.drop(columns=['Province_State'])
        deceased_daily = deceased_daily.values.tolist()[0]

        score_mrsc(file1, file2,
                   'Province_State',
                   name, 0,
                   lockdown_date_index,
                   end_date_index,
                   metric[0], 'in',
                   metadata['dates'], lockdown_date,
                   control_group=state['control'],
                   events=get_events_between(metadata['dates'][0], metadata['dates'][-1], name),
                   daily_confirmed=confirmed_daily,
                   daily_deaths=deceased_daily)

        score_mrsc(file2, file1,
                   'Province_State',
                   name, 0,
                   lockdown_date_index,
                   end_date_index,
                   metric[1], 'in',
                   metadata['dates'], lockdown_date,
                   control_group=state['control'],
                   events=get_events_between(metadata['dates'][0], metadata['dates'][-1], name),
                   daily_confirmed=confirmed_daily,
                   daily_deaths=deceased_daily)

        time.sleep(5)

if __name__ == "__main__":
    main()