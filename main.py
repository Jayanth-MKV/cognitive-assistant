import os
import warnings
from ontology_dc8f06af066e4a7880a5938933236037.simple_text import SimpleText

from openfabric_pysdk.context import OpenfabricExecutionRay
from openfabric_pysdk.loader import ConfigClass
from time import time

import wikipedia
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer



############################################################
# Callback function called on update config
############################################################
def config(configuration: ConfigClass):
    # TODO Add code here
    nltk.download('stopwords')
    nltk.download('punkt')
    # pass


############################################################
# Callback function called on each execution pass
############################################################
def execute(request: SimpleText, ray: OpenfabricExecutionRay) -> SimpleText:
    stemmer = SnowballStemmer("english")
    stop_words = set(stopwords.words('english'))
    output = []
    for text in request.text:
        # TODO Add code here
        response = ''

        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word not in stop_words]
        
        stems = [stemmer.stem(token) for token in tokens]
        
        search_query = ' '.join(stems)
        try:
            wiki_summary = wikipedia.summary(search_query, sentences=2)
            response = wiki_summary
        except wikipedia.exceptions.PageError:
            response = "Sorry, I couldn't find any information to this query."
        except wikipedia.exceptions.DisambiguationError:
            response = "Sorry, there are multiple results to this query. Please be more specific?"
        except Exception:
            response = "Sorry, something went wrong. Please try again later."

        output.append(response)

    return SimpleText(dict(text=output))
