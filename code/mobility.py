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

def plot_mobility_trend(df, title, ylabel="% Chnage from baseline", xlabel=None, xlim=(None, None), ylim=(-100, +100),events=None):
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
    plt.savefig(f'../img/mobility/{title}.pdf', dpi=600)
    plt.clf()


def main():
    df = pd.read_csv('../data/mobility/applemobilitytrends-2020-06-19.csv')
    df_walking = df[df['transportation_type']=='walking']
    df_driving = df[df['transportation_type'] == 'driving']
    df_transit = df[df['transportation_type'] == 'transit']

    df_walking = df_walking.drop(
        columns=['transportation_type', 'geo_type', 'alternative_name', 'sub-region', 'country'])
    df_driving = df_driving.drop(
        columns=['transportation_type', 'geo_type', 'alternative_name', 'sub-region', 'country'])
    df_transit = df_transit.drop(
        columns=['transportation_type', 'geo_type', 'alternative_name', 'sub-region', 'country'])

    places_of_interest = ['New York City',
                          'New Jersey',
                          'Illinois',
                          'Italy',
                          'Spain',
                          'Mumbai',
                          "France",
                          "Germany",
                          "Sweden",
                          "United Kingdom",
                          "Belgium",
                          "Netherlands",
                          "Brazil"]

    for place in places_of_interest:
        df_walking_place = df_walking[df_walking['region']==place]
        df_driving_place = df_driving[df_driving['region']==place]
        df_transit_place = df_transit[df_transit['region']==place]

        plot_dict = {}

        if not df_walking_place.empty:
            df_walking_place = df_walking_place.drop(columns=['region'])
            plot_dict['Walking'] = [a-100 for a in df_walking_place.values.tolist()[0]]
            plot_dict['Dates'] = df_walking_place.columns.tolist()

        if not df_driving_place.empty:
            df_driving_place = df_driving_place.drop(columns=['region'])
            plot_dict['Driving'] = [a-100 for a in df_driving_place.values.tolist()[0]]
            plot_dict['Dates'] = df_driving_place.columns.tolist()

        if not df_transit_place.empty:
            df_transit_place = df_transit_place.drop(columns=['region'])
            plot_dict['Public Transport'] = [a-100 for a in df_transit_place.values.tolist()[0]]
            plot_dict['Dates'] = df_transit_place.columns.tolist()

        plot_df = pd.DataFrame(plot_dict)
        plot_df['Dates'] = pd.to_datetime(plot_df['Dates'])
        plot_df = plot_df.set_index('Dates')
        plot_df = plot_df.fillna(method='ffill')
        eplace = place
        if place == 'New York City':
            eplace = 'New York'
        if place == 'Mumbai':
            eplace = 'Maharashtra'
        plot_mobility_trend(plot_df, f'Mobility Trends in {place}',
                            events=get_events_between('1/13/20', '6/6/20', eplace))

if __name__ == "__main__":
    main()