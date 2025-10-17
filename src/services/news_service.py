"""뉴스 검색 비즈니스 로직"""
from typing import List, Dict
from src.api.naver_news_api import NaverNewsAPI
from src.utils.formatter import format_news_list
from src.utils.deduplicator import NewsDeduplicator


class NewsService:
    """뉴스 검색 및 처리 서비스"""

    def __init__(self):
        self.api = NaverNewsAPI()
        self.deduplicator = NewsDeduplicator()

    def search_and_format(
        self,
        query: str,
        count: int = 10,
        sort: str = "date",
        remove_duplicates: bool = True,
        similarity_threshold: float = 0.7
    ) -> List[Dict]:
        """
        뉴스 검색 및 포맷팅 (중복 제거 포함)

        Args:
            query: 검색 키워드
            count: 가져올 뉴스 개수 (중복 제거 후 목표 개수)
            sort: 정렬 방식 (date: 날짜순, sim: 정확도순)
            remove_duplicates: 중복 제거 여부
            similarity_threshold: 유사도 임계값 (0.0 ~ 1.0)

        Returns:
            포맷팅된 뉴스 리스트
        """
        if not remove_duplicates:
            # 중복 제거 없이 바로 반환
            result = self.api.search_news(query, display=count, sort=sort)
            items = result.get('items', [])
            return format_news_list(items)

        # 중복 제거를 위해 더 많은 뉴스를 가져옴
        all_news = []
        start = 1
        max_fetch = count * 3  # 최대 목표 개수의 3배까지 수집
        batch_size = min(100, count * 2)  # 한 번에 가져올 개수

        while len(all_news) < max_fetch:
            # API 호출
            result = self.api.search_news(
                query,
                display=batch_size,
                start=start,
                sort=sort
            )
            items = result.get('items', [])

            if not items:
                break

            # 포맷팅 후 추가
            formatted_items = format_news_list(items)
            all_news.extend(formatted_items)

            # 중복 제거 후 개수 확인
            unique_news = self.deduplicator.remove_duplicates(
                all_news,
                similarity_threshold
            )

            # 목표 개수 달성 시 종료
            if len(unique_news) >= count:
                return unique_news[:count]

            # 다음 페이지
            start += batch_size

            # 더 이상 가져올 뉴스가 없으면 종료
            if len(items) < batch_size:
                break

        # 중복 제거 후 반환
        unique_news = self.deduplicator.remove_duplicates(
            all_news,
            similarity_threshold
        )

        return unique_news[:count]

    def get_news_summary(self, query: str, count: int = 5) -> Dict:
        """
        뉴스 요약 정보 반환

        Args:
            query: 검색 키워드
            count: 가져올 뉴스 개수

        Returns:
            요약 정보 딕셔너리
        """
        news_list = self.search_and_format(query, count)

        return {
            'query': query,
            'total_count': len(news_list),
            'news_list': news_list
        }
