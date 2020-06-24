import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
from matplotlib.pyplot import text
from events import get_events_between
from matplotlib.dates import DayLocator, DateFormatter, date2num

dpi=300
#plt.style.use('fivethirtyeight')
pd.plotting.register_matplotlib_converters()
plt.style.use("seaborn-whitegrid")
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["font.size"] = 11.0
plt.rcParams["figure.figsize"] = (12, 6)

def plot_mobility_trend(df, title, ylabel="% Chnage from baseline", xlabel=None, xlim=(None, None), ylim=(-100, +100),events=None):
    fig, ax = plt.subplots(figsize=(15, 5))
    ax = sns.lineplot(ax=ax, data=df,palette="tab10",dashes=False,markers=False)

    ax.set_title(f'Government Response Stringency Index and {title}')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
    if events:
        #plot events
        for evt in events:
            ax.axvline(x=evt['date'], linewidth=1, color='lightgrey')
            text(evt['date'], -75, f"{evt['date']}: {evt['event']}", rotation=90, fontsize=8, color='gray')
    plt.tight_layout()
    plt.savefig(f'../img/mobility/{title}.pdf', dpi=600)
    plt.clf()


def main():
    df = pd.read_csv('../data/mobility/applemobilitytrends-2020-06-21.csv')
    df_walking = df[df['transportation_type']=='walking']
    df_driving = df[df['transportation_type'] == 'driving']
    df_transit = df[df['transportation_type'] == 'transit']

    df_fb_mobility = pd.read_csv('../data/fb_movement/movement-range-2020-06-20.txt', delimiter='\t')

    df_stringency = pd.read_csv('../data/stringency_index/covid-stringency-index.csv')

    df_google_mobility = pd.read_csv('../data/google_mobility/Global_Mobility_Report.csv')


    df_walking = df_walking.drop(
        columns=['transportation_type', 'geo_type', 'alternative_name', 'sub-region', 'country'])
    df_driving = df_driving.drop(
        columns=['transportation_type', 'geo_type', 'alternative_name', 'sub-region', 'country'])
    df_transit = df_transit.drop(
        columns=['transportation_type', 'geo_type', 'alternative_name', 'sub-region', 'country'])

    places_of_interest = ['Italy',
                          'Spain',
                          "France",
                          "Germany",
                          "Sweden",
                          "United Kingdom",
                          "Belgium",
                          "Netherlands"]
    places_iso = ['ITA', 'ESP', 'FRA', 'DEU', 'SWE', 'GBR', 'BEL', 'NLD']

    for place, iso in zip(places_of_interest, places_iso):
        #Apple
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

        #Facebook
        df_fb_mobility_place = df_fb_mobility[df_fb_mobility['country']==iso]
        df_fb_mobility_place['ds'] = pd.to_datetime(df_fb_mobility_place['ds'])
        df_fb_mobility_place = df_fb_mobility_place.drop(columns=['polygon_source',
                                                                  'polygon_id',
                                                                  'polygon_name',
                                                                  'baseline_name',
                                                                  'baseline_type'])

        df_fb_mobility_place_no_move = df_fb_mobility_place.groupby('ds').agg(
            {'all_day_ratio_single_tile_users': 'mean'})
        df_fb_mobility_place_visited = df_fb_mobility_place.groupby('ds').agg(
            {'all_day_bing_tiles_visited_relative_change': 'mean'})

        df_fb_mobility_place_no_move.columns = ['Staying put']
        df_fb_mobility_place_visited.columns = ['Relative change in movement']

        df_fb_mobility_place_no_move['Staying put'] = df_fb_mobility_place_no_move['Staying put'].apply(
            lambda x: x * 100.0)
        df_fb_mobility_place_visited['Relative change in movement'] = df_fb_mobility_place_visited['Relative change in movement'].apply(
            lambda x: x * 100.0)

        #Oxford
        df_stringency_place = df_stringency[df_stringency['Entity']==place]
        df_stringency_place['Date'] = pd.to_datetime(df_stringency_place['Date'])
        df_stringency_place = df_stringency_place.set_index('Date')
        df_stringency_place = df_stringency_place.drop(columns=['Entity','Code'])


        #Google
        df_google_mobility_place = df_google_mobility[(df_google_mobility['country_region']==place) & (df_google_mobility['sub_region_1'].isnull())]
        df_google_mobility_place = df_google_mobility_place.drop(columns=['country_region_code',
                                                                          'country_region',
                                                                          'sub_region_1',
                                                                          'sub_region_2',
                                                                          'iso_3166_2_code',
                                                                          'census_fips_code'])
        df_google_mobility_place.columns = ['date','Retail & Recreation','Grocery & pharmacy', 'Parks', 'Transit Stations', 'Workplaces', 'Residential']
        df_google_mobility_place['date'] = pd.to_datetime(df_google_mobility_place['date'])
        df_google_mobility_place = df_google_mobility_place.set_index('date')

        plot_df = pd.DataFrame(plot_dict)
        plot_df['Dates'] = pd.to_datetime(plot_df['Dates'])
        plot_df = plot_df.set_index('Dates')

        plot_df = pd.merge(plot_df, df_fb_mobility_place_no_move, how='inner', left_index=True, right_index=True)
        plot_df = pd.merge(plot_df, df_fb_mobility_place_visited, how='inner', left_index=True, right_index=True)
        plot_df = pd.merge(plot_df, df_stringency_place, how='inner', left_index=True, right_index=True)
        #plot_df = pd.merge(plot_df, df_google_mobility_place, how='inner', left_index=True, right_index=True)

        plot_df = plot_df.fillna(method='ffill')
        eplace = place
        if place == 'New York City':
            eplace = 'New York'
        if place == 'Mumbai':
            eplace = 'Maharashtra'

        plot_mobility_trend(plot_df, f'Mobility Trends in {place}',events=None)

if __name__ == "__main__":
    main()