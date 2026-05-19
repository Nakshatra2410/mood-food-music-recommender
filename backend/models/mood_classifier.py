import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizer, BertModel
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import joblib
import pandas as pd
import os

class MoodClassifier:
    def __init__(self, use_bert=True):
        self.use_bert = use_bert
        self.emotions = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']
        
        if use_bert:
            print("Loading BERT model for emotion detection...")
            try:
                self.model_name = "bhadresh-savani/bert-base-uncased-emotion"
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
                self.model.eval()
                print("✅ BERT model loaded successfully")
            except:
                print("⚠️ BERT model download failed, falling back to ML model")
                self.use_bert = False
                self._load_ml_model()
        else:
            self._load_ml_model()
        
        # Mood responses and emojis
        self.mood_responses = {
            'joy': "🎉 I sense happiness! Let's celebrate with something special!",
            'sadness': "💙 I understand you're feeling down. Here's some comfort food to lift your spirits.",
            'love': "❤️ Feeling the love! Here are some romantic recommendations.",
            'anger': "🔥 Let's cool down with some satisfying choices!",
            'fear': "🫂 Feeling anxious? Let's find something comforting.",
            'surprise': "✨ Surprised? Let's go with the flow!"
        }
        
        self.mood_emojis = {
            'joy': '😊', 'sadness': '😢', 'love': '❤️', 
            'anger': '😠', 'fear': '😨', 'surprise': '😲'
        }
    
    def _load_ml_model(self):
        """Load pre-trained ML model or train new one"""
        self.vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
        self.classifier = LogisticRegression(max_iter=1000, multi_class='multinomial', C=1.0)
        print("✅ ML model ready for training")
    
    def train_ml_model(self, texts, labels):
        """Train the ML model on dataset"""
        print(f"Training ML model on {len(texts)} samples...")
        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, labels)
        print("✅ ML model trained successfully")
        return self
    
    def predict_mood_bert(self, text):
        """Predict mood using BERT"""
        inputs = self.tokenizer(text, return_tensors="pt", 
                               truncation=True, padding=True, max_length=128)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        mood_idx = torch.argmax(predictions).item()
        confidence = predictions[0][mood_idx].item()
        
        return {
            'mood': self.emotions[mood_idx],
            'confidence': confidence,
            'all_scores': {self.emotions[i]: predictions[0][i].item() 
                          for i in range(len(self.emotions))}
        }
    
    def predict_mood_ml(self, text):
        """Predict mood using ML model"""
        X = self.vectorizer.transform([text])
        proba = self.classifier.predict_proba(X)[0]
        mood_idx = np.argmax(proba)
        confidence = proba[mood_idx]
        
        return {
            'mood': self.emotions[mood_idx],
            'confidence': confidence,
            'all_scores': {self.emotions[i]: proba[i] for i in range(len(self.emotions))}
        }
    
    def predict_mood(self, text):
        """Main prediction method"""
        if self.use_bert:
            result = self.predict_mood_bert(text)
        else:
            result = self.predict_mood_ml(text)
        
        result['response'] = self.mood_responses.get(result['mood'], 
                                                     "Here are some recommendations for you!")
        result['emoji'] = self.mood_emojis.get(result['mood'], '😊')
        
        return result
    
    def save_model(self, path='models/'):
        """Save ML model to disk"""
        if not self.use_bert:
            joblib.dump(self.vectorizer, f'{path}vectorizer.pkl')
            joblib.dump(self.classifier, f'{path}mood_classifier.pkl')
            print(f"✅ Models saved to {path}")
    
    def load_model(self, path='models/'):
        """Load ML model from disk"""
        if os.path.exists(f'{path}vectorizer.pkl'):
            self.vectorizer = joblib.load(f'{path}vectorizer.pkl')
            self.classifier = joblib.load(f'{path}mood_classifier.pkl')
            print("✅ Models loaded successfully")
            return True
        return False

print("✅ Mood Classifier module created!")
