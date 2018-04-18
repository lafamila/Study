import pandas as pd
import re
import nltk

from nltk.stem import WordNetLemmatizer, porter
from nltk.corpus import stopwords


class Wrangler:
    def __init__(self, file_path, output, text_column_name, id_column_name, sep="\t", encoding="utf-8", stop_words=None):
        self.stop_words = set(stopwords.words('english'))
        self.stop_words_extra = set() if stop_words is None else set(stop_words)
        self.lemmatizer = WordNetLemmatizer()
        self.stemmer = porter.PorterStemmer()
        self.file_path = file_path
        self.output = output
        self.seperator = sep
        self.encoding = encoding
        self.column_text = text_column_name
        self.column_id = id_column_name

    def wrangling(self):
        print("Input file '{}' Wrangling started..".format(self.file_path))
        steam = pd.read_csv(self.file_path, sep=self.seperator, encoding=self.encoding)
        steam["text"] = steam[self.column_text].apply(str)
        steam.text = steam.text.apply(self.cleaning)
        steam = steam.rename(index=str, columns={self.column_id: "title"})
        steam["id"] = list(range(len(steam["text"])))
        steam["date"] = steam["posted"]
        steam[["id", "title", "text", "date"]].to_csv(self.output,  index=False, sep="\t", encoding="utf-8")
        print("Output created at '{}'.".format(self.output))
        return self.output

    def cleaning(self, text):

        only_letters = re.sub("[^a-zA-Z]", " ", text)
        tokens = nltk.word_tokenize(only_letters)[:]
        lower_case = [l.lower() for l in tokens]

        # stopwords_1
        filtered = list(filter(lambda l: l not in self.stop_words, lower_case))

        # lemmatize
        lemmas = [self.lemmatizer.lemmatize(word) for word in filtered]

        # stemming
        singles = [self.stemmer.stem(word) for word in lemmas]

        # stopwords_2
        filtered_result = list(filter(lambda l: l not in self.stop_words_extra, singles))
        text = " ".join(filtered_result)
        return text
