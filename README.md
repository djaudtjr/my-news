# 📰 네이버 뉴스 검색 & 요약

네이버 뉴스 검색 API를 활용한 뉴스 검색 및 요약 애플리케이션입니다.

## 🚀 주요 기능

- ✅ 키워드 기반 네이버 뉴스 검색
- ✅ 뉴스 제목, 요약, 링크 정보 제공
- ✅ 날짜순/정확도순 정렬
- ✅ 주요 키워드 자동 추출
- ✅ Streamlit 기반 직관적인 UI

## 📋 사전 준비

### 1. 네이버 검색 API 인증 정보 발급

1. [네이버 개발자 센터](https://developers.naver.com/)에 로그인
2. [애플리케이션 등록](https://developers.naver.com/apps/#/register)
   - 애플리케이션 이름: 원하는 이름 입력
   - 사용 API: **검색** 선택
3. **Client ID**와 **Client Secret** 발급 받기

### 2. Python 환경

- Python 3.8 이상 필요

## 🛠️ 설치 및 실행

### 1. 저장소 클론 (또는 다운로드)

```bash
cd my-news
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일 생성:

```bash
cp .env.example .env
```

`.env` 파일을 열어 네이버 API 인증 정보 입력:

```env
NAVER_CLIENT_ID=발급받은_클라이언트_ID
NAVER_CLIENT_SECRET=발급받은_클라이언트_시크릿
```

### 4. 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저에서 자동으로 `http://localhost:8501` 열림

## 📁 프로젝트 구조

```
my-news/
├── src/
│   ├── api/
│   │   └── naver_news_api.py      # 네이버 뉴스 API 클라이언트
│   ├── services/
│   │   ├── news_service.py        # 뉴스 검색 비즈니스 로직
│   │   └── summary_service.py     # 뉴스 요약 처리
│   └── utils/
│       ├── config.py              # 환경 설정 관리
│       └── formatter.py           # 데이터 포맷팅
├── app.py                         # Streamlit 메인 애플리케이션
├── requirements.txt               # Python 의존성
├── .env.example                   # 환경변수 예시
└── README.md
```

## 🎯 사용 방법

1. **검색 키워드 입력**: 왼쪽 사이드바에서 검색할 뉴스 키워드 입력
2. **결과 개수 선택**: 5~100개 사이에서 원하는 뉴스 개수 선택
3. **정렬 방식 선택**:
   - **날짜순**: 최신 뉴스부터 표시
   - **정확도순**: 검색어와 관련성이 높은 순서대로 표시
4. **검색 버튼 클릭**: 뉴스 검색 시작

## 🔧 향후 개발 계획

- [ ] 웹 애플리케이션으로 전환 (Express + React/Vue)
- [ ] 뉴스 저장 및 북마크 기능
- [ ] AI 기반 뉴스 요약 강화
- [ ] 뉴스 카테고리 필터링
- [ ] 데이터 시각화 (차트, 그래프)

## 📄 라이선스

MIT License

## 🤝 기여

이슈와 PR은 언제나 환영합니다!
