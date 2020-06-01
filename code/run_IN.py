from prepare_data_IN import update, prepare
from mrsc_score import score_rsc, score_mrsc
import json


lockdown_state = [
    {'name':'MH','start': '3/22/20', 'end':''},
    {'name':'TN','start': '3/22/20', 'end':''},
    {'name':'WB', 'start': '3/22/20', 'end':''},
    {'name':'DL', 'start': '3/22/20', 'end':''}
]

def main():
    #update()
    prepare()
    metric = ['deaths', 'confirmed']
    file1 = f'../data/processed/in/{metric[0]}.csv'
    file2 = f'../data/processed/in/{metric[1]}.csv'

    metadata = None
    with open(f'../data/processed/in/{metric[0]}.json') as f:
        metadata = json.load(f)

    for state in lockdown_state:
        name = state['name']
        lockdown_date = state['start']
        lockdown_date_index = metadata['dates'].index(lockdown_date)+21
        end_date_index = len(metadata['dates'])
        score_mrsc(file1, file2,'Province_State', name, 0, lockdown_date_index, end_date_index, metric[0], 'in', metadata['dates'], lockdown_date)

if __name__ == "__main__":
    main()