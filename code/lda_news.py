import pandas as pd
from lda_model import run_lda
import json
import datetime
from geolocation import filter_df

start = datetime.datetime.strptime("2020-01-22", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-06-01", "%Y-%m-%d")
date_of_interest = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
places_of_interest = ['New York', 'New Jersey', 'Illinois', 'Italy', 'Spain', 'India']
topics_of_interest = ['covid19', 'quarantine', 'socialdistancing']

for place in places_of_interest:
    for topic in topics_of_interest:

        for day in date_of_interest:
            cd = day.strftime("%Y%m%d")
            path = f'../data/news_intermediate_datefile/{topic}/{cd}-{topic}.csv'
            day_df = pd.read_csv(path, engine='python')
            day_df = day_df.dropna()
            day_df = filter_df(day_df, 'text', place)

            if day_df.shape[0] > 100:
                print(f'Using {day_df.shape[0]} articles for {place} on {topic} for {cd}')
                res = run_lda(day_df, 'text')
                res['doc_count'] = day_df.shape[0]
                res['place'] = place
                res['folder'] = topic
                res['date'] = cd
                with open(f'../data/news_processed/{place}/{topic}/{cd}.json', 'w', encoding='utf-8') as f:
                    json.dump(res, f, ensure_ascii=False, indent=4)
            else:
                pass


