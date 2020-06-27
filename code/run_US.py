from prepare_data_US import update, prepare
from mrsc_score import score_rsc, score_mrsc
import json
from trend_analysis import trend_analysis
import time
from events import get_events_between

# from https://www.businessinsider.com.au/us-map-stay-at-home-orders-lockdowns-2020-3?r=US&IR=T
lockdown_state = [
    {'name':'New Jersey','start': '3/28/20', 'end':'', 'control':['New York',
                                                                       'California',
                                                                       'Illinois',
                                                                       'Massachusetts',
                                                                       'Pennsylvania',
                                                                       'Texas',
                                                                       'Michigan']},
    {'name':'New York','start': '3/22/20', 'end':'5/15/20', 'control':['New Jersey',
                                                                       'California',
                                                                       'Illinois',
                                                                       'Massachusetts',
                                                                       'Pennsylvania',
                                                                       'Texas',
                                                                       'Michigan',
                                                                       'Florida']},
    {'name':'Illinois', 'start': '3/24/20', 'end':'5/1/20', 'control':None}
]


def main():
    update()
    prepare()
    metric = ['deaths', 'confirmed']
    file1 = f'../data/processed/us/{metric[0]}.csv'
    file2 = f'../data/processed/us/{metric[1]}.csv'

    metadata = None
    with open(f'../data/processed/us/{metric[0]}.json') as f:
        metadata = json.load(f)
    for state in lockdown_state:
        name = state['name']
        lockdown_date = state['start']
        lockdown_date_index = metadata['dates'].index(lockdown_date)
        end_date_index = len(metadata['dates'])

        events = get_events_between(metadata['dates'][0], metadata['dates'][-1], name)

        trend_analysis(file1, 'us', name, metric[0], metadata['dates'],  events=events)
        trend_analysis(file2, 'us', name, metric[1], metadata['dates'],  events=events)

        score_mrsc(file1, file2,
                   'Province_State',
                   name, 0,
                   lockdown_date_index,
                   end_date_index,
                   metric[0], 'us',
                   metadata['dates'], lockdown_date,
                   control_group=state['control'],
                   events=events)

        score_mrsc(file2, file1,
                   'Province_State',
                   name, 0,
                   lockdown_date_index,
                   end_date_index,
                   f'{metric[1]} cases', 'us',
                   metadata['dates'], lockdown_date,
                   control_group=state['control'],
                   events=events)
        time.sleep(5)

if __name__ == "__main__":
    main()