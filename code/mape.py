from mrsc_score import score_mrsc_wp
import numpy as np
import json
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from events import get_events_between
from matplotlib.dates import DayLocator, DateFormatter, date2num

dpi=300
pd.plotting.register_matplotlib_converters()
plt.style.use("seaborn-whitegrid")
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["font.size"] = 11.0
plt.rcParams["figure.figsize"] = (12, 6)

def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100, np.median(np.abs((y_true - y_pred) / y_true)) * 100

MAPE = []
MdAPE = []
ticksToPlot = ['3/1/20', '3/8/20', '3/15/20', '3/22/20', '3/29/20',
               '4/5/20', '4/12/20', '4/19/20', '4/26/20',
               '5/3/20', '5/10/20', '5/17/20', '5/24/20', '5/31/20',
               '6/7/20', '6/14/20', '6/21/20']

metric = ['deaths', 'confirmed']
file1 = f'../data/processed/us/{metric[0]}.csv'
file2 = f'../data/processed/us/{metric[1]}.csv'

metadata = None
with open(f'../data/processed/us/{metric[0]}.json') as f:
    metadata = json.load(f)

states = ['Alabama', 'Alaska', 'American Samoa', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
          'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Grand Princess', 'Guam', 'Hawaii', 'Idaho',
          'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
          'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
          'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Northern Mariana Islands',
          'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico', 'Rhode Island', 'South Carolina',
          'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands', 'Virginia', 'Washington',
          'West Virginia', 'Wisconsin', 'Wyoming']

for intervention in ticksToPlot:
    y_true_score = []
    y_pred_score = []

    for name in states:
        lockdown_date = intervention
        lockdown_date_index = metadata['dates'].index(lockdown_date)
        end_date_index = len(metadata['dates'])

        [deaths_actual,
         deaths_predicted,
         confirmed_actual,
         confirmed_predicted] = score_mrsc_wp(file1, file2,
                                               'Province_State',
                                               name, 0,
                                               lockdown_date_index,
                                               end_date_index,
                                               control_group=None)
        if deaths_actual == 0:
            deaths_actual = 1
        if deaths_predicted == 0:
            deaths_predicted = 1
        y_true_score.append(deaths_actual)
        y_pred_score.append(deaths_predicted)
        print(f'{deaths_actual} \t {deaths_predicted}')

    [mape_s, mdape_s] = mean_absolute_percentage_error(y_true_score, y_pred_score)
    print(f'{intervention} \t {mape_s} \t {mdape_s}')
    MAPE.append(mape_s)
    MdAPE.append(mdape_s)


data_df = pd.DataFrame({'Intervention':ticksToPlot,
                        'MAPE Score' : MAPE,
                        'MdAPE Score' : MdAPE})
data_df['Intervention'] = pd.to_datetime(data_df['Intervention'])
data_df = data_df.set_index('Intervention')
data_df.to_csv('../data/mape.csv')

fig, ax = plt.subplots(figsize=(15, 5))
ax = sns.lineplot(ax=ax, data=data_df, palette="tab10",dashes=False,markers=False)
ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
plt.title(f'APE forecast error for US data')
plt.xlabel('Intervention Dates')
plt.tight_layout()
plt.savefig(f'../img/mape_us.pdf', dpi=600)