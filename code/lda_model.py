from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from covidwordsegment import load, segment
import nltk
import re

load()

def print_topics(model, vdata, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    Wordcount = vdata.toarray().sum(axis=0)
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i] + ' ' + str(Wordcount[i])
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

def get_topic_as_json(model, vdata, count_vectorizer, n_top_words):
    json_dict = {}
    words = count_vectorizer.get_feature_names()
    Wordcount = vdata.toarray().sum(axis=0)

    topic_term_dists = model.components_ / model.components_.sum(axis=1)[:, None]
    doc_topic_dists = model.transform(vdata)/ model.transform(vdata).sum(axis=1)[:, None]
    doc_length = vdata.sum(axis=1).getA1()

    json_dict['topic'] = {}

    for topic_idx, topic in enumerate(model.components_):
        json_dict['topic'][f'topic{topic_idx}'] = [{'word': words[i], 'count': Wordcount[i]}
                        for i in topic.argsort()[:-n_top_words - 1:-1]]
    json_dict['data'] = {}
    json_dict['data']['topic_term_dists'] = topic_term_dists.tolist()
    json_dict['data']['doc_topic_dists'] = doc_topic_dists.tolist()
    json_dict['data']['doc_length'] = doc_length.tolist()

    return json_dict

def remove_links(tweet):
    '''Takes a string and removes web links from it'''
    tweet = re.sub(r'http\S+', '', tweet) # remove http links
    tweet = re.sub(r'bit.ly/\S+', '', tweet) # rempve bitly links
    tweet = tweet.strip('[link]') # remove [links]
    return tweet

def remove_users(tweet):
    '''Takes a string and removes retweet and @user information'''
    tweet = re.sub('(RT\s@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove retweet
    tweet = re.sub('(@[A-Za-z]+[A-Za-z0-9-_]+)', '', tweet) # remove tweeted at
    return tweet

def clean(tweet, bigrams=True):
    """
    Cleans twitter data
    :param data: is a list of string
    :return: cleaned data as list of strings
    """
    stopwords = nltk.corpus.stopwords.words('english')
    punctuation = '!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~•@'

    tweet = remove_users(tweet)
    tweet = remove_links(tweet)
    tweet = tweet.lower()  # lower case
    tweet = re.sub('[' + punctuation + ']+', ' ', tweet)  # strip punctuation
    tweet = ' '.join(re.sub("(@[A-Za-z0–9]+)|(\w+://\S+)", " ", tweet).split())
    tweet = tweet.replace("#", "").replace("_", " ").replace("@", "").replace('…', '')
    tweet = ' '.join([' '.join(segment(w)) for w in tweet.split()])
    tweet_token_list = [word for word in tweet.split(' ') if word not in stopwords]  # remove stopwords

    if bigrams:
        tweet_token_list = tweet_token_list + [tweet_token_list[i] + '_' + tweet_token_list[i + 1]
                                               for i in range(len(tweet_token_list) - 1)]
    tweet = ' '.join(tweet_token_list)
    return tweet

def vectorize(data):
    """
    Convert a collection of text documents to a matrix of token counts

    This implementation produces a sparse representation of the counts using
    scipy.sparse.csr_matrix.

    :param data: is a list of string
    :return: matrix of token counts
    """
    # Initialise the count vectorizer with the English stop words
    count_vectorizer = CountVectorizer(max_df=0.9, min_df=25, stop_words='english')
    # Fit and transform the processed titles
    count_data = count_vectorizer.fit_transform(data)

    return [count_vectorizer,count_data]

def train(vdata, vectorizer, number_topics = 10, number_words = 10):
    # Create and fit the LDA model
    lda = LDA(n_components=number_topics, n_jobs=-1)
    lda.fit(vdata)
    print_topics(lda, vdata, vectorizer, number_words)
    return get_topic_as_json(lda, vdata, vectorizer, number_words)

def run_lda(df, field):
    print(f'Cleaning..\n')
    df['clean'] = df[field].apply(clean)
    s = df['clean']
    print(f'Vectorization..\n')
    [vectorizer, vdata] = vectorize(s)
    print(f'Running LDA..\n')
    res = train(vdata,vectorizer)
    return res