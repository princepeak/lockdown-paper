from prepare_data_US import update, prepare
from mrsc_score import score_rsc, score_mrsc


def main():
    #update()
    prepare()
    metric = ['deaths', 'confirmed']
    file1 = f'../data/processed/us/{metric[0]}.csv'
    file2 = f'../data/processed/us/{metric[1]}.csv'

    score_mrsc(file1, file2,'Province_State', 'Washington', 0, 110, 127, metric[0], 'us')

if __name__ == "__main__":
    main()