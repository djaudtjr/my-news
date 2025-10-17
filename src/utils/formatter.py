"""데이터 포맷팅 유틸리티"""
import re
from typing import Dict, List


def remove_html_tags(text: str) -> str:
    """HTML 태그 제거"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def format_news_item(item: Dict) -> Dict:
    """
    뉴스 항목 포맷팅

    Args:
        item: 원본 뉴스 항목

    Returns:
        포맷팅된 뉴스 항목
    """
    return {
        'title': remove_html_tags(item.get('title', '')),
        'description': remove_html_tags(item.get('description', '')),
        'link': item.get('link', ''),
        'originallink': item.get('originallink', ''),
        'pubDate': item.get('pubDate', '')
    }


def format_news_list(items: List[Dict]) -> List[Dict]:
    """
    뉴스 항목 리스트 포맷팅

    Args:
        items: 원본 뉴스 항목 리스트

    Returns:
        포맷팅된 뉴스 항목 리스트
    """
    return [format_news_item(item) for item in items]
