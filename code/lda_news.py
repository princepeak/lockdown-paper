import pandas as pd
from lda_model import run_lda
import json
import datetime

start = datetime.datetime.strptime("2020-02-12", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-03-12", "%Y-%m-%d")

date_of_interest = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

df = pd.read_csv('../data/news/OnlineNews-150Snippet.csv')
df['text'] = df['Title'] + df['Context']
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d%H%M%S')
df = df.dropna()
df = df.set_index(['Date'])

result = {}

for day in date_of_interest:
    cd = day.strftime("%Y-%m-%d")
    day_df = df.loc[cd]
    print(f'Using {day_df.shape[0]} articles for {cd}')
    res = run_lda(day_df, field="text", name=f'OnlineNews-150Snippet_{cd}')
    result[cd] = res

with open('../data/news_processed/OnlineNews-150Snippet-LDA_bigram.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)