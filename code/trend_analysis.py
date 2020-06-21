import matplotlib.pyplot as plt
import datetime
import matplotlib.cm as cm
import matplotlib
from matplotlib.ticker import ScalarFormatter
from matplotlib.pyplot import text
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import warnings
import numpy as np
import pandas as pd

import math
from matplotlib.pyplot import figure
from matplotlib.dates import DayLocator, DateFormatter, date2num
from matplotlib.ticker import FuncFormatter
from matplotlib import rc
import matplotlib.pyplot as plt
import datetime
from matplotlib.pyplot import text

dpi=300
rc('text', usetex=True)
plt.style.use('seaborn-pastel')
pd.plotting.register_matplotlib_converters()
plt.style.use("seaborn-ticks")
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["font.size"] = 11.0
plt.rcParams["figure.figsize"] = (12, 6)

pd.plotting.register_matplotlib_converters()
plt.style.use("seaborn-ticks")
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["font.size"] = 11.0
plt.rcParams["figure.figsize"] = (9, 6)


def trend_analysis(file, country, place, metric, days, events=None):
    dates = [datetime.datetime.strptime(d, '%m/%d/%y') for d in days]
    df = prepare(file, place, dates)
    show_trend(df, country, place, metric, n_changepoints=2,events=events)


def prepare(file, place, dates):
    df = pd.read_csv(file)
    df = df.set_index('Province_State').T
    s = df[place].values
    # Data arrangement
    df = pd.DataFrame({'ds': dates,'y': s})
    return df


def show_trend(df, country, place, metric, n_changepoints=20, events=None):
    """
    Show trend of log10(@variable) using fbprophet package.
    @ncov_df <pd.DataFrame>: the clean data
    @variable <str>: variable name to analyse
        - if Confirmed, use Infected + Recovered + Deaths
    @n_changepoints <int>: max number of change points
    @kwargs: keword arguments of select_area()
    """
    # Log10(x)
    warnings.resetwarnings()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        df["y"] = np.log10(df["y"]).replace([np.inf, -np.inf], 0)
    # fbprophet
    model = Prophet(growth="linear", daily_seasonality=False, n_changepoints=n_changepoints)
    model.fit(df)
    future = model.make_future_dataframe(periods=1)
    forecast = model.predict(future)

    c = model.changepoints
    # Create figure
    fig = model.plot(forecast,figsize=(15, 5))
    _ = add_changepoints_to_plot(fig.gca(), model, forecast)

    ax = plt.gca()
    for i, v in model.changepoints.items():
        text(v, (df["y"].max() - df["y"].min())/2., f'{v.strftime("%Y-%m-%d")}', rotation=90, fontsize=8, color='gray')

    middle = (df["y"].max() - df["y"].min())/2. - (df["y"].max() - df["y"].min())/4.
    if events:
        #plot events
        for evt in events:
            ax.axvline(x=evt['date'], linewidth=1, color='lightgrey')
            text(evt['date'], middle, evt['event'], rotation=90, fontsize=8, color='gray')

    name = f"{place}: "
    plt.title(f"{name} log10({metric}) over time and chainge points")
    plt.ylabel(f"log10(the number of {metric})")
    plt.xlabel("")
    ax.grid(False)

    # Use tight layout
    fig.tight_layout()

    plt.savefig(f'../img/{country}/{place}_{metric}_trend.pdf',dpi=600)
    plt.clf()