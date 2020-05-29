from prepare_data_IN import update, prepare
from mrsc_score import score_rsc, score_mrsc


def main():
    #update()
    prepare()
    metric = ['deaths', 'confirmed']
    file1 = f'../data/processed/in/{metric[0]}.csv'
    file2 = f'../data/processed/in/{metric[1]}.csv'

    # Missing line of Score msrc -- I didn't totally look into that function yet

if __name__ == "__main__":
    main()