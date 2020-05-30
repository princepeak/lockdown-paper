from prepare_data_AUS import update, prepare
from mrsc_score import score_rsc, score_mrsc
import json


lockdown_state = [
    {'name':'Australian Capital Territory','start': '3/13/20', 'end':''},
    {'name':'New South Wales','start': '3/13/20', 'end':''},
    {'name':'Northern Territory', 'start': '3/13/20', 'end':''},
    {'name':'Queensland', 'start': '3/13/20', 'end':''},
    {'name':'South Australia', 'start': '3/13/20', 'end':''},
    {'name':'Tasmania', 'start': '3/13/20', 'end':''},
    {'name':'Victoria', 'start': '3/13/20', 'end':''},
    {'name':'Western Australia', 'start': '3/13/20', 'end':''}  
]

def main():
    update()
    prepare()
    metric = ['deaths', 'confirmed']
    file2 = f'../data/processed/aus/{metric[1]}.csv'
    file1 = f'../data/processed/aus/{metric[0]}.csv'

    metadata = None
    with open(f'../data/processed/aus/{metric[0]}.json') as f:
        metadata = json.load(f)

    for state in lockdown_state:
        name = state['name']
        lockdown_date = state['start']
        lockdown_date_index = metadata['dates'].index(lockdown_date)
        end_date_index = len(metadata['dates'])
        score_mrsc(file1, file2,'Province_State', name, 0, lockdown_date_index, end_date_index, metric[0], 'aus')

if __name__ == "__main__":
    main()  