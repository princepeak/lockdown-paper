import pandas as pd
import datetime
from geolocation import filter_df
import gensim
from gensim.models import CoherenceModel
from gensim.corpora.dictionary import Dictionary
from gensim.models.wrappers import DtmModel
import os
import re
import nltk
from pathlib import Path
from gensim.matutils import corpus2csc
from scipy.sparse import save_npz, load_npz
from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np
import spacy
import en_core_web_lg

nlp = en_core_web_lg.load()
nlp.create_pipe('ner')
HOME_DIR = str(Path(__file__).resolve().parents[1])
MODEL_PATH = os.path.join(HOME_DIR, 'code', 'bin', 'dtm')


class Dtm(DtmModel):

    @classmethod
    def load(cls, fname, time_slice_labels):
        model_path = os.path.join(HOME_DIR, 'models', fname, 'dtm.gensim')
        obj = super().load(model_path)
        obj.term_counts = load_npz(
            os.path.join(HOME_DIR, 'models', fname, 'term_counts.npz')
        ).todense()
        obj.normalized_term_counts = \
            (obj.term_counts + 1) / \
            (obj.term_counts.sum(axis=0) + obj.term_counts.shape[0])
        obj.assign_corpus(time_slice_labels)
        obj.topic_assignments = np.apply_along_axis(np.argmax, 1, obj.gamma_)
        return obj

    def assign_term_counts(self, term_counts):
        self.term_counts = term_counts.todense()
        self.normalized_term_counts = \
            (self.term_counts + 1) / \
            (self.term_counts.sum(axis=0) + self.term_counts.shape[0])

    def assign_corpus(self, time_slice_labels):
        """Assign corpus object to the model"""
        self.time_slice_labels = time_slice_labels


    def show_topic(self, topic, time, topn=10, use_relevance_score=True,
                   lambda_=.6, **kwargs):
        """Show top terms from topic

        This override `show_topic` to account for lambda normalizing as
        described in "LDAvis: A method for visualizing and interpreting topics":
        https://nlp.stanford.edu/events/illvi2014/papers/sievert-illvi2014.pdf

        The score returned is computed as

            lambda_ * log(phi_kw) + (1 - lambda_) * log(phi_kw / pw)

        where

            phi_kw : Conditional probability of term `w` in topic `k`.
            pw : Marginal probability of term `w`.

        Parameters
        ----------
        topic : int
        time : int
            Time slice specified as index, e.g. 0, 1, ...
        topn : int
        use_relevance_score : bool
            If True, apply the lambda_ based relevance scoring. Else, fall back
            to the default `show_topic` behavior.
        lambda_ : float
            The lambda constant to use in relevance scoring. Must be in the
            range [0,1].

        Returns
        -------
        list of (float, str)
        """
        if not use_relevance_score:
            return super().show_topic(topic, time=time, topn=topn, **kwargs)
        conditional = super().show_topic(topic, time, topn=None, **kwargs)
        marginal = {
            self.id2word[term_id]: marg[0]
            for term_id, marg in enumerate(
            self.normalized_term_counts[:, time].tolist())}
        weighted = [
            (lambda_ * np.log(cond) + \
             (1 - lambda_) * np.log(cond / marginal[term]), term)
            for cond, term in conditional
        ]
        return sorted(weighted, reverse=True)[:topn]

    def term_distribution(self, term, topic):
        """Extracts the probability over each time slice of a term/topic
        pair."""
        word_index = self.id2word.token2id[term]
        topic_slice = np.exp(self.lambda_[topic])
        topic_slice = topic_slice / topic_slice.sum(axis=0)
        return topic_slice[word_index]

    def term_variance(self, topic):
        """Finds variance of probability over time for terms for a given topic.
        High variance terms are more likely to be interesting than low variance
        terms."""
        p = np.exp(self.lambda_[topic]) / \
            np.exp(self.lambda_[topic]).sum(axis=0)
        variances = np.var(p, axis=1)
        order = np.argsort(variances)[::-1]
        terms = np.array([term for term, _
                          in sorted(self.id2word.token2id.items(),
                                    key=lambda x: x[1])])[order]
        variances = variances[order]
        return list(zip(terms, variances))

    def term_slope(self, topic):
        """Finds slope of probability over time for terms for a given topic.
        This is useful for roughly identifying terms that are rising or
        declining in popularity over time."""
        p = np.exp(self.lambda_[topic]) / \
            np.exp(self.lambda_[topic]).sum(axis=0)
        slopes = np.apply_along_axis(
            lambda y: linregress(x=range(len(y)), y=y).slope, axis=1, arr=p)
        order = np.argsort(slopes)
        terms = np.array([term for term, _
                          in sorted(self.id2word.token2id.items(),
                                    key=lambda x: x[1])])[order]
        slopes = slopes[order]
        return list(zip(terms, slopes))

    def plot_terms(self, topic, terms, title=None, name=None, hide_y=True):
        """Creates a plot of term probabilities over time in a given topic."""
        fig, ax = plt.subplots()
        plt.style.use('fivethirtyeight')
        for term in terms:
            ax.plot(
                self.time_slice_labels, self.term_distribution(term, topic),
                label=term)
        leg = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        if hide_y:
            ax.set_yticklabels([])
        ax.set_ylabel('Probability')
        if title:
            ax.set_title(title)
        if name:
            fig.savefig(
                name, dpi=300, bbox_extra_artists=(leg,), bbox_inches='tight')
        return fig, ax

    def top_term_table(self, topic, slices, topn=10):
        """Returns a dataframe with the top n terms in the topic for each of
        the given time slices."""
        data = {}
        for time_slice in slices:
            time = np.where(self.time_slice_labels == time_slice)[0][0]
            data[time_slice] = [
                term for p, term
                in self.show_topic(topic, time=time, topn=topn)
            ]
        return pd.DataFrame(data)

    def top_label_table(self, topic, slices, topn=10):
        """Returns a dataframe with the top n labels in the topic for each of
        the given time slices."""
        data = {}
        for time_slice in slices:
            data[time_slice] = [
                x[0] for x
                in self.label_topic(topic, time_slice, topn)
            ]
        return pd.DataFrame(data)

    def summary(self, slices, topn=10):
        """Prints a summary of all the topics"""
        for topic in range(self.num_topics):
            print('Topic %d' % topic)
            print(self.top_term_table(topic, slices, topn))
            print()

    def topic_summary(self, topic, n=20):
        """Prints the top N terms by variance, increasing slope, and decreasing
        slope."""
        print('Variance\n---------')
        for row in self.term_variance(topic)[:n]:
            print(row)
        slopes = self.term_slope(topic)
        print('\nSlope (positive)\n----------')
        for row in slopes[-n:][::-1]:
            print(row)
        print('\nSlope (negative)\n----------')
        for row in slopes[:n]:
            print(row)


