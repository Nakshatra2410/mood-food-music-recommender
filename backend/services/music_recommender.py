import random

class MusicRecommender:
    def __init__(self):
        self.music_db = {
            'joy': [
                {'name': 'Happy', 'artist': 'Pharrell Williams', 'genre': 'pop', 'year': 2013, 'spotify_id': '6Nl5KRfE4DqZKuM8YE5RTV'},
                {'name': "Can't Stop The Feeling", 'artist': 'Justin Timberlake', 'genre': 'pop', 'year': 2016, 'spotify_id': '5F2s2nUapB7hZKgq3LvX8t'},
                {'name': 'Uptown Funk', 'artist': 'Mark Ronson ft. Bruno Mars', 'genre': 'funk', 'year': 2014, 'spotify_id': '3e1LplHbgB0vJ3RT9GXqHo'},
                {'name': 'Good as Hell', 'artist': 'Lizzo', 'genre': 'pop', 'year': 2016, 'spotify_id': '5CwyQ0VnbZ51S9bNQrQpS6'},
                {'name': 'Dancing Queen', 'artist': 'ABBA', 'genre': 'disco', 'year': 1976, 'spotify_id': '0GjEhVFGZW8afUYGChu3Rr'}
            ],
            'sadness': [
                {'name': 'Someone Like You', 'artist': 'Adele', 'genre': 'ballad', 'year': 2011, 'spotify_id': '1kMYIVI4H9Z1JxsXBcSUqe'},
                {'name': 'Fix You', 'artist': 'Coldplay', 'genre': 'rock', 'year': 2005, 'spotify_id': '7LVHVU3tWfcxj5aiPFEW4Q'},
                {'name': 'Yesterday', 'artist': 'The Beatles', 'genre': 'rock', 'year': 1965, 'spotify_id': '3BQHpFgApUd2bQCG2e0hzF'},
                {'name': 'Hallelujah', 'artist': 'Jeff Buckley', 'genre': 'folk', 'year': 1994, 'spotify_id': '3pRaLNL3b8xYYuSoK7OoHp'},
                {'name': 'The Scientist', 'artist': 'Coldplay', 'genre': 'rock', 'year': 2002, 'spotify_id': '75JFxkI2RXiU7L9VXzMkle'}
            ],
            'love': [
                {'name': 'Perfect', 'artist': 'Ed Sheeran', 'genre': 'pop', 'year': 2017, 'spotify_id': '0tgVpDi06FyKpA1z0VMD4v'},
                {'name': 'All of Me', 'artist': 'John Legend', 'genre': 'r&b', 'year': 2013, 'spotify_id': '3U4isOIWM3VvDubwSI3y7a'},
                {'name': 'Thinking Out Loud', 'artist': 'Ed Sheeran', 'genre': 'pop', 'year': 2014, 'spotify_id': '34gCuhDGsG4bRPIf9bb02f'},
                {'name': 'At Last', 'artist': 'Etta James', 'genre': 'jazz', 'year': 1960, 'spotify_id': '4Hhv2vrOTy89HFRcjU3QOx'},
                {'name': 'Just the Way You Are', 'artist': 'Bruno Mars', 'genre': 'pop', 'year': 2010, 'spotify_id': '7BqBn9nzAq8spo5oL7DcV0'}
            ],
            'anger': [
                {'name': 'Break Stuff', 'artist': 'Limp Bizkit', 'genre': 'rock', 'year': 2000, 'spotify_id': '5cZqsjY6U8RDHMOYDQVhQT'},
                {'name': 'In the End', 'artist': 'Linkin Park', 'genre': 'rock', 'year': 2001, 'spotify_id': '60a0Rd6rkpjxjPbaKzXjfq'},
                {'name': 'Killing in the Name', 'artist': 'Rage Against the Machine', 'genre': 'rock', 'year': 1992, 'spotify_id': '59WN2psjkt1tyaxjspN8fp'},
                {'name': 'Boulevard of Broken Dreams', 'artist': 'Green Day', 'genre': 'rock', 'year': 2004, 'spotify_id': '5GorCbAP4aL0EJ16uxGPDB'},
                {'name': 'Smells Like Teen Spirit', 'artist': 'Nirvana', 'genre': 'rock', 'year': 1991, 'spotify_id': '4ghd4e2OCcZ4Wv4fI5TkW7'}
            ],
            'fear': [
                {'name': 'Weightless', 'artist': 'Marconi Union', 'genre': 'ambient', 'year': 2011, 'spotify_id': '5dvsfJqUz74hF01F7UIAqT'},
                {'name': 'Clair de Lune', 'artist': 'Debussy', 'genre': 'classical', 'year': 1905, 'spotify_id': '5CvUbkfNla3yHBj26QJcHk'},
                {'name': 'River Flows in You', 'artist': 'Yiruma', 'genre': 'piano', 'year': 2001, 'spotify_id': '3xr8COed4nPPn6XWZ0iCGr'},
                {'name': 'Canon in D', 'artist': 'Pachelbel', 'genre': 'classical', 'year': 1680, 'spotify_id': '4r7qhBcBZOrPdi0li8ZfAj'},
                {'name': 'Nocturne', 'artist': 'Chopin', 'genre': 'classical', 'year': 1830, 'spotify_id': '5CvUbkfNla3yHBj26QJcHk'}
            ],
            'surprise': [
                {'name': 'Sandstorm', 'artist': 'Darude', 'genre': 'electronic', 'year': 1999, 'spotify_id': '6Sy9BUbgFse0n0LPA5lwy5'},
                {'name': 'Animals', 'artist': 'Martin Garrix', 'genre': 'edm', 'year': 2013, 'spotify_id': '2bL2gyO6kBc08k9KAvOeTr'},
                {'name': 'Titanium', 'artist': 'David Guetta', 'genre': 'electronic', 'year': 2011, 'spotify_id': '2dlzSUMaUImCSBgPWsjhHe'},
                {'name': 'Wake Me Up', 'artist': 'Avicii', 'genre': 'edm', 'year': 2013, 'spotify_id': '2ohr9HUjKcyKz2P6hPwVUz'},
                {'name': 'Levels', 'artist': 'Avicii', 'genre': 'edm', 'year': 2011, 'spotify_id': '2ohr9HUjKcyKz2P6hPwVUz'}
            ]
        }
    
    def get_music_recommendations(self, mood, limit=3):
        if mood not in self.music_db:
            mood = 'joy'
        songs = self.music_db[mood].copy()
        random.shuffle(songs)
        recommendations = []
        for song in songs[:limit]:
            recommendations.append({
                'name': song['name'],
                'artist': song['artist'],
                'genre': song['genre'],
                'year': song['year'],
                'spotify_url': f"https://open.spotify.com/track/{song['spotify_id']}"
            })
        return recommendations

print("✅ Music Recommender created!")
