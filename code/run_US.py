from prepare_data_US import update, prepare
from mrsc_score import score_rsc, score_mrsc
import json

# from https://www.businessinsider.com.au/us-map-stay-at-home-orders-lockdowns-2020-3?r=US&IR=T
lockdown_state = [
    {'name':'New Jersey','start': '3/21/20', 'end':''},
    {'name':'New York','start': '3/22/20', 'end':'5/15/20'},
    {'name':'Illinois', 'start': '3/21/20', 'end':'5/1/20'},
    {'name':'Washington', 'start': '3/23/20', 'end':'5/11/20'},
    {'name':'Texas', 'start': '4/1/20', 'end':'4/30/20'},
    {'name': 'New Mexico', 'start': '3/24/20', 'end':'5/16/20'},
    {'name': 'Minnesota', 'start': '3/25/20', 'end':'5/17/20'}
]

def main():
    #update()
    #prepare()
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
        score_mrsc(file1, file2,'Province_State', name, 0, lockdown_date_index, end_date_index, metric[0], 'us', metadata['dates'], lockdown_date)

if __name__ == "__main__":
    main()