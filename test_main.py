import pytest
from main import get_transcript_text
from youtube_transcript_api import NoTranscriptFound

def test_get_transcript_text_success(mocker):
    """
    성공적인 스크립트 추출 사례를 테스트합니다. (영어)
    """
    # get_transcript가 반환할 모의 데이터를 설정합니다.
    mock_transcript = [
        {'text': 'All right, so here we are', 'start': 0.0, 'duration': 2.0},
        {'text': 'in front of the\nelephants', 'start': 2.0, 'duration': 2.0}
    ]
    mocker.patch('main.YouTubeTranscriptApi.get_transcript', return_value=mock_transcript)
    
    transcript = get_transcript_text('any_video_id')
    assert "here we are" in transcript
    assert "in front of the elephants" in transcript # 개행 문자가 공백으로 처리되었는지 확인

def test_get_transcript_text_korean_success(mocker):
    """
    성공적인 한국어 스크립트 추출 사례를 테스트합니다.
    """
    mock_transcript = [
        {'text': '한국형 로봇팔 개발', 'start': 0.0, 'duration': 2.0},
        {'text': '우주 잔해물 수거', 'start': 2.0, 'duration': 2.0}
    ]
    mocker.patch('main.YouTubeTranscriptApi.get_transcript', return_value=mock_transcript)
    
    transcript = get_transcript_text('any_korean_video_id', languages=['ko'])
    assert "한국형 로봇팔" in transcript
    assert "우주 잔해물" in transcript

def test_get_transcript_no_transcript_for_language(mocker):
    """
    요청한 언어의 스크립트가 없는 경우를 테스트합니다.
    """
    # get_transcript가 NoTranscriptFound 예외를 발생시키도록 설정합니다.
    # 예외 생성자에 필요한 인수들을 더미 값으로 제공합니다.
    mocker.patch(
        'main.YouTubeTranscriptApi.get_transcript',
        side_effect=NoTranscriptFound('dummy_id', ['de'], {})
    )
    
    transcript = get_transcript_text('any_video_id', languages=['de'])
    assert "해당 언어(['de'])로 된 스크립트를 찾을 수 없습니다." in transcript

def test_no_transcript_at_all(mocker):
    """
    스크립트가 아예 없는 동영상의 경우.
    """
    # get_transcript가 일반 예외를 발생시키도록 설정합니다.
    mocker.patch('main.YouTubeTranscriptApi.get_transcript', side_effect=Exception('Generic error'))
    
    transcript = get_transcript_text('video_with_no_transcripts')
    assert "스크립트를 가져올 수 없습니다" in transcript

def test_get_transcript_invalid_id(mocker):
    """
    잘못된 동영상 ID의 경우를 테스트합니다.
    """
    mocker.patch('main.YouTubeTranscriptApi.get_transcript', side_effect=Exception('Invalid ID error'))

    transcript = get_transcript_text('invalid_video_id')
    assert "스크립트를 가져올 수 없습니다" in transcript 