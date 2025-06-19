# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a YouTube transcript extraction and AI summarization web application with both CLI and web interfaces. The application extracts transcripts from YouTube videos in multiple languages and provides AI-powered summaries using OpenAI, Anthropic Claude, or Google Gemini.

## Development Commands

### Setup & Installation
```bash
# Quick start (automated setup)
./run_app.sh

# Manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your API keys
```

### Running the Application
```bash
# Web application (runs on port 5001)
python app.py

# CLI usage
python main.py <video_id> [language_code]
./run.sh <video_id> [language_code]
```

### Testing
```bash
# Run unit tests
pytest test_main.py -v

# Run tests with coverage (if needed)
pytest test_main.py -v --cov=main
```

### Dependencies Management
```bash
# Install dependencies
pip install -r requirements.txt

# Update requirements
pip freeze > requirements.txt
```

## Architecture Overview

### Dual Interface Design
- **CLI Interface** (`main.py`): Simple transcript extraction to files
- **Web Interface** (`app.py`): Full-featured Flask web application with AI summarization

### Core Components

1. **Transcript Extraction** (`main.py`, `app.py`):
   - Uses `youtube-transcript-api` for transcript fetching
   - Supports multiple languages: English, Korean, Japanese, Spanish, French, German
   - Handles both manual and auto-generated transcripts

2. **AI Integration** (`app.py`):
   - Multi-provider LLM support (OpenAI, Anthropic Claude, Google Gemini)
   - Four summary types: Short, Medium, Detailed, Key Points
   - Markdown formatting for rich text output

3. **Web Interface** (`templates/index.html`, `static/`):
   - Bootstrap 5 responsive design
   - Real-time search with highlighting
   - Timestamp navigation
   - Export functionality (TXT, JSON)

### API Endpoints
- `POST /api/transcript` - Fetch YouTube transcript
- `POST /api/summarize` - Generate AI summary using selected LLM
- `POST /api/search` - Search within transcript with highlighting
- `POST /api/export` - Export transcript data in various formats

## Configuration

### Environment Variables (`.env`)
```env
# LLM API Keys (at least one required for summarization)
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here  
GOOGLE_API_KEY=your_google_api_key_here
```

### Important Notes
- Application runs on **port 5001** (changed from 5000)
- Virtual environment (`.venv`) is required and managed by run scripts
- Korean comments are used throughout the codebase following Korean coding standards
- TDD approach with comprehensive unit tests using pytest and mocking

## File Structure Context

### Key Files
- `app.py`: Main Flask application with LLM integrations
- `main.py`: CLI transcript extraction utility
- `test_main.py`: Unit tests with Korean comments and TDD approach
- `run.sh`: CLI execution script with virtual environment handling
- `run_app.sh`: Quick start script for web application
- `templates/index.html`: Main web interface
- `static/css/style.css`: Custom styling
- `static/js/app.js`: Frontend JavaScript with API interactions

### Data Flow
1. **URL Processing**: Extract video ID from various YouTube URL formats
2. **Transcript Fetching**: Use YouTube Transcript API with language fallbacks
3. **AI Processing**: Send transcript to selected LLM provider for summarization
4. **Frontend Display**: Render with timestamp navigation and search capabilities
5. **Export**: Generate downloadable files in TXT or JSON format

## Testing Strategy

The project follows TDD principles with:
- **Unit tests** for core transcript extraction functionality
- **Mocking** for external API calls (YouTube Transcript API)
- **Korean documentation** in test files
- **Success and failure scenarios** covered
- **Language-specific testing** (English, Korean)

Run tests before making changes to ensure functionality is preserved.

## Development Workflow

1. **Setup**: Use `./run_app.sh` for quick environment setup
2. **Configuration**: Ensure `.env` file has required API keys
3. **Testing**: Run `pytest test_main.py -v` before committing changes
4. **Web Development**: App auto-reloads in development mode
5. **CLI Testing**: Use `./run.sh <video_id>` for command-line testing

The application supports both development and production deployment with comprehensive error handling and user feedback.