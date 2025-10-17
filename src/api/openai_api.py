"""OpenAI API 연동 모듈"""
from openai import OpenAI
from typing import Optional
from src.utils.config import OPENAI_API_KEY


class OpenAIClient:
    """OpenAI API 클라이언트"""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-4o-mini"  # 비용 효율적인 모델

    def summarize_text(
        self,
        text: str,
        max_length: int = 300,
        language: str = "Korean"
    ) -> Optional[str]:
        """
        텍스트 요약 생성

        Args:
            text: 요약할 텍스트
            max_length: 요약 최대 길이 (문자 수)
            language: 요약 언어

        Returns:
            요약된 텍스트 (실패 시 None)
        """
        try:
            system_prompt = f"""당신은 뉴스 기사를 요약하는 전문가입니다.
다음 규칙을 따라 요약해주세요:
1. 핵심 내용만 간결하게 요약
2. 중요한 사실과 수치 포함
3. 객관적이고 중립적인 톤 유지
4. {max_length}자 이내로 작성
5. {language}로 작성"""

            user_prompt = f"다음 뉴스 기사를 요약해주세요:\n\n{text}"

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"OpenAI API 오류: {str(e)}")
            return None

    def summarize_with_key_points(self, text: str) -> Optional[dict]:
        """
        텍스트 요약 및 핵심 포인트 추출

        Args:
            text: 요약할 텍스트

        Returns:
            요약과 핵심 포인트를 포함한 딕셔너리
        """
        try:
            system_prompt = """당신은 뉴스 기사를 분석하는 전문가입니다.
다음 형식으로 응답해주세요:

[요약]
(3-5문장으로 핵심 내용 요약)

[핵심 포인트]
- (핵심 포인트 1)
- (핵심 포인트 2)
- (핵심 포인트 3)"""

            user_prompt = f"다음 뉴스 기사를 분석해주세요:\n\n{text}"

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )

            content = response.choices[0].message.content.strip()

            # 응답 파싱
            parts = content.split('[핵심 포인트]')
            summary = parts[0].replace('[요약]', '').strip()
            key_points = []

            if len(parts) > 1:
                points_text = parts[1].strip()
                key_points = [
                    line.strip('- ').strip()
                    for line in points_text.split('\n')
                    if line.strip().startswith('-')
                ]

            return {
                'summary': summary,
                'key_points': key_points
            }

        except Exception as e:
            print(f"OpenAI API 오류: {str(e)}")
            return None
