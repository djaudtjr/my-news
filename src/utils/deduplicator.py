"""뉴스 중복 제거 유틸리티"""
from typing import List, Dict
from difflib import SequenceMatcher


class NewsDeduplicator:
    """뉴스 중복 제거 클래스"""

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        두 텍스트의 유사도 계산

        Args:
            text1: 첫 번째 텍스트
            text2: 두 번째 텍스트

        Returns:
            유사도 (0.0 ~ 1.0)
        """
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    @staticmethod
    def are_similar_news(news1: Dict, news2: Dict, threshold: float = 0.7) -> bool:
        """
        두 뉴스가 유사한지 판단

        Args:
            news1: 첫 번째 뉴스
            news2: 두 번째 뉴스
            threshold: 유사도 임계값 (기본값: 0.7)

        Returns:
            유사 여부
        """
        # 제목 유사도 체크
        title_similarity = NewsDeduplicator.calculate_similarity(
            news1.get('title', ''),
            news2.get('title', '')
        )

        # 설명 유사도 체크
        desc_similarity = NewsDeduplicator.calculate_similarity(
            news1.get('description', ''),
            news2.get('description', '')
        )

        # 제목이나 설명 중 하나라도 임계값 이상이면 유사한 뉴스로 판단
        return title_similarity >= threshold or desc_similarity >= threshold

    @staticmethod
    def parse_pub_date(pub_date_str: str) -> int:
        """
        발행일 문자열을 타임스탬프로 변환

        Args:
            pub_date_str: 발행일 문자열 (예: "Mon, 16 Oct 2023 10:30:00 +0900")

        Returns:
            Unix timestamp (초)
        """
        from datetime import datetime
        import email.utils

        try:
            # RFC 2822 형식 파싱
            time_tuple = email.utils.parsedate_to_datetime(pub_date_str)
            return int(time_tuple.timestamp())
        except Exception:
            # 파싱 실패 시 현재 시간 반환
            return int(datetime.now().timestamp())

    @staticmethod
    def remove_duplicates(news_list: List[Dict], similarity_threshold: float = 0.7) -> List[Dict]:
        """
        중복 뉴스 제거 (최신 뉴스 우선)

        Args:
            news_list: 뉴스 리스트
            similarity_threshold: 유사도 임계값

        Returns:
            중복 제거된 뉴스 리스트
        """
        if not news_list:
            return []

        # 발행일 기준으로 정렬 (최신순)
        sorted_news = sorted(
            news_list,
            key=lambda x: NewsDeduplicator.parse_pub_date(x.get('pubDate', '')),
            reverse=True
        )

        unique_news = []
        for news in sorted_news:
            # 기존 리스트에 유사한 뉴스가 있는지 확인
            is_duplicate = False
            for unique in unique_news:
                if NewsDeduplicator.are_similar_news(news, unique, similarity_threshold):
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_news.append(news)

        return unique_news

    @staticmethod
    def get_duplicate_count(news_list: List[Dict], similarity_threshold: float = 0.7) -> int:
        """
        중복된 뉴스 개수 계산

        Args:
            news_list: 뉴스 리스트
            similarity_threshold: 유사도 임계값

        Returns:
            중복 개수
        """
        unique_list = NewsDeduplicator.remove_duplicates(news_list, similarity_threshold)
        return len(news_list) - len(unique_list)
