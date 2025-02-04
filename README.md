# Spotify Roast 🔥

A fun web app that analyzes your Spotify listening history and roasts your music taste in Gen-Z style using AI. Built with Flask, Spotify API, and OpenAI's GPT-4.

## Features

- 🎵 Analyzes your top tracks across different time ranges
- 📊 Visualizes your most-played genres and artists
- 🤖 Generates AI-powered roasts in Gen-Z style
- 💅 Clean, Spotify-inspired UI using Tailwind CSS
<img width="407" alt="Screenshot 2025-02-04 at 11 39 39" src="https://github.com/user-attachments/assets/5380ff66-cf6e-4c86-952d-3f8bfe1a9f9a" />
<img width="664" alt="Screenshot 2025-02-04 at 11 39 00" src="https://github.com/user-attachments/assets/c1d25725-19d1-433d-90fd-b2a3fbda41dc" />
<img width="612" alt="Screenshot 2025-02-04 at 11 39 21" src="https://github.com/user-attachments/assets/9f7bd933-eaf3-49dd-8d2b-0e4df5c2a577" />
<img width="635" alt="Screenshot 2025-02-04 at 11 39 27" src="https://github.com/user-attachments/assets/dada17d9-5ce9-4f45-a8f5-c0ec3d5ac5a6" />

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/spotify-roast.git
cd spotify-roast
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Create a `.env` file in the root directory
   - Add your Spotify and OpenAI API credentials:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_secret_key
```

4. Run the application:
```bash
python app.py
```

The app will be available at `http://localhost:5001`

## Configuration

To use this app, you'll need:
- A Spotify Developer account and API credentials
- An OpenAI API key
- Python 3.7 or higher

## License

MIT License - feel free to use and modify as you like!

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
