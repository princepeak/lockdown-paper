import pandas as pd
import datetime

def get_start_end_dates(year, week):
    d = datetime.date(year, 1, 1)
    if (d.weekday() <= 3):
        d = d - datetime.timedelta(d.weekday())
    else:
        d = d + datetime.timedelta(7 - d.weekday())
    dlt = datetime.timedelta(days=(week - 1) * 7)
    return [d + dlt, d + dlt + datetime.timedelta(days=6)]

weeks_of_interst = []

for i in range(5,22):
    [s,e] = get_start_end_dates(2020, i)
    r = {}
    r['wno'] = i
    r['sd'] = s
    r['ed'] = e
    weeks_of_interst.append(r)

places_of_interest = ['New York', 'New Jersey', 'Illinois', 'Italy', 'Spain', 'India']
topics_of_interest = ['covid19', 'quarantine', 'socialdistancing']

def proces_20191101_20200326(topic):
    #load
    path = f'../data/news/{topic}/20191101-20200326-{topic}.csv'
    df = pd.read_csv(path)
    df.columns = ['Datetime', 'URL', 'Title', 'Content']
    df['Date'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M:%S UTC')
    df['text'] = df['Title'] + ' ' + df['Content']
    df = df.dropna()
    df = df.set_index(['Date'])

    start = datetime.datetime.strptime("2020-01-22", "%Y-%m-%d")
    end = datetime.datetime.strptime("2020-03-26", "%Y-%m-%d")
    date_of_interest = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]

    for day in date_of_interest:
        cd = day.strftime("%Y%m%d")
        day_df = df.loc[cd]
        print(f'Using {day_df.shape[0]} articles for {cd}')
        #save a copy
        save_path = f'../data/news_intermediate_datefile/{topic}/{cd}-{topic}.csv'
        day_df.to_csv(save_path)

def process_remaining(topic,cd):
    # load
    path = f'../data/news/{topic}/{cd}-{topic}.csv'
    df = pd.read_csv(path)
    df.columns = ['Datetime', 'URL', 'Title', 'Content']
    df['Date'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M:%S UTC')
    df['text'] = df['Title'] + ' ' + df['Content']
    df = df.dropna()
    df = df.set_index(['Date'])
    day_df = df.loc[cd]
    print(f'Using {day_df.shape[0]} articles for {cd}')
    # save a copy
    save_path = f'../data/news_intermediate_datefile/{topic}/{cd}-{topic}.csv'
    day_df.to_csv(save_path)


for topic in topics_of_interest:
    proces_20191101_20200326(topic)

for topic in topics_of_interest:
    start = datetime.datetime.strptime("2020-03-27", "%Y-%m-%d")
    end = datetime.datetime.strptime("2020-06-02", "%Y-%m-%d")
    date_of_interest = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    for day in date_of_interest:
        cd = day.strftime("%Y%m%d")
        process_remaining(topic,cd)

"""
def process_oneoff(topic,cd):
    # load
    path = f'../data/news/{topic}/20191101-20200326-{topic}.csv'
    df = pd.read_csv(path)
    df.columns = ['Datetime', 'URL', 'Title', 'Content']
    df['Date'] = pd.to_datetime(df['Datetime'], format='%Y-%m-%d %H:%M:%S UTC')
    df['text'] = df['Title'] + ' ' + df['Content']
    df = df.dropna()
    df = df.set_index(['Date'])
    day_df = df.loc[cd]
    print(f'Using {day_df.shape[0]} articles for {cd}')
    # save a copy
    save_path = f'../data/news_intermediate_datefile/{topic}/{cd}-{topic}.csv'
    day_df.to_csv(save_path)
    
for topic in topics_of_interest:
    cd = '20200326'
    process_oneoff(topic,cd)
"""