
"""
Based on #https://www.nbcnews.com/health/health-news/coronavirus-timeline-tracking-critical-moments-covid-19-n1154341

1/23/20 Wuhan placed under quarantine
1/30/20 WHO declares a Public Health Emergency of International Concern
2/11/20 WHO announces name COVID-19
2/19/20 Confirmed cases in Iran
2/29/20 US reports first COVID-19 death
3/11/20 WHO classifies COVID-19 as a pandemic
2/1/20 First reported case in Spain
2/4/20 Diamond Princes cruise ship is quarantined in Japan
2/18/20 Passengers begin to disembark the Diamond Princes
2/20/20 First reported case in Italy
3/8/20 Italy begins Lockdown
3/11/20 US bans travel from most European countries
12/31/19 China, reported a cluster of cases of pneumonia in Wuhan, Hubei Province
1/12/20 China publicly shared the genetic sequence of COVID-19
1/13/20 First recorded case outside of China
3/12/20 Stock markets worldwide suffer greatest single day fall since 1987
1/31/20 US ban entry for most foreign nationals who had traveled to China within the last 14 days.
2/2/20 The first coronavirus death reported outside China
2/7/20 Dr Li Wenliang died in Wuhan
2/24/20 Italy became the worst-hit country in Europe
3/10/20 Lockdown extended to whole Italy
3/13/20 Trump declared a national state of emergency in US
3/15/20 New York school closure
3/18/20 Germany sealed its borders
3/16/20 San Francisco lockdown
3/16/20 France lockdown
3/17/20 EU travel restriction
3/19/20 China reported no new domestic cases for the first time since the start of the epidemic
3/19/20 Australia and New Zealand closes border
3/19/20 Italy records more coronavirus-related deaths than China
3/19/20 California issued a statewide stay-at-home order 
3/21/20 Coronavirus cases in New York State crosses 10,000
3/24/20 India lockdown 1.0
3/21/20 New Jersey lockdown
3/21/20 New Illinois lockdown
3/22/20 New York lockdown
3/24/20 France entered a two-month state of emergency
3/25/20 Prince Charles, 71, tested positive for coronavirus
3/26/20 Major disaster declaration for New Jersey
3/26/20 U.S. coronavirus cases surpassed China
3/27/20 Britain’s Prime Minister Boris Johnson tested positive for coronavirus
3/28/20 South Korea recorded more recoveries than active coronavirus cases
3/28/20 An infant, younger than a year old died in Illinois
3/29/20 The city of Wuhan, China, reopened subways
3/30/20 Moscow announced a lockdown
3/30/20 Italy extends lockdown
4/7/20 New York saw its "largest single-day increase" in deaths
4/9/20 Second coronavirus vaccine trial began in the U.S.
4/9/20 Spain extended state of emergency measures until April 26.
4/11/20 US becomes the worst-hit country in the world
4/13/20 New York outlined first steps towards easing lockdown restrictions
4/14/20 India extended the nationwide lockdown
4/17/20 President Trump encouraged anti-lockdown groups
4/19/20 Europe reached 100,000 coronavirus deaths
4/21/20 Protest in North Carolina and Missouri against stay-at-home orders
4/22/20 Illinois reported a new daily high in coronavirus cases
4/23/20 President Donald Trump suggested exploring disinfectants as a possible treatment for COVID-19 infections
4/25/20 The Indian government allowed a limited reopening 
5/1/20 India extended its nationwide lockdown for another two weeks
5/4/20 Around 4 million Italians returned to work
5/6/20 European Commission forecast suggest 7.5 percent contraction in economy
5/8/20 Cuomo said that the state has 73 cases of children developing symptoms similar to Kawasaki disease
5/12/20 Fauci warned of serious consequences if governors reopen state economies prematurely
5/14/20 Number of unemployment claim in US reaches 36.5 million
5/14/20 MIS-C, has been reported in at least 19 states and Washington, D.C.
5/15/20 In US April retail sales sank by 16.4 percent
5/16/20 Restaurants, pubs and cafes in Australia reopens
5/18/20 Restaurants and shops reopened in Italy
5/20/20 In US, all 50 states had begun lifting some lockdown measures
5/22/20 The Justice Department backed a lawsuit challenging the stay at home restrictions in Illinois
5/22/20 Hertz filed for bankruptcy protection
5/26/20 Lockdown eases in many states of US
5/27/20 The United States surpassed 100,000 coronavirus deaths.
5/31/20 Thousands gathered in cities across US to protest the in-custody death of George Floyd

Relevance for
['New York', 'New Jersey', 'Illinois', 'Italy', 'Spain', 'Maharashtra', 'Delhi']

Use as:
evs = get_events_between('1/1/20','5/31/20','New York')
for e in evs:
    print(e)
"""
global_events = [
    {'date': '1/23/20', 'event': 'Wuhan placed under quarantine', 'relevency': []},
    {'date': '1/30/20', 'event': 'WHO declares a Public Health Emergency of International Concern', 'relevency': []},
    {'date': '2/11/20', 'event': 'WHO announces name COVID-19',
     'relevency': ['New York', 'New Jersey', 'Illinois', 'Italy', 'Spain', 'Maharashtra']},
    {'date': '2/19/20', 'event': 'Confirmed cases in Iran', 'relevency': []},
    {'date': '2/29/20', 'event': 'US reports first COVID-19 death',
     'relevency': ['New York', 'New Jersey', 'Illinois']},
    {'date': '2/1/20', 'event': 'First reported case in Spain', 'relevency': ['Spain']},
    {'date': '2/4/20', 'event': 'Diamond Princes cruise ship is quarantined in Japan', 'relevency': []},
    {'date': '2/18/20', 'event': 'Passengers begin to disembark the Diamond Princes', 'relevency': []},
    {'date': '2/20/20', 'event': 'First reported case in Italy', 'relevency': ['Italy']},
    {'date': '3/11/20', 'event': 'WHO classifies COVID-19 as a pandemic',
     'relevency': ['New York', 'New Jersey', 'Illinois', 'Italy', 'Spain', 'Maharashtra']},
    {'date': '3/11/20', 'event': 'US bans travel from most European countries', 'relevency': []},
    {'date': '3/8/20', 'event': 'Italy begins Lockdown', 'relevency': ['Italy']},
    {'date': '12/31/19', 'event': 'China, reported a cluster of cases of pneumonia in Wuhan, Hubei Province',
     'relevency': []},
    {'date': '1/12/20', 'event': 'China publicly shared the genetic sequence of COVID-19', 'relevency': []},
    {'date': '1/13/20', 'event': 'First recorded case outside of China', 'relevency': []},
    {'date': '3/12/20', 'event': 'Stock markets worldwide suffer greatest single day fall since 1987', 'relevency': []},
    {'date': '1/31/20',
     'event': 'US ban entry for most foreign nationals who had traveled to China within the last 14 days',
     'relevency': []},
    {'date': '2/2/20', 'event': 'The first coronavirus death reported outside China', 'relevency': []},
    {'date': '2/7/20', 'event': 'Dr Li Wenliang died in Wuhan', 'relevency': []},
    {'date': '2/24/20', 'event': 'Italy became the worst-hit country in Europe', 'relevency': ['Italy']},
    {'date': '3/10/20', 'event': 'Lockdown extended to whole Italy', 'relevency': ['Italy']},
    {'date': '3/13/20', 'event': 'Trump declared a national \n state of emergency in US',
     'relevency': ['New Jersey', 'Illinois']},
    {'date': '3/15/20', 'event': 'New York school closure', 'relevency': ['New York']},
    {'date': '3/18/20', 'event': 'Germany sealed its borders', 'relevency': []},
    {'date': '3/16/20', 'event': 'San Francisco lockdown', 'relevency': []},
    {'date': '3/16/20', 'event': 'France lockdown', 'relevency': []},
    {'date': '3/17/20', 'event': 'EU travel restriction', 'relevency': ['Italy']},
    {'date': '3/19/20',
     'event': 'China reported no new domestic cases for the first time since the start of the epidemic',
     'relevency': []},
    {'date': '3/19/20', 'event': 'Australia and New Zealand closes border', 'relevency': []},
    {'date': '3/19/20', 'event': 'Italy records more coronavirus-related deaths than China', 'relevency': ['Italy']},
    {'date': '3/19/20', 'event': 'California issued a statewide stay-at-home order', 'relevency': []},
    {'date': '3/21/20', 'event': 'Coronavirus cases in New York State\n crosses 10,000', 'relevency': []},
    {'date': '3/24/20', 'event': 'A complete 21-day national lockdown', 'relevency': ['Maharashtra']},
    {'date': '3/21/20', 'event': 'New Jersey lockdown', 'relevency': ['New Jersey']},
    {'date': '3/21/20', 'event': 'Illinois lockdown', 'relevency': ['Illinois']},
    {'date': '3/22/20', 'event': 'New York lockdown', 'relevency': ['New York']},
    {'date': '3/24/20', 'event': 'France entered a two-month state of emergency', 'relevency': []},
    {'date': '3/25/20', 'event': 'Prince Charles, 71, tested positive for coronavirus', 'relevency': []},
    {'date': '3/26/20', 'event': 'Major disaster declaration for New Jersey', 'relevency': ['New Jersey']},
    {'date': '3/26/20', 'event': 'U.S. coronavirus cases surpassed China', 'relevency': []},
    {'date': '3/27/20', 'event': 'Britain’s Prime Minister Boris Johnson tested positive for coronavirus',
     'relevency': []},
    {'date': '3/28/20', 'event': 'South Korea recorded more recoveries than active coronavirus cases', 'relevency': []},
    {'date': '3/28/20', 'event': 'An infant, younger \n than a year old \n died in Illinois',
     'relevency': ['Illinois']},
    {'date': '3/29/20', 'event': 'The city of Wuhan, China, reopened subways', 'relevency': []},
    {'date': '3/30/20', 'event': 'Moscow announced a lockdown', 'relevency': []},
    {'date': '3/30/20', 'event': 'Italy extends lockdown', 'relevency': ['Italy']},
    {'date': '4/7/20', 'event': 'New York saw its largest single-day increase in deaths', 'relevency': ['New York']},
    {'date': '4/9/20', 'event': 'Second coronavirus vaccine trial began in the U.S.', 'relevency': []},
    {'date': '4/9/20', 'event': 'Spain extended state of emergency measures until April 26.', 'relevency': ['Spain']},
    {'date': '4/11/20', 'event': 'US becomes the worst-hit\n country in the world',
     'relevency': ['New Jersey', 'Illinois']},
    {'date': '4/13/20', 'event': 'New York outlined first steps \ntowards easing lockdown restrictions',
     'relevency': ['New York']},
    {'date': '4/14/20', 'event': 'India extended the nationwide lockdown', 'relevency': ['Maharashtra']},
    {'date': '4/17/20', 'event': 'President Trump encouraged anti-lockdown groups', 'relevency': []},
    {'date': '4/19/20', 'event': 'Europe reached 100,000 coronavirus deaths', 'relevency': ['Italy', 'Spain']},
    {'date': '4/21/20', 'event': 'Protest in North Carolina and Missouri against stay-at-home orders', 'relevency': []},
    {'date': '4/22/20', 'event': 'Illinois reported a new daily high\n in coronavirus cases',
     'relevency': ['Illinois']},
    {'date': '4/23/20',
     'event': 'President Donald Trump suggested exploring disinfectants as a possible treatment for COVID-19 infections',
     'relevency': []},
    {'date': '4/25/20', 'event': 'The Indian government allowed a limited reopening', 'relevency': ['Maharashtra']},
    {'date': '5/1/20', 'event': 'India extended its nationwide lockdown for another two weeks',
     'relevency': ['Maharashtra']},
    {'date': '5/4/20', 'event': 'Around 4 million Italians returned to work', 'relevency': ['Italy']},
    {'date': '5/6/20', 'event': 'European Commission forecast suggest 7.5 percent contraction in economy',
     'relevency': []},
    {'date': '5/8/20',
     'event': 'Cuomo said that the state has 73 cases of children developing symptoms similar to Kawasaki disease',
     'relevency': []},
    {'date': '5/12/20',
     'event': 'Fauci warned of serious consequences \nif governors reopen state economies \nprematurely',
     'relevency': ['New York', 'New Jersey', 'Illinois']},
    {'date': '5/14/20', 'event': 'Number of unemployment claim in US reaches 36.5 million', 'relevency': []},
    {'date': '5/14/20', 'event': 'MIS-C, has been reported in at least 19 states and Washington, D.C.',
     'relevency': []},
    {'date': '5/15/20', 'event': 'In US April retail sales sank by 16.4 percent', 'relevency': []},
    {'date': '5/16/20', 'event': 'Restaurants, pubs and cafes in Australia reopens', 'relevency': []},
    {'date': '5/18/20', 'event': 'Restaurants and shops reopened in Italy', 'relevency': ["Italy"]},
    {'date': '5/20/20', 'event': 'In US, all 50 states had begun lifting some lockdown measures', 'relevency': []},
    {'date': '5/22/20',
     'event': 'The Justice Department backed \na lawsuit challenging the \nstay at home restrictions in Illinois',
     'relevency': ['Illinois']},
    {'date': '5/22/20', 'event': 'Hertz filed for bankruptcy protection', 'relevency': []},
    {'date': '5/26/20', 'event': 'Lockdown eases in many states of US', 'relevency': []},
    {'date': '5/27/20', 'event': 'The United States surpassed 100,000 coronavirus deaths', 'relevency': []},
    {'date': '5/31/20', 'event': 'Thousands gathered across US\n to protest the death \nof George Floyd',
     'relevency': ['New York', 'New Jersey', 'Illinois']},
    {'date': '2/21/20', 'event': '14 confirmed cases in Lombardy', 'relevency': ["Italy"]},
    {'date': '4/6/20', 'event': 'Lowest number of new daily cases in three weeks', 'relevency': ["Italy"]},
    {'date': '2/25/20', 'event': 'Four new cases related to the Italian cluster', 'relevency': ["Spain"]},
    {'date': '3/20/20', 'event': 'Spain exceeds 1,000 deaths', 'relevency': ["Spain"]},
    {'date': '4/26/20', 'event': 'Lowest number of deaths recorded \nsince more than a month', 'relevency': ["Spain"]},
    {'date': '3/15/20', 'event': 'National lockdown due to the \nState of Alarm becomes effective',
     'relevency': ["Spain"]},
    {'date': '5/11/20', 'event': 'Phase 1 De-escalation start', 'relevency': ["Spain"]},
    {'date': '4/6/20', 'event': 'The doubling rate had slowed \nto six days from three days',
     'relevency': ['Maharashtra']},
    {'date': '5/30/20', 'event': 'Lockdown extended till 30 June in containment zones', 'relevency': ['Maharashtra']}
]

def get_event(date, place):
    for event in global_events:
        if event['date'] == date and place in event['relevency']:
            return event
    return None

def get_events_between(from_date, to_date, place):
    events = []
    import datetime

    start = datetime.datetime.strptime(from_date, '%m/%d/%y')
    end = datetime.datetime.strptime(to_date, '%m/%d/%y')

    date_of_interest = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    for dt in date_of_interest:
        cd = f'{dt.month}/{dt.day}/{dt.year % 100}'
        res = get_event(cd, place)
        if res:
            events.append(res)
    return events

