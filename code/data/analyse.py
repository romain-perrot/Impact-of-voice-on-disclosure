########################## import ###################################

from nltk.corpus import stopwords
from transformers import pipeline


######################### functions #################################


"""
brief  : function to count the number of word in an answer
input  : text : text we work on
output : the length of the answer as an int
"""
def count_words(text):
    if len(text)>1:
        words = text.split()
        return len(words)
    else :
        return len(text)


"""
brief  : function to remove the stop words of a text
input  : text : text we work on
output : the text without stop words
"""
def remove_stop_words(text):
    #retireve the stop word dictionnary from nltk library
    stop_words = set(stopwords.words('english'))
    cleaned_words = []
    lines = text.split('\n')
    # remove the stop words
    for line in lines:
        words = line.split()
        cleaned_words.extend([word for word in words if word.lower() not in stop_words])
    return cleaned_words


"""
brief  : analyse the emotion of a text
input  : text : text we work on
output : name of the emotion detected
"""
def analyze_emotion(text):
    # transformer pipeline to use a model
    emotion_classifier = pipeline("sentiment-analysis")
    result = emotion_classifier(text)
    emotion_label = result[0]['label']

    return emotion_label


"""
brief  : analyse the sentiment of a text
input  : text : text we work on
output : name of the emotion detected
"""
def analyze_sentiment(text):
    # transformer pipeline to use a model
    emotion_classifier = pipeline("sentiment-analysis", model="SamLowe/roberta-base-go_emotions")
    result = emotion_classifier(text)
    sentiment_label = result[0]['label']

    return sentiment_label

