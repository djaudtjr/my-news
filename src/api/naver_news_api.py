"""네이버 뉴스 검색 API 연동 모듈"""
import requests
from typing import Dict, List, Optional
from src.utils.config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET


class NaverNewsAPI:
    """네이버 뉴스 검색 API 클라이언트"""

    BASE_URL = "https://openapi.naver.com/v1/search/news.json"

    def __init__(self):
        self.client_id = NAVER_CLIENT_ID
        self.client_secret = NAVER_CLIENT_SECRET
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

    def search_news(
        self,
        query: str,
        display: int = 10,
        start: int = 1,
        sort: str = "date"
    ) -> Dict:
        """
        뉴스 검색

        Args:
            query: 검색 키워드
            display: 한 번에 표시할 검색 결과 개수 (10~100, 기본값: 10)
            start: 검색 시작 위치 (1~1000, 기본값: 1)
            sort: 정렬 방식 (date: 날짜순, sim: 정확도순, 기본값: date)

        Returns:
            검색 결과 딕셔너리
        """
        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": sort
        }

        try:
            response = requests.get(
                self.BASE_URL,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"네이버 뉴스 API 요청 실패: {str(e)}")

    def get_news_items(self, query: str, count: int = 10) -> List[Dict]:
        """
        뉴스 항목 리스트 반환

        Args:
            query: 검색 키워드
            count: 가져올 뉴스 개수

        Returns:
            뉴스 항목 리스트
        """
        result = self.search_news(query, display=count)
        return result.get('items', [])
