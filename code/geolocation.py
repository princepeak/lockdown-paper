from geotext import GeoText

def filter_by_location(text, location):
    places = GeoText(text)
    if location in places.cities:
        return True
    else:
        return False


def filter_df(df,field,location):
    return df[df[field].apply(filter_by_location, location=location)]
