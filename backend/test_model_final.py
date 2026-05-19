# test_model_final.py - WITH LABEL FIX
import os
import joblib
import sys

print("=" * 60)
print("🧪 TESTING MOOD CLASSIFICATION MODEL (WITH LABEL FIX)")
print("=" * 60)

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(current_dir, 'models')

print(f"\n📁 Models directory: {models_dir}")

# Load models
try:
    vectorizer = joblib.load(os.path.join(models_dir, 'vectorizer.pkl'))
    classifier = joblib.load(os.path.join(models_dir, 'mood_classifier.pkl'))
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    sys.exit(1)

# ============================================
# LABEL FIX (Same as in main.py)
# ============================================
# The model was trained with swapped labels (0=joy, 1=sadness)
# Correct order should be: 0=sadness, 1=joy, 2=love, 3=anger, 4=fear, 5=surprise
MODEL_TO_CORRECT = [1, 0, 2, 3, 4, 5]  # Model index -> Correct index
CORRECT_EMOTIONS = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

def correct_prediction(model_pred, model_proba):
    """Convert model's swapped predictions to correct labels"""
    # Map the predicted index to correct index
    correct_pred = MODEL_TO_CORRECT[model_pred]
    
    # Rearrange all probabilities to correct order
    correct_proba = [0.0] * 6
    for i in range(6):
        correct_proba[MODEL_TO_CORRECT[i]] = model_proba[i]
    
    return correct_pred, correct_proba

print("\n✅ Label correction enabled:")
print("   Model index 0 (joy) → Correct index 1 (joy)")
print("   Model index 1 (sadness) → Correct index 0 (sadness)")

# Test texts
test_texts = [
    "I'm feeling really happy today!",
    "I'm so sad and depressed",
    "I love this so much, it's amazing!",
    "This makes me so angry!",
    "I'm scared and anxious",
    "Wow! What a wonderful surprise!"
]

print("\n" + "=" * 60)
print("📊 PREDICTION RESULTS (AFTER LABEL FIX)")
print("=" * 60)

for text in test_texts:
    # Get raw model predictions
    X = vectorizer.transform([text])
    model_pred = classifier.predict(X)[0]
    model_proba = classifier.predict_proba(X)[0]
    
    # Apply label correction
    correct_pred, correct_proba = correct_prediction(model_pred, model_proba)
    
    mood = CORRECT_EMOTIONS[correct_pred]
    confidence = correct_proba[correct_pred]
    
    print(f"\n📝 '{text}'")
    print(f"   🎯 Corrected Prediction: {mood} ({confidence:.2%})")
    
    # Show raw vs corrected for debugging
    raw_mood = ['joy', 'sadness', 'love', 'anger', 'fear', 'surprise'][model_pred]
    print(f"   🔍 Raw model said: {raw_mood} ({model_proba[model_pred]:.2%})")
    
    # Show all corrected scores
    print(f"   📊 All corrected mood scores:")
    for i, score in enumerate(correct_proba):
        if score > 0.05:  # Only show significant scores
            print(f"      {CORRECT_EMOTIONS[i]}: {score:.3f}")

print("\n" + "=" * 60)
print("✅ Test complete!")