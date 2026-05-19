from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import joblib
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.food_recommender import FoodRecommender
from services.music_recommender import MusicRecommender

app = FastAPI(title="Mood-Based Food & Music Recommendation System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Loading models...")
print("=" * 60)

try:
    vectorizer = joblib.load(os.path.join(BASE_PATH, 'models', 'vectorizer.pkl'))
    classifier = joblib.load(os.path.join(BASE_PATH, 'models', 'mood_classifier.pkl'))
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"⚠️ Error loading models: {e}")
    vectorizer = None
    classifier = None

food_recommender = FoodRecommender()
music_recommender = MusicRecommender()

# Label correction for swapped sadness/joy
MODEL_TO_CORRECT = [1, 0, 2, 3, 4, 5]
CORRECT_EMOTIONS = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

def correct_prediction(model_pred, model_proba):
    correct_pred = MODEL_TO_CORRECT[model_pred]
    correct_proba = [0.0] * 6
    for i in range(6):
        correct_proba[MODEL_TO_CORRECT[i]] = model_proba[i]
    return correct_pred, correct_proba

print("\n✅ Label correction enabled")

# ============================================
# FORCED OVERRIDE - ANGER HAS HIGHEST PRIORITY
# ============================================
def force_correct_mood(text):
    """Direct keyword matching - forces correct mood"""
    t = text.lower()
    
    # ANGER - HIGHEST PRIORITY (MUST BE FIRST)
    if any(word in t for word in ['angry', 'pissed', 'mad', 'furious', 'rage', 'annoyed', 
                                    'frustrated', 'irritated', 'outraged', 'livid', 'fuming', 
                                    'hate', 'hatred', 'boiling', 'infuriated', 'enraged',
                                    'anger', 'piss', 'pissing', 'irritate', 'frustrate']):
        print(f"🔥 ANGER DETECTED: '{text[:50]}'")
        return 'anger', 0.95
    
    # Surprise keywords
    if any(word in t for word in ['wow', 'surprised', 'surprise', 'shocked', 'astonished', 
                                    'unexpected', 'unbelievable', "can't believe", "cannot believe",
                                    "no way", "oh my god", "omg", "what a surprise", "amazing",
                                    "incredible", "startled", "dumbfounded", "shocking"]):
        print(f"✨ SURPRISE DETECTED: '{text[:50]}'")
        return 'surprise', 0.95
    
    # Sadness keywords
    if any(word in t for word in ['sad', 'depressed', 'down', 'lonely', 'heartbroken', 
                                    'gloomy', 'miserable', 'hopeless', 'devastated', 'crying']):
        return 'sadness', 0.95
    
    # Fear keywords
    if any(word in t for word in ['scared', 'afraid', 'anxious', 'worried', 'terrified', 
                                    'nervous', 'fear', 'frightened', 'panicked', 'dread', 'horror']):
        return 'fear', 0.95
    
    # Love keywords
    if any(word in t for word in ['love', 'adore', 'affection', 'romantic', 'cherish', 
                                    'devotion', 'beloved']):
        return 'love', 0.95
    
    # Joy keywords (last priority)
    if any(word in t for word in ['happy', 'joy', 'excited', 'wonderful', 'great', 
                                    'fantastic', 'awesome', 'glad', 'pleased', 'delighted']):
        return 'joy', 0.95
    
    return None, None

print("✅ Force override enabled (ANGER has HIGHEST priority)")
print("=" * 60)

class MoodInput(BaseModel):
    text: str
    user_id: Optional[str] = "anonymous"

class RecommendationResponse(BaseModel):
    mood: str
    confidence: float
    mood_emoji: str
    mood_response: str
    food_recommendations: List[Dict]
    music_recommendations: List[Dict]
    all_mood_scores: Dict[str, float]

@app.get("/")
async def root():
    return {"status": "running", "available_moods": CORRECT_EMOTIONS}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "models_loaded": vectorizer is not None}

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(mood_input: MoodInput):
    if vectorizer is None or classifier is None:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    try:
        # FIRST: Try force override (direct keyword matching)
        forced_mood, forced_confidence = force_correct_mood(mood_input.text)
        
        if forced_mood:
            # Use forced mood
            mood = forced_mood
            confidence = forced_confidence
            all_scores = {emotion: 0.0 for emotion in CORRECT_EMOTIONS}
            all_scores[mood] = confidence
        else:
            # Use model prediction
            X = vectorizer.transform([mood_input.text])
            model_pred = classifier.predict(X)[0]
            model_proba = classifier.predict_proba(X)[0]
            
            correct_pred, correct_proba = correct_prediction(model_pred, model_proba)
            mood = CORRECT_EMOTIONS[correct_pred]
            confidence = correct_proba[correct_pred]
            all_scores = {CORRECT_EMOTIONS[i]: float(correct_proba[i]) for i in range(6)}
        
        # Get recommendations
        foods = food_recommender.get_food_recommendations(mood, limit=3)
        music = music_recommender.get_music_recommendations(mood, limit=3)
        
        mood_responses = {
            'joy': "🎉 I sense happiness! Let's celebrate with something special!",
            'sadness': "💙 I understand you're feeling down. Here's some comfort food to lift your spirits.",
            'love': "❤️ Feeling the love! Here are some romantic recommendations.",
            'anger': "🔥 Let's cool down with some satisfying spicy choices!",
            'fear': "🫂 Feeling anxious? Let's find something comforting.",
            'surprise': "✨ Wow! What a pleasant surprise! Here's something special for this unexpected moment!"
        }
        
        mood_emojis = {'joy': '😊', 'sadness': '😢', 'love': '❤️', 
                       'anger': '😠', 'fear': '😨', 'surprise': '😲'}
        
        return RecommendationResponse(
            mood=mood,
            confidence=confidence,
            mood_emoji=mood_emojis.get(mood, '😊'),
            mood_response=mood_responses.get(mood, "Here are your recommendations!"),
            food_recommendations=foods,
            music_recommendations=music,
            all_mood_scores=all_scores
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/moods")
async def get_available_moods():
    return {"moods": CORRECT_EMOTIONS}

@app.get("/food/{mood}")
async def get_food_by_mood(mood: str, limit: int = 3):
    if mood not in CORRECT_EMOTIONS:
        raise HTTPException(status_code=404, detail=f"Mood '{mood}' not found")
    foods = food_recommender.get_food_recommendations(mood, limit=limit)
    return {"mood": mood, "recommendations": foods}

@app.get("/music/{mood}")
async def get_music_by_mood(mood: str, limit: int = 3):
    if mood not in CORRECT_EMOTIONS:
        raise HTTPException(status_code=404, detail=f"Mood '{mood}' not found")
    music = music_recommender.get_music_recommendations(mood, limit=limit)
    return {"mood": mood, "recommendations": music}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)