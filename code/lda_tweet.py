import pandas as pd
from lda_model import run_lda

df = pd.read_csv('../data/tweet_processed/april28-june3.csv')
df = df.dropna()
run_lda(df, field="status")