def bow(text):
    return list(gensim.utils.simple_preprocess(str(text), deacc=True))

def remove_links(text):
    '''Takes a string and removes web links from it'''
    text = re.sub(r'http\S+', '', text) # remove http links
    text = re.sub(r'bit.ly/\S+', '', text) # rempve bitly links
    text = text.strip('[link]') # remove [links]
    return text

def remove_users(text):
    '''Takes a string and removes retweet and @user information'''
    text = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', text) # remove retweet
    text = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', text) # remove tweeted at
    return text

def clean(text):
    """
    Cleans twitter data
    :param data: is a list of string
    :return: cleaned data as list of strings
    """
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.extend(
        ['from', 'subject', 're', 'edu', 'use', 'said', 'covid', 'coronavirus', 'new', 'novel', '19', 'covid19'])

    punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'

    text = remove_users(text)
    text = remove_links(text)
    text = re.sub('\S*@\S*\s?', '', text) # Remove Emails
    text = re.sub('\s+', ' ', text) # Remove new line characters
    text = re.sub("\'", "", text) # Remove distracting single quotes
    text = text.lower()  # lower case
    text = re.sub('[' + punctuation + ']+', ' ', text)  # strip punctuation
    text = ' '.join(re.sub("(@[A-Za-z0–9]+)|(\w+://\S+)", " ", text).split()) #
    text = text.replace("#", "").replace("_", " ").replace("@", "").replace('…', '') #Replace few things like # _ ...
    text_token_list = [word for word in text.split(' ') if word not in stopwords]  # remove stopwords
    text = ' '.join(text_token_list)
    text = re.sub(r'\b[0-9_]+\b\W*', '', text) # Remove just the numbers
    return text

