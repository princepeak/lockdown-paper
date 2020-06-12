import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

def get_location_list(text):
    doc = nlp(text)
    locations = [l.text for l in doc.ents if l.label_ in ['GPE']]
    return locations

def filter_by_location(text, location, sentinel):
    places = set(get_location_list(text))
    if places.intersection(sentinel):
        return True
    else:
        return False

def filter_df(df, field, location, sentinel):
    return df[df[field].apply(filter_by_location, location=location, sentinel=sentinel)]
