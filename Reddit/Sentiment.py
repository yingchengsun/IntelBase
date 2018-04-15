'''
Created on Apr 1, 2018

@author: yingc
'''
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentences = [
                "The plot was good, but the characters are uncompelling and the dialog is not great.", 
                "A really bad, horrible book.",       
                "At least it isn't a horrible book."
            ]

analyzer = SentimentIntensityAnalyzer()



for sentence in sentences:
    print sentence,
    vs = analyzer.polarity_scores(sentence)
    print(str(vs))
    print(str(vs["compound"]))
    
