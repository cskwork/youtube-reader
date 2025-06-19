# YouTube Transcript Reader with AI Summarization

A modern web application that extracts transcripts from YouTube videos and provides AI-powered summarization using multiple LLM providers.

## Features

- 📝 **YouTube Transcript Extraction**: Extract transcripts in multiple languages
- 🤖 **AI Summarization**: Generate summaries using OpenAI, Anthropic Claude, or Google Gemini
- 🔍 **Search**: Search within transcripts with highlighting
- 💾 **Export**: Export transcripts as TXT or JSON
- ⏱️ **Timestamp Navigation**: Click timestamps to jump to specific video moments
- 🎨 **Modern UI**: Clean, responsive interface with Bootstrap 5
- 🌐 **Multi-language Support**: Extract transcripts in various languages

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd youtube-reader
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory:

```env
# LLM API Keys (at least one required for summarization)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

### Basic Usage
1. Enter a YouTube URL in the input field
2. Select the transcript language
3. Click "Get Transcript" to fetch the transcript
4. The transcript will appear in the left panel with clickable timestamps

### AI Summarization
1. After loading a transcript, select an LLM provider (OpenAI, Anthropic, or Google)
2. Choose a summary type:
   - **Short Summary**: 3-5 sentences
   - **Medium Summary**: 2-3 paragraphs
   - **Detailed Summary**: Comprehensive with key points
   - **Key Points Only**: Bulleted list of main points
3. Click "Generate Summary" to create an AI summary

### Search Feature
1. Click the search icon in the transcript panel
2. Enter your search query
3. Matching sections will be highlighted
4. The view will automatically scroll to the first match

### Export Options
- **TXT Format**: Plain text with timestamps
- **JSON Format**: Structured data with all metadata

## API Endpoints

- `POST /api/transcript` - Fetch YouTube transcript
- `POST /api/summarize` - Generate AI summary
- `POST /api/search` - Search within transcript
- `POST /api/export` - Export transcript data

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **LLM Integration**: OpenAI, Anthropic, Google Gemini
- **YouTube API**: youtube-transcript-api

## Project Structure

```
youtube-reader/
├── app.py              # Flask application
├── templates/
│   └── index.html      # Main UI template
├── static/
│   ├── css/
│   │   └── style.css   # Custom styles
│   └── js/
│       └── app.js      # Frontend JavaScript
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── output/            # Transcript outputs (from CLI version)
```

## Advanced Features

### URL Parameters
You can link directly to a video transcript:
```
http://localhost:5000?v=VIDEO_ID
```

### Keyboard Shortcuts
- `Enter` in URL field: Fetch transcript
- `Enter` in search field: Search transcript

## Troubleshooting

### Common Issues

1. **"No transcript available"**: The video might not have captions enabled
2. **"API key not configured"**: Make sure you've set up at least one LLM API key in `.env`
3. **Export not working**: Check browser popup blocker settings

### API Key Setup

- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com)
- **Anthropic**: Get your API key from [Anthropic Console](https://console.anthropic.com)
- **Google**: Get your API key from [Google AI Studio](https://makersuite.google.com)

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License 