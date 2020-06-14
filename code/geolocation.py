import en_core_web_sm
from joblib import Parallel, delayed
nlp = en_core_web_sm.load()

def ner_pipe(doc,sentinel):
    locations = [l.text for l in doc.ents if l.label_ in ['GPE']]
    if any(x in locations for x in sentinel):
        return True
    else:
        return False

def chunker(iterable, total_length, chunksize):
    return (iterable[pos: pos + chunksize] for pos in range(0, total_length, chunksize))

def flatten(list_of_lists):
    "Flatten a list of lists to a combined list"
    return [item for sublist in list_of_lists for item in sublist]

def process_chunk(texts,sentinel):
    preproc_pipe = []
    for doc in nlp.pipe(texts, n_threads=5, batch_size=1000):
        preproc_pipe.append(ner_pipe(doc, sentinel))
    return preproc_pipe

def filter_df(df, field, location, sentinel):
    print(df.shape)
    executor = Parallel(n_jobs=7, verbose=100, prefer="processes")
    do = delayed(process_chunk)
    tasks = (do(chunk,sentinel) for chunk in chunker(df[field].values, len(df), chunksize=5000))
    result = executor(tasks)
    selected = flatten(result)
    return df[selected]
