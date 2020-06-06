import pandas as pd
from lda_model import run_lda

df = pd.read_csv('../data/tweet_processed/tweetsDataset.csv')
df = df.dropna()
run_lda(df, field="Status",name='tweet')