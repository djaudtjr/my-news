# 프로젝트 구조

## 📂 폴더 구조

```
my-news/
├── src/
│   ├── api/                  # 외부 API 연동 모듈
│   │   ├── naver_news_api.py
│   │   └── openai_api.py
│   ├── services/             # 비즈니스 로직 계층
│   │   ├── news_service.py
│   │   ├── summary_service.py
│   │   └── ai_summary_service.py
│   └── utils/                # 유틸리티 함수
│       ├── config.py
│       ├── formatter.py
│       └── crawler.py
├── app.py                    # Streamlit 애플리케이션 진입점
├── requirements.txt          # Python 의존성
├── .env.example              # 환경변수 템플릿
├── .gitignore                # Git 제외 파일
├── README.md                 # 프로젝트 문서
├── CLAUDE.md                 # Claude Code 가이드
├── DEV_GUIDE.md              # 개발 가이드
├── STRUCTURE.md              # 프로젝트 구조 (현재 파일)
├── DEPENDENCIES.md           # 의존성 관계
└── CHANGELOG.md              # 개발 변경 이력
```

## 📄 파일별 역할

### src/api/naver_news_api.py
- **역할**: 네이버 뉴스 검색 API와의 통신을 담당하는 클라이언트
- **주요 export**: `NaverNewsAPI` 클래스
- **의존성**: `requests`, `config`
- **상태**: ✅ 최적 구조
- **설명**: API 호출, 인증, 에러 처리를 캡슐화

### src/services/news_service.py
- **역할**: 뉴스 검색 비즈니스 로직 처리
- **주요 export**: `NewsService` 클래스
- **의존성**: `NaverNewsAPI`, `formatter`
- **상태**: ✅ 최적 구조
- **설명**: API와 UI 사이의 중간 계층, 데이터 변환 및 가공

### src/services/summary_service.py
- **역할**: 뉴스 요약 생성 및 키워드 추출
- **주요 export**: `SummaryService` 클래스
- **의존성**: 없음 (독립적)
- **상태**: ✅ 최적 구조
- **설명**: 텍스트 요약 및 분석 기능 제공

### src/api/openai_api.py
- **역할**: OpenAI API 클라이언트
- **주요 export**: `OpenAIClient` 클래스
- **의존성**: `openai`, `config`
- **상태**: ✅ 최적 구조
- **설명**: AI 텍스트 요약 및 분석 API 연동

### src/services/ai_summary_service.py
- **역할**: AI 기반 뉴스 요약 통합 서비스
- **주요 export**: `AISummaryService` 클래스
- **의존성**: `NewsCrawler`, `OpenAIClient`
- **상태**: ✅ 최적 구조
- **설명**: 크롤링과 AI 요약을 결합한 고급 요약 기능

### src/utils/config.py
- **역할**: 환경 변수 로드 및 검증
- **주요 export**: `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET`, `OPENAI_API_KEY`, `validate_config()`, `validate_openai_config()`
- **의존성**: `dotenv`
- **상태**: ✅ 최적 구조
- **설명**: 설정 관리 중앙화

### src/utils/formatter.py
- **역할**: 데이터 포맷팅 및 정제
- **주요 export**: `remove_html_tags()`, `format_news_item()`, `format_news_list()`
- **의존성**: `re`
- **상태**: ✅ 최적 구조
- **설명**: HTML 태그 제거, 데이터 정규화

### src/utils/crawler.py
- **역할**: 뉴스 웹페이지 크롤링
- **주요 export**: `NewsCrawler` 클래스
- **의존성**: `requests`, `BeautifulSoup`
- **상태**: ✅ 최적 구조
- **설명**: 뉴스 기사 본문 추출

### app.py
- **역할**: Streamlit UI 및 사용자 인터랙션 처리
- **주요 export**: `main()` 함수
- **의존성**: `streamlit`, `NewsService`, `SummaryService`, `AISummaryService`, `config`
- **상태**: ✅ 최적 구조
- **설명**: 애플리케이션 진입점, UI 레이아웃 및 이벤트 처리

## 🔍 구조 품질 체크

- ✅ **단일 책임 준수**: 각 파일이 명확한 단일 역할을 수행
- ✅ **재사용성**: API, 서비스, 유틸리티가 독립적으로 재사용 가능
- ✅ **응집도**: 관련 기능이 적절히 그룹화됨
  - API 계층: `src/api/`
  - 비즈니스 로직: `src/services/`
  - 유틸리티: `src/utils/`
- ✅ **결합도**: 낮은 결합도로 유지보수 용이
- ✅ **확장성**: 웹 애플리케이션으로 전환 시 `app.py`만 교체하면 됨

## 💡 개선 제안

현재 구조는 단일 책임 원칙을 잘 따르고 있으며, AI 요약 기능이 추가되었습니다.

향후 확장 시:
- 데이터베이스 연동: `src/db/` 디렉토리 추가 (뉴스 저장/북마크)
- 웹 API 전환: `src/routes/`, `src/controllers/` 추가
- 캐싱 시스템: 크롤링 결과 및 AI 요약 캐싱으로 비용 절감
