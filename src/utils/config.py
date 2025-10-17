"""환경 설정 관리 모듈"""
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 네이버 API 인증 정보
NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

# OpenAI API 인증 정보
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def validate_config():
    """필수 환경 변수 검증"""
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        raise ValueError(
            "네이버 API 인증 정보가 설정되지 않았습니다.\n"
            ".env 파일을 생성하고 NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET을 설정하세요."
        )
    return True

def validate_openai_config():
    """OpenAI API 환경 변수 검증"""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OpenAI API 키가 설정되지 않았습니다.\n"
            ".env 파일에 OPENAI_API_KEY를 설정하세요."
        )
    return True
