import json
import datetime

start = datetime.datetime.strptime("2020-01-22", "%Y-%m-%d")
end = datetime.datetime.strptime("2020-06-01", "%Y-%m-%d")
date_of_interest = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
places_of_interest = ['New York', 'New Jersey', 'Illinois', 'Italy', 'Spain', 'India']
topics_of_interest = ['covid19', 'quarantine', 'socialdistancing']

for place in places_of_interest:
    for topic in topics_of_interest:
        for day in date_of_interest:
            cd = day.strftime("%Y%m%d")

            try:
                with open(f'../data/news_processed/{place}/{topic}/{cd}.json') as f:
                    model_data = json.load(f)

                vocab = model_data['data']['vocab']
                topic_term_dists = model_data['data']['topic_term_dists']
                freq = model_data['data']['freq']
            except:
                pass