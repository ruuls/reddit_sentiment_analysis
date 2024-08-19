
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import pandas as pd

class SentimentAnalyzer:
    def __init__(self, model_name='finiteautomata/bertweet-base-sentiment-analysis'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def score_calculator(self, comment_body):
        try:
            tokens = self.tokenizer(comment_body, return_tensors='pt', truncation=True, padding='max_length', max_length=512)
            
            if tokens['input_ids'].size(1) == 0:
                return np.nan
            
            with torch.no_grad():
                result = self.model(**tokens)
            
            predicted_class = torch.argmax(result.logits).item()
            sentiment_map = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
            return sentiment_map[predicted_class]
        
        except Exception as e:
            print(f"Error processing comment: {e}")
            return np.nan

    def analyze_sentiment(self, df):
        df['Sentiment'] = df['Comment_Body'].apply(lambda x: self.score_calculator(str(x)))
        return df
