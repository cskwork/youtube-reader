from flask import Flask, render_template, request, jsonify, send_file
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os
import re
from datetime import datetime
import json
from typing import Dict, List, Optional
from anthropic import Anthropic
import google.generativeai as genai
from dotenv import load_dotenv
import io
import markdown

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)

# LLM 설정
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# LLM 클라이언트 초기화
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

def extract_video_id(url: str) -> Optional[str]:
    """YouTube URL에서 비디오 ID 추출"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # URL이 이미 비디오 ID인 경우
    if len(url) == 11 and re.match(r'^[0-9A-Za-z_-]{11}$', url):
        return url
    
    return None

def get_transcript(video_id: str, language: str = 'en') -> Dict:
    """YouTube 트랜스크립트 가져오기"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # 요청된 언어의 트랜스크립트 찾기
        try:
            transcript = transcript_list.find_transcript([language])
        except:
            # 요청된 언어가 없으면 자동 생성된 것 찾기
            transcript = transcript_list.find_generated_transcript([language])
        
        # 트랜스크립트 데이터 가져오기
        transcript_data = transcript.fetch()
        
        # API가 반환하는 데이터가 어떤 형태이든 처리할 수 있도록 각 항목을 확인하여
        # 일관된 딕셔너리 리스트를 생성합니다.
        transcript_dict_list = []
        for segment in transcript_data:
            if isinstance(segment, dict):
                transcript_dict_list.append({
                    'text': segment.get('text', ''),
                    'start': segment.get('start', 0),
                    'duration': segment.get('duration', 0)
                })
            else: # It's an object
                transcript_dict_list.append({
                    'text': getattr(segment, 'text', ''),
                    'start': getattr(segment, 'start', 0),
                    'duration': getattr(segment, 'duration', 0)
                })

        # 일관되게 만들어진 딕셔너리 리스트에서 전체 텍스트를 생성합니다.
        full_text = '\n'.join([item['text'] for item in transcript_dict_list])
        
        return {
            'success': True,
            'video_id': video_id,
            'language': transcript.language_code,
            'is_generated': transcript.is_generated,
            'transcript_data': transcript_dict_list,
            'full_text': full_text
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def summarize_with_openai(text: str, summary_type: str = 'medium') -> str:
    """OpenAI GPT를 사용한 요약"""
    if not OPENAI_API_KEY:
        return "OpenAI API key not configured"
    
    prompts = {
        'short': "Provide a brief 3-5 sentence summary of the following transcript:",
        'medium': "Provide a comprehensive summary (about 2-3 paragraphs) of the following transcript:",
        'detailed': "Provide a detailed summary with key points and main topics from the following transcript:",
        'key_points': "Extract the top 10 key points from the following transcript as a bulleted list:"
    }
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes video transcripts."},
                {"role": "user", "content": f"{prompts.get(summary_type, prompts['medium'])}\n\n{text[:4000]}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error with OpenAI: {str(e)}"

def summarize_with_anthropic(text: str, summary_type: str = 'medium') -> str:
    """Anthropic Claude를 사용한 요약"""
    if not anthropic_client:
        return "Anthropic API key not configured"
    
    prompts = {
        'short': "Provide a brief 3-5 sentence summary of the following transcript:",
        'medium': "Provide a comprehensive summary (about 2-3 paragraphs) of the following transcript:",
        'detailed': "Provide a detailed summary with key points and main topics from the following transcript:",
        'key_points': "Extract the top 10 key points from the following transcript as a bulleted list:"
    }
    
    try:
        message = anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompts.get(summary_type, prompts['medium'])}\n\n{text[:4000]}"
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"Error with Anthropic: {str(e)}"

def summarize_with_google(text: str, summary_type: str = 'medium') -> str:
    """Google Gemini를 사용한 요약"""
    if not GOOGLE_API_KEY:
        return "Google API key not configured"
    
    prompts = {
        'short': "Provide a brief 3-5 sentence summary of the following transcript:",
        'medium': "Provide a comprehensive summary (about 2-3 paragraphs) of the following transcript:",
        'detailed': "Provide a detailed summary with key points and main topics from the following transcript:",
        'key_points': "Extract the top 10 key points from the following transcript as a bulleted list:"
    }
    
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{prompts.get(summary_type, prompts['medium'])}\n\n{text[:4000]}")
        return response.text
    except Exception as e:
        return f"Error with Google Gemini: {str(e)}"

def format_timestamp(seconds: float) -> str:
    """초를 HH:MM:SS 형식으로 변환"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/transcript', methods=['POST'])
def get_transcript_api():
    """트랜스크립트 가져오기 API"""
    data = request.json
    url = data.get('url', '')
    language = data.get('language', 'en')
    
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'success': False, 'error': 'Invalid YouTube URL'}), 400
    
    result = get_transcript(video_id, language)
    
    if result['success']:
        # 타임스탬프 포맷팅
        for item in result['transcript_data']:
            item['formatted_start'] = format_timestamp(item['start'])
    
    return jsonify(result)

@app.route('/api/summarize', methods=['POST'])
def summarize_api():
    """텍스트 요약 API"""
    data = request.json
    text = data.get('text', '')
    summary_type = data.get('summary_type', 'medium')
    llm_provider = data.get('llm_provider', 'openai')
    
    if not text:
        return jsonify({'success': False, 'error': 'No text provided'}), 400
    
    try:
        if llm_provider == 'openai':
            summary = summarize_with_openai(text, summary_type)
        elif llm_provider == 'anthropic':
            summary = summarize_with_anthropic(text, summary_type)
        elif llm_provider == 'google':
            summary = summarize_with_google(text, summary_type)
        else:
            summary = "Invalid LLM provider"
        
        # Markdown을 HTML로 변환
        summary_html = markdown.markdown(summary)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'summary_html': summary_html,
            'provider': llm_provider,
            'type': summary_type
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_transcript():
    """트랜스크립트 내보내기"""
    data = request.json
    transcript_data = data.get('transcript_data', [])
    format_type = data.get('format', 'txt')
    include_timestamps = data.get('include_timestamps', True)
    
    if format_type == 'txt':
        output = io.StringIO()
        for item in transcript_data:
            if include_timestamps:
                output.write(f"[{item['formatted_start']}] {item['text']}\n")
            else:
                output.write(f"{item['text']}\n")
        
        content = output.getvalue()
        output.seek(0)
        
        return send_file(
            io.BytesIO(content.encode('utf-8')),
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'transcript_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        )
    
    elif format_type == 'json':
        content = json.dumps(transcript_data, indent=2, ensure_ascii=False)
        
        return send_file(
            io.BytesIO(content.encode('utf-8')),
            mimetype='application/json',
            as_attachment=True,
            download_name=f'transcript_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
    
    else:
        return jsonify({'success': False, 'error': 'Invalid format'}), 400

@app.route('/api/search', methods=['POST'])
def search_transcript():
    """트랜스크립트 내 검색"""
    data = request.json
    transcript_data = data.get('transcript_data', [])
    query = data.get('query', '').lower()
    
    if not query:
        return jsonify({'success': False, 'error': 'No search query provided'}), 400
    
    results = []
    for i, item in enumerate(transcript_data):
        if query in item['text'].lower():
            results.append({
                'index': i,
                'text': item['text'],
                'start': item['start'],
                'formatted_start': item.get('formatted_start', format_timestamp(item['start'])),
                'duration': item.get('duration', 0)
            })
    
    return jsonify({
        'success': True,
        'results': results,
        'count': len(results)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001) 