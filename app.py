"""
app.py
MarketEcho Index Dashboard - Streamlit 메인 애플리케이션
모듈화된 구조로 UI와 로직을 분리하여 관리
"""

import streamlit as st
from datetime import datetime, timedelta

# 모듈 임포트
from core.scraper import generate_market_echo_index, generate_asset_prices, generate_dummy_news
from ui.charts import create_market_echo_chart
from ui.components import (
    render_page_config,
    render_sidebar,
    render_chat_input,
    render_left_metrics,
    render_right_news,
    render_footer
)


def main():
    """메인 애플리케이션 함수"""
    
    # 페이지 설정
    render_page_config()
    
    # 더미 데이터 로드
    market_echo_df = generate_market_echo_index(days=252)
    asset_df = generate_asset_prices(days=252)
    news_df = generate_dummy_news(days=252, num_news=15)
    
    # 사이드바 렌더링 (자산 선택, 기간 필터)
    selected_asset, selected_period = render_sidebar(market_echo_df, asset_df)
    
    # ========================================================================
    # TOP SECTION: AI 채팅 입력 (Placeholder)
    # ========================================================================
    render_chat_input()
    
    # ========================================================================
    # MAIN LAYOUT: 3단 컬럼 (1:4:1.5 비율)
    # ========================================================================
    col_left, col_main, col_right = st.columns([0.7, 4, 1.5])
    
    # LEFT COLUMN: 메트릭
    with col_left:
        render_left_metrics(market_echo_df, asset_df)
    
    # MAIN COLUMN: 차트
    with col_main:
        st.subheader("📈 시간 흐름에 따른 지수 추이")
        
        # 차트 생성 및 표시
        fig = create_market_echo_chart(
            market_echo_df,
            asset_df,
            selected_asset=selected_asset,
            selected_period=selected_period
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # 차트 설명
        st.info(
            "💡 **Tip**: 마우스를 차트 위에 올려 상세 정보를 확인하세요. "
            "좌측 축은 MarketEcho Index(초록색), 우측 축은 선택한 자산 가격(대시선)입니다."
        )
    
    # RIGHT COLUMN: 뉴스
    with col_right:
        render_right_news(news_df, selected_period)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    render_footer()


if __name__ == '__main__':
    main()
