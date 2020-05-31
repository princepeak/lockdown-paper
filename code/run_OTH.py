from prepare_data_OTH import update, prepare
from mrsc_score import score_rsc, score_mrsc
import json


lockdown_state = [
    {'name':'Italy','start': '3/9/20', 'end':''},
    #{'name':'Spain','start': '3/9/20', 'end':''},
    # {'name':' ', 'start': '', 'end':''}
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
        end_date_index = len(metadata['dates'])-20
        score_mrsc(file1, file2,'Province_State', name, 0, lockdown_date_index, end_date_index, metric[0], 'other')

if __name__ == "__main__":
    main()  