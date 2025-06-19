#!/bin/bash

# 스크립트가 있는 디렉토리로 이동하여 어디서든 실행할 수 있도록 합니다.
cd "$(dirname "$0")"

# 가상 환경이 존재하는지 확인하고 활성화합니다.
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "오류: '.venv' 가상 환경을 찾을 수 없습니다." >&2
    echo "먼저 'python3.12 -m venv .venv'를 실행하여 가상 환경을 생성하고," >&2
    echo "'.venv/bin/pip install -r requirements.txt'로 의존성을 설치하세요." >&2
    exit 1
fi

# 비디오 ID 인수가 제공되었는지 확인합니다.
if [ -z "$1" ]; then
    echo "사용법: $0 <video_id> [language_code]" >&2
    echo "  <video_id>       : YouTube 동영상의 ID (필수)" >&2
    echo "  [language_code]  : 스크립트의 언어 코드 (선택, 기본값: en)" >&2
    echo "" >&2
    echo "예시:" >&2
    echo "  $0 jNQXAC9IVRw" >&2
    echo "  $0 VYOjWn6h5g8 ko" >&2
    exit 1
fi

VIDEO_ID=$1
# 두 번째 인수가 있으면 해당 언어를 사용하고, 없으면 'en'을 기본값으로 사용합니다.
LANGUAGE=${2:-en}

# 'output' 디렉토리를 생성합니다 (존재하지 않는 경우).
OUTPUT_DIR="output"
mkdir -p "$OUTPUT_DIR"

# 출력 파일 경로를 설정합니다.
OUTPUT_FILE="$OUTPUT_DIR/${VIDEO_ID}_${LANGUAGE}.txt"

# Python 스크립트를 실행합니다.
# 성공적인 출력(stdout)만 파일로 리디렉션됩니다.
# 오류 출력(stderr)은 콘솔에 그대로 표시됩니다.
python main.py "$VIDEO_ID" "$LANGUAGE" > "$OUTPUT_FILE"

# $?는 마지막으로 실행된 명령어의 종료 코드를 담고 있습니다.
# 0은 성공, 그 외는 오류를 의미합니다.
if [ $? -eq 0 ]; then
    echo "스크립트가 성공적으로 '$OUTPUT_FILE' 파일에 저장되었습니다."
else
    echo "스크립트를 가져오는 데 실패했습니다. 위의 오류 메시지를 확인하세요." >&2
    # 실패 시 생성된 빈 파일을 삭제합니다.
    rm -f "$OUTPUT_FILE"
fi 