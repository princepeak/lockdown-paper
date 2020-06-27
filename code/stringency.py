import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from events import get_events_between

dpi=300
plt.style.use('seaborn-pastel')
pd.plotting.register_matplotlib_converters()
plt.style.use("seaborn-ticks")
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["font.size"] = 11.0
plt.rcParams["figure.figsize"] = (12, 6)

def plot_stringency_index_trend(df, title, ylabel="Stringency Index ", xlabel=None, xlim=(None, None), ylim=(-100, +100),events=None):
    ax = df.plot(figsize=(15, 5))

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if events:
        #plot events
        for evt in events:
            ax.axvline(x=evt['date'], linewidth=1, color='lightgrey')
            text(evt['date'], -75, f"{evt['date']}: {evt['event']}", rotation=90, fontsize=8, color='gray')
    plt.tight_layout()
    plt.savefig(f'../img/stringency_index/{title}.pdf', dpi=600)
    plt.clf()

def main():
    df = pd.read_csv('../data/stringency_index/covid-stringency-index.csv')

    places_of_interest = ['United States',
                          'Italy',
                          'Spain',
                          'India',
                          "France",
                          "Germany",
                          "Sweden",
                          "United Kingdom",
                          "Belgium",
                          "Netherlands",
                          "Brazil",
                          'Philippines']

    for place in places_of_interest:
        df_place = df[df['Entity'] == place]
        sindex = df_place['Government Response Stringency Index ((0 to 100, 100 = strictest))']
        dates = df_place['Date']
        plot_dict = {}
        plot_dict['Government Response Stringency Index ((0 to 100, 100 = strictest))'] = sindex
        plot_dict['Date'] = dates
        plot_df = pd.DataFrame(plot_dict)
        plot_df['Date'] = pd.to_datetime(plot_df['Date'])
        plot_df = plot_df.set_index('Date')

        eplace = place
        if place == 'Germany':
            eplace = 'Italy'
        if place == 'Sweden':
            eplace = 'Italy'

        plot_stringency_index_trend(plot_df, f'Government Response Stringency Index in {place} ((0 to 100, 100 = strictest))',
                            events=get_events_between('1/13/20', '6/19/20', eplace))

if __name__ == "__main__":
    main()