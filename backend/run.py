import uvicorn
import os
import sys

# Add the backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Starting Mood-Based Food & Music Recommendation System")
    print("=" * 50)
    print("Backend server will run at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )