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
pd.plotting.register_matplotlib_converters()
plt.style.use("seaborn-ticks")
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["font.size"] = 11.0
plt.rcParams["figure.figsize"] = (9, 6)


def trend_analysis(file, country, place, metric, days):
    dates = [datetime.datetime.strptime(d, '%m/%d/%y') for d in days]
    df = prepare(file, place, dates)
    show_trend(df, country, place, metric, n_changepoints=2)


def prepare(file, place, dates):
    df = pd.read_csv(file)
    df = df.set_index('Province_State').T
    s = df[place].values
    # Data arrangement
    df = pd.DataFrame({'ds': dates,'y': s})
    return df


def show_trend(df, country, place, metric, n_changepoints=20):
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
        df["y"] = df["y"] #np.log10(df["y"]).replace([np.inf, -np.inf], 0)
    # fbprophet
    model = Prophet(growth="linear", daily_seasonality=False, n_changepoints=n_changepoints)
    model.fit(df)
    future = model.make_future_dataframe(periods=14)
    forecast = model.predict(future)

    c = model.changepoints
    # Create figure
    fig = model.plot(forecast)
    _ = add_changepoints_to_plot(fig.gca(), model, forecast)

    for i, v in model.changepoints.items():
        text(v, (df["y"].max() - df["y"].min())/2., f'{v.strftime("%Y-%m-%d")}', rotation=90, verticalalignment='center')
    name = f"{place}: "
    plt.title(f"{name} {metric} over time and chainge points")
    plt.ylabel(f"the number of cases")
    plt.xlabel("")


    # Use tight layout
    fig.tight_layout()

    plt.savefig(f'../img/{country}/{place}_{metric}_trend.png')
    plt.clf()