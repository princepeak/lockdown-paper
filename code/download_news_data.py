import datetime
from tqdm import tqdm
import requests
import gzip
import shutil

uri_prefix = 'http://data.gdeltproject.org/blog/2020-coronavirus-narrative/live_onlinenews/'

start = datetime.datetime.strptime("20200326", "%Y%m%d")
end = datetime.datetime.strptime("20200603", "%Y%m%d")
date_of_interset = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

topics = ['covid19', 'quarantine', 'socialdistancing']

#topics = ['cases', 'covid19', 'falsehoods', 'masks', 'panic', 'prices', 'quarantine', 'shortages', 'socialdistancing', 'testing', 'ventilators']

extension = '.csv.gz'

for topic in topics:
    for day in date_of_interset:
        day = day.strftime("%Y%m%d")
        url = f'{uri_prefix}{day}-{topic}{extension}'
        response = requests.get(url, stream=True)

        with open(f'../data/news/{topic}/{day}-{topic}{extension}', 'wb') as handle:
            for data in tqdm(response.iter_content()):
                handle.write(data)

        with gzip.open(f'../data/news/{topic}/{day}-{topic}{extension}', 'rb') as f_in:
            with open(f'../data/news/{topic}/{day}-{topic}.csv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
