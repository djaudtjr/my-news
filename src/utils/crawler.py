"""뉴스 웹페이지 크롤링 모듈"""
import requests
from bs4 import BeautifulSoup
from typing import Optional
import time


class NewsCrawler:
    """뉴스 전문 크롤링 클래스"""

    # 다양한 User-Agent 목록
    USER_AGENTS = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    ]

    @staticmethod
    def fetch_article_content(url: str, retry_count: int = 2) -> Optional[str]:
        """
        뉴스 페이지에서 본문 추출 (재시도 로직 포함)

        Args:
            url: 뉴스 기사 URL
            retry_count: 재시도 횟수

        Returns:
            뉴스 본문 텍스트 (실패 시 None)
        """
        for attempt in range(retry_count + 1):
            try:
                # User-Agent 로테이션
                headers = {
                    'User-Agent': NewsCrawler.USER_AGENTS[attempt % len(NewsCrawler.USER_AGENTS)],
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }

                response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
                response.raise_for_status()
                response.encoding = response.apparent_encoding

                soup = BeautifulSoup(response.text, 'html.parser')

                article = None

                # 네이버 뉴스 본문 추출 (여러 가지 선택자 시도)
                if 'news.naver.com' in url:
                    # 최신 네이버 뉴스
                    article = soup.find('article', {'id': 'dic_area'})
                    if not article:
                        article = soup.find('div', {'id': 'articleBodyContents'})
                    if not article:
                        article = soup.find('div', {'class': 'article_body'})
                    if not article:
                        article = soup.find('div', {'class': 'article_viewer'})
                    if not article:
                        # 엔터 뉴스
                        article = soup.find('div', {'id': 'articeBody'})
                else:
                    # 일반 뉴스 사이트
                    article = (
                        soup.find('article', {'class': lambda x: x and 'article' in x.lower()}) or
                        soup.find('div', {'class': lambda x: x and any(kw in x.lower() for kw in ['article', 'content', 'body', 'post'])}) or
                        soup.find('article') or
                        soup.find('div', {'id': lambda x: x and any(kw in x.lower() for kw in ['article', 'content', 'main'])})
                    )

                if article:
                    # 불필요한 태그 제거
                    for tag in article.find_all(['script', 'style', 'aside', 'nav', 'footer', 'iframe', 'form', 'button']):
                        tag.decompose()

                    # 광고, 관련기사 등 제거
                    for tag in article.find_all(['div', 'section'], {'class': lambda x: x and any(kw in str(x).lower() for kw in ['ad', 'banner', 'related', 'recommend'])}):
                        tag.decompose()

                    # 텍스트 추출 및 정제
                    text = article.get_text(separator='\n', strip=True)
                    # 빈 줄과 짧은 줄 제거
                    lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 10]
                    full_text = '\n'.join(lines)

                    # 최소 길이 체크
                    if len(full_text) >= 100:
                        print(f"✓ 크롤링 성공: {len(full_text)}자 추출 - {url[:50]}...")
                        return full_text
                    else:
                        print(f"본문 길이 부족: {len(full_text)}자 (재시도 {attempt + 1}/{retry_count + 1}) - {url[:50]}...")

                # 본문을 찾지 못한 경우
                if attempt < retry_count:
                    print(f"본문 요소를 찾을 수 없음 (재시도 {attempt + 1}/{retry_count + 1}) - {url[:50]}...")
                    time.sleep(1)  # 재시도 전 대기
                    continue
                else:
                    print(f"✗ 크롤링 최종 실패: 본문 요소를 찾을 수 없음 - {url[:50]}...")
                    # 마지막 시도로 전체 body 텍스트 추출
                    body = soup.find('body')
                    if body:
                        text = body.get_text(separator='\n', strip=True)
                        lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 20]
                        full_text = '\n'.join(lines)
                        if len(full_text) >= 100:
                            print(f"⚠ body 전체에서 추출: {len(full_text)}자 - {url[:50]}...")
                            return full_text
                    return None

            except requests.exceptions.Timeout:
                print(f"타임아웃 (재시도 {attempt + 1}/{retry_count + 1}) - {url[:50]}...")
                if attempt < retry_count:
                    time.sleep(2)
                    continue
            except requests.exceptions.RequestException as e:
                print(f"네트워크 오류 (재시도 {attempt + 1}/{retry_count + 1}): {str(e)} - {url[:50]}...")
                if attempt < retry_count:
                    time.sleep(2)
                    continue
            except Exception as e:
                print(f"크롤링 오류 (재시도 {attempt + 1}/{retry_count + 1}): {str(e)} - {url[:50]}...")
                if attempt < retry_count:
                    time.sleep(1)
                    continue

        print(f"✗ 최종 실패: 모든 재시도 소진 - {url[:50]}...")
        return None

    @staticmethod
    def get_article_summary_info(url: str) -> dict:
        """
        뉴스 페이지에서 본문과 메타 정보 추출

        Args:
            url: 뉴스 기사 URL

        Returns:
            본문과 메타 정보를 포함한 딕셔너리
        """
        content = NewsCrawler.fetch_article_content(url)

        return {
            'url': url,
            'content': content,
            'success': content is not None,
            'word_count': len(content) if content else 0
        }
