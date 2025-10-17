"""뉴스 요약 처리 서비스"""
from typing import Dict, List


class SummaryService:
    """뉴스 요약 생성 서비스"""

    @staticmethod
    def create_simple_summary(news_item: Dict) -> str:
        """
        단순 요약 생성 (description 기반)

        Args:
            news_item: 뉴스 항목

        Returns:
            요약 텍스트
        """
        description = news_item.get('description', '')
        # 첫 100자만 추출
        return description[:100] + '...' if len(description) > 100 else description

    @staticmethod
    def create_summary_list(news_items: List[Dict]) -> List[Dict]:
        """
        뉴스 리스트의 요약 생성

        Args:
            news_items: 뉴스 항목 리스트

        Returns:
            요약이 포함된 뉴스 항목 리스트
        """
        result = []
        for item in news_items:
            summary_item = item.copy()
            summary_item['summary'] = SummaryService.create_simple_summary(item)
            result.append(summary_item)
        return result

    @staticmethod
    def get_keywords_from_titles(news_items: List[Dict]) -> List[str]:
        """
        뉴스 제목에서 자주 나오는 키워드 추출 (간단한 구현)

        Args:
            news_items: 뉴스 항목 리스트

        Returns:
            키워드 리스트
        """
        # 제목들을 합쳐서 단어로 분리
        all_words = []
        for item in news_items:
            title = item.get('title', '')
            words = title.split()
            all_words.extend(words)

        # 단어 빈도 계산 (간단한 구현)
        word_count = {}
        for word in all_words:
            if len(word) > 1:  # 한 글자는 제외
                word_count[word] = word_count.get(word, 0) + 1

        # 빈도순 정렬하여 상위 5개 반환
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:5]]
