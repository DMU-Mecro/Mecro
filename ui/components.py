import streamlit as st

def render_news_section(news_df):
    """우측 뉴스 피드 렌더링"""
    st.subheader("📰 최신 뉴스 피드")
    if not news_df.empty:
        for _, row in news_df.head(15).iterrows():
            # 뉴스 소스와 제목을 결합한 헤더
            title_preview = str(row.get('title', ''))[:25]
            with st.expander(f"[{row.get('source', 'News')}] {title_preview}..."):
                st.caption(f"발행일: {row.get('published_at', 'N/A')}")
                st.link_button("뉴스 원문 읽기", row.get('url', '#'))
    else:
        st.info("수집된 뉴스가 아직 없습니다.")

def render_ai_report_area(report_text):
    """생성된 AI 리포트 출력 구역"""
    if report_text:
        st.divider()
        st.info("🤖 Gemini 3.1 Flash Lite의 매크로 전략 분석")
        st.markdown(report_text)