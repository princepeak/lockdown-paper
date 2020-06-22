from prepare_data_OTH import update, prepare
from mrsc_score import score_rsc, score_mrsc, rankDiagnostic
from trend_analysis import trend_analysis
import json
import time
from events import get_events_between

lockdown_state = [
    {'name':'Italy','start': '3/9/20', 'end':'', 'control':["France",
                                                            "Spain",
                                                            "Germany",
                                                            "Sweden",
                                                            "United Kingdom",
                                                            "Belgium",
                                                            "Netherlands"]},
    {'name':'Spain','start': '3/9/20', 'end':'', 'control':["France",
                                                            "Italy",
                                                            "Brazil"]}
]

def main():
    update()
    prepare()
    metric = ['deaths', 'confirmed']
    file2 = f'../data/processed/other/{metric[1]}.csv'
    file1 = f'../data/processed/other/{metric[0]}.csv'

    metadata = None
    with open(f'../data/processed/other/{metric[0]}.json') as f:
        metadata = json.load(f)

    for state in lockdown_state:
        name = state['name']
        lockdown_date = state['start']
        lockdown_date_index = metadata['dates'].index(lockdown_date)
        end_date_index = len(metadata['dates'])

        events=get_events_between(metadata['dates'][0], metadata['dates'][-1], name)

        trend_analysis(file1, 'other', name, metric[0], metadata['dates'], events=events)
        trend_analysis(file2, 'other', name, f'{metric[1]} cases', metadata['dates'], events=events)

        score_mrsc(file1, file2,
                   'Province_State',
                   name, 0,
                   lockdown_date_index,
                   end_date_index,
                   metric[0], 'other',
                   metadata['dates'], lockdown_date,
                   control_group=state['control'],
                   events=events)

        score_mrsc(file2, file1,
                   'Province_State',
                   name, 0,
                   lockdown_date_index,
                   end_date_index,
                   metric[1], 'other',
                   metadata['dates'], lockdown_date,
                   control_group=state['control'],
                   events=events)
        time.sleep(5)

if __name__ == "__main__":
    main()  