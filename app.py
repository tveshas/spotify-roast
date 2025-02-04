from flask import Flask, render_template, request, redirect, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from urllib.parse import urlencode
import json
import os
import re
import secrets
from datetime import datetime
from collections import Counter
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.jinja_env.filters['lower'] = lambda x: x.lower() if x else x

# Configuration
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
REDIRECT_URI = "http://localhost:5001/callback"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_KEY)

# Helper functions
def extract_user_id(input_string):
    url_match = re.search(r'spotify\.com/user/([a-zA-Z0-9]+)', input_string)
    return url_match.group(1) if url_match else input_string

def analyze_music_taste(all_top_tracks):
    analysis = {'top_genres': {}, 'top_artists': {}, 'popularity_stats': {}, 'genre_evolution': {}}
    
    for time_range, data in all_top_tracks.items():
        all_genres = []
        artists = []
        popularity_scores = []
        
        for track in data['tracks']:
            all_genres.extend(track['genres'])
            artists.extend(track['artists'])
            popularity_scores.append(track['popularity'])
        
        analysis['top_genres'][time_range] = dict(Counter(all_genres).most_common(5))
        analysis['top_artists'][time_range] = dict(Counter(artists).most_common(5))
        
        if popularity_scores:
            analysis['popularity_stats'][time_range] = {
                'average': sum(popularity_scores) / len(popularity_scores),
                'max': max(popularity_scores),
                'min': min(popularity_scores)
            }
    
    time_order = ['short_term', 'medium_term', 'long_term']
    all_time_genres = set().union(*[analysis['top_genres'][tr].keys() for tr in time_order])
    
    for genre in all_time_genres:
        analysis['genre_evolution'][genre] = {tr: analysis['top_genres'][tr].get(genre, 0) for tr in time_order}
    
    return analysis

def generate_genz_analysis(analysis_data):
    prompt = """analyze this music data like a chaotic tiktak teen using:
    - all lowercase + emojis every 3-5 words
    - gen-z/alpha slang (rizz, gyatt, skibidi, fanum tax, etc)
    - savage roasts + tiktok refs
    - sections: vibe check, aux royalty, genre gyatt, toxic truth
    
    data: {data}""".format(data=json.dumps(analysis_data))

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "u r a savage 16yo tiktak addict roasting mid music taste"},
                {"role": "user", "content": prompt}
            ],
            temperature=1.2,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"failed to generate roast 💀\n{json.dumps(analysis_data, indent=2)}"

# Routes
@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    session.clear()
    user_input = request.form.get('user_id')
    if not user_input:
        return redirect(url_for('index'))
    
    session['user_id'] = extract_user_id(user_input)
    session['auth_state'] = secrets.token_urlsafe(16)
    
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-top-read",
        show_dialog=True,
        cache_handler=FlaskSessionCacheHandler(session),
        state=session['auth_state']
    )
    
    return redirect(f"{sp_oauth.get_authorize_url()}&force_verify=true")

@app.route('/callback')
def callback():
    if 'auth_state' not in session or request.args.get('state') != session['auth_state']:
        return redirect(url_for('index'))
    
    sp_oauth = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        cache_handler=FlaskSessionCacheHandler(session)
    )
    
    try:
        token_info = sp_oauth.get_access_token(request.args.get('code'))
        sp = spotipy.Spotify(auth=token_info['access_token'])
        user_profile = sp.current_user()
        
        time_ranges = {
            'short_term': 'Last 4 Weeks',
            'medium_term': 'Last 6 Months', 
            'long_term': 'All Time'
        }
        
        all_top_tracks = {}
        for tr, label in time_ranges.items():
            tracks = sp.current_user_top_tracks(limit=20, time_range=tr)
            tracks_data = [{
                'track_name': t['name'],
                'artists': [a['name'] for a in t['artists']],
                'genres': sp.artist(t['artists'][0]['id'])['genres'],
                'popularity': t['popularity']
            } for t in tracks['items']]
            
            all_top_tracks[tr] = {'label': label, 'tracks': tracks_data}
        
        analysis = analyze_music_taste(all_top_tracks)
        return render_template('success.html',
            user_profile=user_profile,
            analysis=analysis,
            genz_analysis=generate_genz_analysis(analysis),
            time_ranges=time_ranges
        )
    
    except Exception as e:
        return f"error: {str(e)}", 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(f"https://accounts.spotify.com/logout?continue={url_for('index', _external=True)}")

@app.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)