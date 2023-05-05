import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import string
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from scipy import stats
from sklearn.metrics.pairwise import linear_kernel # for cosine similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import ssl

def get_recommendations2(arr,prev_game):
    # preprocess the data
    data = pd.DataFrame(arr, columns=['name', 'summary'])
    data.drop_duplicates('name',keep='first', inplace=True)
    data.drop(index=data[data['summary'].isnull()].index, inplace=True)

    proc_data = nlp_recommend(data, 'summary')

    proc_data.reset_index(drop=True, inplace=True)
    #Define a TF-IDF Vectorizer Object.
    tfidf = TfidfVectorizer()
    #Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform([str(i) for i in proc_data['proc_summary']])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(proc_data.index, index=proc_data['name'])#.drop_duplicates()
    return list(recommend_helper(prev_game, indices, cosine_sim,proc_data))


def recommend_helper(title, indices, cosine_sim,proc_data):
    
    # get index of video game that matches title
    
    idx = indices[title]
    
    # get similarity scores of all video games with that video game
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # sort video games based on similarity scores
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # get scores of 30 most similar video games
    
    sim_scores = sim_scores[1:31]
    
    # get video game indices
    
    game_indices = [i[0] for i in sim_scores]
    
    # return top 10 most similar video games
    
    recs = proc_data['name'].iloc[game_indices]
    
    return recs    
# clean/process corpus

# Function to streamline NLP Process

def nlp_recommend(df, text):
    pstem = PorterStemmer()
    wlem = WordNetLemmatizer()
    no_punc = []
    no_stop = []
    preproc_text = []
    df['dummy'] = df[text].astype(str)
    # Lowercase
    dummy = (post.lower() for post in df['dummy'])
    df['dummy'] = [i for i in dummy]
    # Tokenize
    try:
        word_tokenize(df['dummy'][0])
    except LookupError:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            return []
        else:
            ssl._create_default_https_context = _create_unverified_https_context 
            nltk.download("all")
    token_post = (word_tokenize(post) for post in df['dummy'])
    token_post = [i for i in token_post]   
    # Remove Punctuation
    reg = re.compile('(@[a-z0-9]+)|([^0-9a-z \t])|(\w+:\/\/\S+)')
    # Remove punctuation and stopwords
    for filt in token_post:
        review = []
        for token in filt:
            new_token = reg.sub(u'', token)
            if not new_token == u'':
                review.append(new_token)
        no_punc.append(review)       
    for post in no_punc:
        new_term_vector = []
        for word in post:
            if not word in stopwords.words('english'):
                new_term_vector.append(word)
        no_stop.append(new_term_vector)

    for text in no_stop:
        final_text = []
        for word in text:
            pstem.stem(word)
            final_text.append(wlem.lemmatize(word))

        preproc_text.append(final_text)
        
    # create final data set
    #data = df.copy()

    new_col = pd.Series(preproc_text)
    df['proc_summary'] = new_col
    df.drop('dummy', axis=1, inplace=True)
    return df
