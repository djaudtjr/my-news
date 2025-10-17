"""네이버 뉴스 검색 Streamlit 애플리케이션"""
import streamlit as st
from src.utils.config import validate_config, validate_openai_config
from src.services.news_service import NewsService
from src.services.summary_service import SummaryService
from src.services.ai_summary_service import AISummaryService


# 페이지 설정
st.set_page_config(
    page_title="네이버 뉴스 검색",
    page_icon="📰",
    layout="wide"
)


def main():
    """메인 애플리케이션"""

    st.title("📰 네이버 뉴스 검색 & 요약")
    st.markdown("---")

    # 환경 변수 검증
    try:
        validate_config()
    except ValueError as e:
        st.error(str(e))
        st.info(
            "1. `.env.example` 파일을 복사하여 `.env` 파일을 생성하세요.\n"
            "2. https://developers.naver.com/apps 에서 API 키를 발급받으세요.\n"
            "3. `.env` 파일에 `NAVER_CLIENT_ID`와 `NAVER_CLIENT_SECRET`을 설정하세요."
        )
        return

    # 사이드바 설정
    with st.sidebar:
        st.header("⚙️ 검색 설정")

        # 폼으로 감싸서 엔터키 입력 지원
        with st.form(key="search_form"):
            # 검색 키워드 입력
            query = st.text_input(
                "검색 키워드",
                placeholder="예: 인공지능, 주식시장",
                help="검색하고 싶은 뉴스 키워드를 입력하세요 (엔터키로 검색)"
            )

            # 결과 개수 선택
            count = st.slider(
                "결과 개수",
                min_value=5,
                max_value=20,
                value=10,
                step=5,
                help="가져올 뉴스 개수"
            )

            # 정렬 방식 선택
            sort_option = st.radio(
                "정렬 방식",
                options=["날짜순", "정확도순"],
                help="뉴스 정렬 기준"
            )
            sort = "date" if sort_option == "날짜순" else "sim"

            # 검색 버튼 (폼 제출 버튼)
            search_button = st.form_submit_button("🔍 검색", type="primary", use_container_width=True)

    # 메인 컨텐츠 영역
    if search_button:
        if not query:
            st.warning("검색 키워드를 입력해주세요.")
            return

        # 새로운 검색 시 초기화
        keys_to_clear = [key for key in st.session_state.keys() if key.startswith('ai_result_')]
        for key in keys_to_clear:
            del st.session_state[key]

        # 페이지네이션 초기화
        st.session_state['query'] = query
        st.session_state['count'] = count
        st.session_state['sort'] = sort
        st.session_state['page'] = 0
        st.session_state['summarized_count'] = 0

        with st.spinner(f"'{query}' 관련 뉴스를 검색 중 (중복 제거 포함)..."):
            try:
                # 뉴스 검색 (중복 제거 포함)
                news_service = NewsService()
                news_list = news_service.search_and_format(
                    query,
                    count,
                    sort,
                    remove_duplicates=True,
                    similarity_threshold=0.7
                )

                if not news_list:
                    st.info("검색 결과가 없습니다.")
                    return

                # 요약 정보 생성
                summary_service = SummaryService()
                news_with_summary = summary_service.create_summary_list(news_list)
                keywords = summary_service.get_keywords_from_titles(news_list)

                # 세션 상태에 검색 결과 저장
                st.session_state['news_list'] = news_with_summary  # 누적된 뉴스 리스트
                st.session_state['keywords'] = keywords
                st.session_state['requested_count'] = count
                st.session_state['auto_summarize'] = True  # AI 요약 자동 실행 플래그

            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
                st.info("API 인증 정보가 올바른지 확인해주세요.")
                return

    # 검색 결과 표시 (세션 상태에서 가져오기)
    if 'news_list' in st.session_state and st.session_state['news_list']:
        news_with_summary = st.session_state['news_list']
        keywords = st.session_state.get('keywords', [])

        # 결과 표시
        st.success(f"총 {len(news_with_summary)}개의 뉴스를 불러왔습니다.")

        # 키워드 태그
        if keywords:
            st.markdown("### 🏷️ 주요 키워드")
            keyword_html = " ".join([
                f'<span style="background-color: #e3f2fd; color: #1565c0; padding: 5px 10px; '
                f'border-radius: 15px; margin: 5px; display: inline-block; font-weight: 500;">{kw}</span>'
                for kw in keywords
            ])
            st.markdown(keyword_html, unsafe_allow_html=True)
            st.markdown("---")

        # 자동 AI 요약 실행 (새로 추가된 뉴스만)
        if st.session_state.get('auto_summarize', False):
            st.session_state['auto_summarize'] = False

            try:
                validate_openai_config()
                ai_service = AISummaryService()

                # 이미 AI 요약이 완료된 뉴스 개수 확인
                summarized_count = st.session_state.get('summarized_count', 0)

                # 새로 추가된 뉴스만 처리
                new_news = news_with_summary[summarized_count:]

                if new_news:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    success_count = 0
                    fail_count = 0

                    for idx, news in enumerate(new_news, 1):
                        global_idx = summarized_count + idx
                        status_text.text(f"AI 요약 진행 중... ({idx}/{len(new_news)})")
                        progress_bar.progress(idx / len(new_news))

                        # 원본 링크 우선, 없으면 네이버 뉴스 링크 사용
                        article_url = news.get('originallink') or news.get('link')

                        if article_url:
                            try:
                                result = ai_service.summarize_news_from_url(article_url)
                                if result.get('success'):
                                    st.session_state[f'ai_result_{global_idx}'] = result
                                    success_count += 1
                                else:
                                    # 실패 정보 저장
                                    st.session_state[f'ai_result_{global_idx}'] = {
                                        'success': False,
                                        'error': result.get('error', '알 수 없는 오류'),
                                        'url': article_url
                                    }
                                    fail_count += 1
                            except Exception as e:
                                st.session_state[f'ai_result_{global_idx}'] = {
                                    'success': False,
                                    'error': str(e),
                                    'url': article_url
                                }
                                fail_count += 1

                    progress_bar.empty()
                    status_text.empty()

                    # 요약 완료된 개수 업데이트
                    st.session_state['summarized_count'] = len(news_with_summary)

                    # 결과 메시지
                    if fail_count > 0:
                        st.info(f"✅ AI 요약 완료: {success_count}개 성공, {fail_count}개 실패")
                    else:
                        st.success(f"✅ {success_count}개의 뉴스 AI 요약 완료")

                    st.rerun()

            except ValueError:
                st.warning("⚠️ OpenAI API 키가 설정되지 않아 기본 요약만 표시됩니다.")
                st.info("AI 요약을 사용하려면 `.env` 파일에 OPENAI_API_KEY를 설정해주세요.")
            except Exception as e:
                st.error(f"AI 요약 중 오류 발생: {str(e)}")

        # 뉴스 목록 표시
        st.markdown("### 📋 뉴스 목록")

        for idx, news in enumerate(news_with_summary, 1):
            with st.expander(f"**{idx}. {news['title']}**", expanded=(idx == 1)):
                # 발행일
                st.caption(f"📅 {news['pubDate']}")

                # 요약 표시 (AI 요약이 있으면 AI 요약, 없으면 기본 요약)
                ai_summary_data = st.session_state.get(f'ai_result_{idx}')

                # 타입 체크 및 검증
                if isinstance(ai_summary_data, dict) and ai_summary_data.get('success') and 'summary' in ai_summary_data:
                    # AI 요약 표시
                    st.markdown("**🤖 AI 요약**")
                    st.info(ai_summary_data['summary'])

                    # 핵심 포인트
                    if ai_summary_data.get('key_points'):
                        st.markdown("**💡 핵심 포인트**")
                        for point in ai_summary_data['key_points']:
                            st.markdown(f"- {point}")

                    # 통계
                    st.caption(f"📊 원문 길이: {ai_summary_data.get('word_count', 0):,}자")
                elif isinstance(ai_summary_data, dict) and not ai_summary_data.get('success'):
                    # AI 요약 실패 시
                    st.markdown("**📝 기본 요약**")
                    st.write(news.get('summary', news.get('description', '')))
                    st.caption(f"⚠️ AI 요약 실패: {ai_summary_data.get('error', '알 수 없는 오류')}")
                else:
                    # 기본 요약 표시
                    st.markdown("**📝 요약**")
                    st.write(news.get('summary', news.get('description', '')))

                # 원본 기사 링크만 표시
                if news.get('originallink'):
                    st.markdown(f"[🔗 원본 기사 보기]({news['originallink']})")

        # 다음 페이지 버튼
        st.markdown("---")
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            if st.button("➡️ 다음 페이지", type="primary", use_container_width=True):
                # 다음 페이지 로드
                query = st.session_state.get('query', '')
                count = st.session_state.get('count', 10)
                sort = st.session_state.get('sort', 'date')
                current_page = st.session_state.get('page', 0)

                with st.spinner(f"다음 {count}개의 뉴스를 검색 중..."):
                    try:
                        news_service = NewsService()
                        # 다음 페이지 시작 위치 계산
                        start_pos = (current_page + 1) * count + 1

                        # API 호출로 다음 페이지 뉴스 가져오기
                        result = news_service.api.search_news(
                            query,
                            display=count * 2,  # 중복 제거를 고려해 더 많이 가져옴
                            start=start_pos,
                            sort=sort
                        )
                        items = result.get('items', [])

                        if items:
                            from src.utils.formatter import format_news_list
                            formatted_items = format_news_list(items)

                            # 중복 제거
                            from src.utils.deduplicator import NewsDeduplicator
                            deduplicator = NewsDeduplicator()

                            # 기존 뉴스와 새 뉴스를 합쳐서 중복 제거
                            combined_news = st.session_state['news_list'] + formatted_items
                            unique_news = deduplicator.remove_duplicates(combined_news, 0.7)

                            # 새로 추가된 뉴스만 추출
                            new_news_count = len(unique_news) - len(st.session_state['news_list'])

                            if new_news_count > 0:
                                summary_service = SummaryService()
                                news_with_summary = summary_service.create_summary_list(unique_news)

                                # 누적해서 저장
                                st.session_state['news_list'] = news_with_summary
                                st.session_state['page'] += 1
                                st.session_state['auto_summarize'] = True
                                st.rerun()
                            else:
                                st.info("중복 제거 후 새로운 뉴스가 없습니다.")
                        else:
                            st.info("더 이상 검색 결과가 없습니다.")
                    except Exception as e:
                        st.error(f"오류가 발생했습니다: {str(e)}")

    else:
        # 초기 화면
        st.info("👈 왼쪽 사이드바에서 검색 키워드를 입력하고 검색 버튼을 클릭하세요.")

        # 사용 가이드
        with st.expander("📖 사용 가이드"):
            st.markdown("""
            ### 사용 방법
            1. **검색 키워드 입력**: 관심 있는 뉴스 주제를 입력하세요
            2. **결과 개수 선택**: 5~100개 사이에서 선택 가능합니다
            3. **정렬 방식 선택**:
               - 날짜순: 최신 뉴스부터 표시
               - 정확도순: 검색어와 관련성이 높은 순서대로 표시
            4. **검색 버튼 클릭**: 뉴스 검색 시작

            ### 기능
            - 🏷️ **주요 키워드**: 뉴스 제목에서 자주 등장하는 키워드를 추출
            - 📝 **요약**: 각 뉴스의 핵심 내용을 요약하여 표시
            - 🔗 **링크**: 네이버 뉴스와 원본 기사 링크 제공
            - 🤖 **AI 요약**: OpenAI를 활용한 기사 전문 분석 및 상세 요약
              - 기사 원문을 크롤링하여 전체 내용 분석
              - 핵심 내용 요약 및 주요 포인트 추출
              - OpenAI API 키가 필요합니다 (.env 파일에 설정)
            """)


if __name__ == "__main__":
    main()
