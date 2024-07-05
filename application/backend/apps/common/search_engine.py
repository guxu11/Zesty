import nltk
from fuzzywuzzy import process
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re

nltk.download('wordnet')

class SearchEngine:
    def __init__(self):
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def extract_text(self, text):
        # normalize text
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)

        # tokenize text
        words = text.split()

        # apply stemming and lemmatization
        processed_words = []
        for word in words:
            word = self.stemmer.stem(word)  # apply stemming
            word = self.lemmatizer.lemmatize(word)  # apply lemmatization
            processed_words.append(word)

        # rejoin processed words
        processed_text = ' '.join(processed_words)
        
        return processed_text

    # Fuzzy matching, retained for backwards compatibility
    def fuzzy_match(self, query, choices):
        return process.extractOne(query, choices)[0]

