from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np
import json
from gensim.models.wrappers import DtmModel
from gensim.models import CoherenceModel
import pandas as pd
import os
from scipy.sparse import save_npz, load_npz
from pathlib import Path
from matplotlib.pyplot import figure
from matplotlib.dates import DayLocator, DateFormatter, date2num
from matplotlib.ticker import FuncFormatter
from matplotlib import rc
import matplotlib.pyplot as plt
import datetime
from matplotlib.pyplot import text
from scipy.interpolate import make_interp_spline, BSpline
from events import get_events_by_week_no

dpi=300
rc('text', usetex=True)
plt.style.use('seaborn-bright')
pd.plotting.register_matplotlib_converters()
plt.style.use("seaborn-ticks")
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["font.size"] = 11.0
plt.rcParams["figure.figsize"] = (12, 6)

HOME_DIR = str(Path(__file__).resolve().parents[1])
MODEL_PATH = os.path.join(HOME_DIR, 'bin', 'dtm-darwin64')

class Dtm(DtmModel):

    @classmethod
    def load(cls, fname):
        model_path = os.path.join(HOME_DIR, 'models', fname, 'dtm.gensim')
        obj = super().load(model_path)
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

    def plot_terms(self, topic, terms, topic_area=None, place=None, save=None):
        """Creates a plot of term probabilities over time in a given topic."""
        event_data = get_events_by_week_no(self.time_slice_labels.tolist(), place)

        fig, ax = plt.subplots(figsize=(15, 5))
        xnew = np.linspace(self.time_slice_labels.min(), self.time_slice_labels.max(), 300)

        miny = 0
        maxy = 0
        for term in terms:
            td = self.term_distribution(term, topic)
            spl = make_interp_spline(self.time_slice_labels, td, k=3)  # type: BSpline
            ysmooth = spl(xnew)

            if miny > min(td):
                miny = min(td)

            if maxy < max(td):
                maxy = max(td)

            ax.plot(
                xnew, ysmooth, linewidth=2, alpha=0.7,
                label=term)

        middle  = (maxy-miny) / 2. - (maxy - miny) / 4.

        if len(event_data)>0:
            # plot events
            for weekly_evets in event_data:
                wno = weekly_evets['wno']
                events = weekly_evets['events']
                if len(events)>0:
                    ax.axvline(x=wno, linewidth=1, color='lightgrey')
                    text(wno, middle, f"{events[0]['date']}: {events[0]['event']}", rotation=90, fontsize=8, color='gray')
        # Labels
        ax.set_xlabel('Week no.')
        ax.set_ylabel('Probability')
        ax.set_title(f'Term probabilities over time in topic {topic} for {topic_area} in {place}')
        ax.legend(loc='best', framealpha=0.2)
        plt.xticks(self.time_slice_labels.tolist())
        plt.tight_layout()

        if save:
            fig.savefig(os.path.join(HOME_DIR, 'img', 'dtm', place, topic_area, f'Topic-{topic}_{place}_{topic_area}.pdf'), dpi=600)
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