import sys
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def get_transcript_text(video_id: str, languages=['en']):
    """
    지정된 YouTube 동영상 ID에 대한 스크립트를 가져옵니다.
    성공 시 (스크립트, True)를, 실패 시 (오류 메시지, False)를 반환합니다.
    """
    try:
        # Deprecated 되었지만, 언어 지정이 간편하여 get_transcript를 사용합니다.
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        # 각 세그먼트를 결합하고 개행 문자를 공백으로 바꿉니다.
        full_transcript = " ".join(segment['text'].replace('\n', ' ') for segment in transcript_list)
        return full_transcript, True
    except NoTranscriptFound:
        # 지정된 언어의 스크립트를 찾지 못한 경우에 대한 처리입니다.
        return f"해당 언어({languages})로 된 스크립트를 찾을 수 없습니다.", False
    except Exception as e:
        # 라이브러리에서 발생하는 다른 모든 예외를 처리합니다.
        return f"스크립트를 가져올 수 없습니다: {e}", False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # 사용법 및 오류 메시지는 stderr로 출력합니다.
        print("사용법: python main.py <video_id> [language_code]", file=sys.stderr)
        print("예시: python main.py jNQXAC9IVRw", file=sys.stderr)
        print("예시: python main.py VYOjWn6h5g8 ko", file=sys.stderr)
        sys.exit(1)

    video_id = sys.argv[1]
    languages = [sys.argv[2]] if len(sys.argv) > 2 else ['en']

    # 정보 메시지는 stderr로 보냅니다.
    print(f"'{video_id}' 동영상에 대한 스크립트 가져오기 (언어: {languages[0]})...", file=sys.stderr)

    transcript, success = get_transcript_text(video_id, languages=languages)

    if success:
        # 성공 시, 스크립트 본문은 stdout으로 출력하여 리디렉션을 허용합니다.
        print(transcript)
        print(f"\n스크립트가 성공적으로 가져와졌습니다.", file=sys.stderr)
    else:
        # 실패 시, 오류 메시지는 stderr로 출력합니다.
        print(transcript, file=sys.stderr)
        print(f"스크립트를 가져오는 데 실패했습니다. 위의 오류 메시지를 확인하세요.", file=sys.stderr)
        sys.exit(1) 