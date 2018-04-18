import pandas as pd

steam = pd.read_csv("Steam.csv")
list(steam.columns.values)

import re, nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
stop_words.add("facebook")
wordnet_lemmatizer = WordNetLemmatizer()


def normalizer(tweet):
    only_letters = re.sub("[^a-zA-Z]", " ", tweet)
    tokens = nltk.word_tokenize(only_letters)[:]
    lower_case = [l.lower() for l in tokens]
    filtered_result = list(filter(lambda l: l not in stop_words, lower_case))
    lemmas = [wordnet_lemmatizer.lemmatize(t) for t in filtered_result]
    return lemmas


pd.set_option('display.max_colwidth', -1)
steam.comment = steam.comment.apply(str)
steam['normalized_tweet'] = steam.comment.apply(normalizer)
steam[['comment', 'normalized_tweet']].head()

steam_stems = steam.normalized_tweet
from gensim import corpora, models
import gensim

dictionary = corpora.Dictionary(steam_stems)

corpus = [dictionary.doc2bow(steam_stem) for steam_stem in steam_stems]

corpus[0]

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=20)

print(ldamodel.print_topics(num_topics=10, num_words=4))


# 되긴 됨, 엄청느림, 쓸데없는 단어 지워야함...ㅜㅜ, 왜이렇게 느리죠...