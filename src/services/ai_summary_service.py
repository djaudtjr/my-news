"""AI 기반 뉴스 요약 서비스"""
from typing import Optional, Dict
from src.utils.crawler import NewsCrawler
from src.api.openai_api import OpenAIClient


class AISummaryService:
    """AI 기반 뉴스 요약 서비스"""

    def __init__(self):
        self.crawler = NewsCrawler()
        self.ai_client = OpenAIClient()

    def summarize_news_from_url(self, url: str) -> Dict:
        """
        URL에서 뉴스를 가져와 AI로 요약

        Args:
            url: 뉴스 기사 URL

        Returns:
            요약 정보 딕셔너리
        """
        try:
            # 1. 뉴스 전문 크롤링
            article_info = self.crawler.get_article_summary_info(url)

            if not article_info['success']:
                error_msg = f"크롤링 실패 - URL: {url[:50]}..."
                print(error_msg)
                return {
                    'success': False,
                    'error': '뉴스 본문을 가져올 수 없습니다. (크롤링 실패)',
                    'url': url
                }

            content = article_info['content']

            # 본문이 너무 짧은 경우
            if len(content) < 100:
                error_msg = f"본문 길이 부족: {len(content)}자 - URL: {url[:50]}..."
                print(error_msg)
                return {
                    'success': False,
                    'error': f'뉴스 본문이 너무 짧습니다. (추출된 텍스트: {len(content)}자)',
                    'url': url,
                    'content': content
                }

            # 2. AI 요약 생성
            summary_result = self.ai_client.summarize_with_key_points(content)

            if not summary_result:
                error_msg = f"AI 요약 실패 - URL: {url[:50]}..."
                print(error_msg)
                return {
                    'success': False,
                    'error': 'AI 요약 생성에 실패했습니다.',
                    'url': url,
                    'content': content
                }

            # 3. 결과 반환
            return {
                'success': True,
                'url': url,
                'original_content': content,
                'word_count': article_info['word_count'],
                'summary': summary_result['summary'],
                'key_points': summary_result['key_points']
            }

        except Exception as e:
            error_msg = f"예외 발생 - {str(e)} - URL: {url[:50]}..."
            print(error_msg)
            return {
                'success': False,
                'error': f'처리 중 오류 발생: {str(e)}',
                'url': url
            }

    def get_simple_summary(self, url: str, max_length: int = 300) -> Optional[str]:
        """
        URL에서 간단한 요약만 생성

        Args:
            url: 뉴스 기사 URL
            max_length: 요약 최대 길이

        Returns:
            요약 텍스트 (실패 시 None)
        """
        article_info = self.crawler.get_article_summary_info(url)

        if not article_info['success']:
            return None

        return self.ai_client.summarize_text(
            article_info['content'],
            max_length=max_length
        )
