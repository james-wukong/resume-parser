from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

class TextCleaner:

    def __init__(self, raw_text):
        self.stopwords_set = set(stopwords.words('english') + list(string.punctuation))
        self.lemmatizer = WordNetLemmatizer()
        self.raw_input_text = raw_text

    def clean_text(self) -> str:
        tokens = word_tokenize(self.raw_input_text.lower())
        # remove the stop words and punctuations
        tokens = [token for token in tokens if token not in self.stopwords_set]
        # word lemmatization
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return ' '.join(tokens)