def get_range():
    def get_start_end_dates(year, week):
        d = datetime.date(year, 1, 1)
        if (d.weekday() <= 3):
            d = d - datetime.timedelta(d.weekday())
        else:
            d = d + datetime.timedelta(7 - d.weekday())
        dlt = datetime.timedelta(days=(week - 1) * 7)
        return [d + dlt, d + dlt + datetime.timedelta(days=6)]

    weeks_of_interst = []

    weeks_of_interst.append({'wno': 4, 'sd': datetime.datetime.strptime("2020-01-22", "%Y-%m-%d"),
                             'ed': datetime.datetime.strptime("2020-01-26", "%Y-%m-%d")})

    for i in range(5, 23):
        [s, e] = get_start_end_dates(2020, i)
        r = {}
        r['wno'] = i
        r['sd'] = datetime.datetime(s.year, s.month, s.day)
        r['ed'] = datetime.datetime(e.year, e.month, e.day)
        weeks_of_interst.append(r)

    start = datetime.datetime.strptime("2020-01-22", "%Y-%m-%d")
    end = datetime.datetime.strptime("2020-06-01", "%Y-%m-%d")
    date_of_interest = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days)]
    places_of_interest = ['India', 'New York', 'New Jersey', 'Illinois', 'Italy', 'Spain']
    places_sentinail = {'India':['India', 'Delhi', 'New Delhi', 'Mumbai', 'Bombay', 'Bengaluru', 'Bangalore', 'Calcutta', 'Kolkata', 'Kerala', 'Chennai', 'Hydrabad'],
                        'New York':['New York', 'New York City', 'NY', 'N. Y.'],
                        'New Jersey':['New Jersey', 'NJ'],
                        'Illinois':['Illinois', 'Chicago', 'Aurora', 'Rockford', 'Joliet', 'Naperville', 'Springfield', 'Elgin', 'Peoria'],
                        'Italy':['Italy', 'Rome', 'Venice', 'Milan'],
                        'Spain':['Spain', 'Madrid', 'Barcelona', 'Valencia']}
    topics_of_interest = ['socialdistancing', 'covid19', 'quarantine']

    return [weeks_of_interst, date_of_interest, places_of_interest, topics_of_interest, places_sentinail]

def preprocess():
    [weeks_of_interst,
     date_of_interest,
     places_of_interest,
     topics_of_interest,
     places_sentinail] = get_range()

    for topic in topics_of_interest:
        for week in weeks_of_interst:
            sd = week['sd'].strftime("%Y%m%d")
            ed = week['ed'].strftime("%Y%m%d")
            wn = week['wno']
            # All the dates
            date_of_interest = [week['sd'] + datetime.timedelta(days=x) for x in
                                range(0, (week['ed'] - week['sd']).days + 1)]
            all_filenames = [f'../data/news_intermediate_datafile/{topic}/{day.strftime("%Y%m%d")}-{topic}.csv' for day
                             in date_of_interest]

            combined_df = pd.concat([pd.read_csv(f, engine='python') for f in all_filenames])
            combined_df = combined_df.drop(columns=['Datetime','URL','Title','Content'])
            combined_df['week'] = wn
            #Add NER
            #Add Geolocation
            #Clean and save final text [Date,Week,Text,Geo]
            combined_df.to_csv(f'../data/news_weekly_datafile/{topic}/{wn}.csv', index=False)


def train():
    [weeks_of_interst,
     date_of_interest,
     places_of_interest,
     topics_of_interest,
     places_sentinail] = get_range()

    for place in places_of_interest:
        for topic in topics_of_interest:
            output_dir = os.path.join(HOME_DIR, 'models', place, topic, datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'))
            os.mkdir(output_dir)

            print('Combining all the data.')

            all_filenames = [f"../data/news_weekly_datafile/{topic}/{week['wno']}.csv" for week in weeks_of_interst]
            combined_df = pd.concat([pd.read_csv(f, engine='python') for f in all_filenames])

            combined_df = combined_df.dropna()

            print(f'Filtering by place: {place}')
            sentinel = places_sentinail[place]
            combined_place_df = filter_df(combined_df, 'text', place, sentinel)

            time_slices = combined_place_df.groupby('week').size()
            time_slice_labels = combined_place_df.week.unique()

            print(f'Got timeslices: {time_slices}')

            print(f'Cleaning.')
            combined_place_df['clean'] = combined_place_df['text'].apply(clean)
            combined_place_df['bag_of_words'] = combined_place_df['clean'].apply(bow)

            # Create Dictionary
            print(f'Building Dictionary')
            id2word = Dictionary(combined_place_df.bag_of_words)
            id2word.filter_extremes(no_below=100)

            # Create Corpus
            print(f'Creating Corpus')
            corpus = combined_place_df.bag_of_words.apply(id2word.doc2bow)

            term_counts = corpus2csc(
                combined_place_df.groupby('week')
                    .agg({'bag_of_words': 'sum'})
                    .bag_of_words
                    .apply(id2word.doc2bow))

            save_npz(
                os.path.join(output_dir, 'term_counts.npz'), term_counts)

            print(f'Running DTM.')
            model = Dtm(
                MODEL_PATH, corpus=corpus, id2word=id2word,
                num_topics=10,
                time_slices=time_slices.values, rng_seed=5278)
            model.assign_corpus(time_slice_labels)
            model.assign_term_counts(term_counts)
            model.save(os.path.join(output_dir, 'dtm.gensim'))
            print(model.summary(time_slice_labels))

train()