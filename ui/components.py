"""
ui/components.py
Streamlit UI 컴포넌트 및 헬퍼 함수
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render_page_config():
    """Streamlit 페이지 설정"""
    st.set_page_config(
        page_title="MarketEcho Index",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 다크 테마 CSS 적용
    st.markdown("""
        <style>
            :root {
                --primary-color: #1f77b4;
                --text-color: #ffffff;
            }
            .metric-card {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #00ff88;
            }
        </style>
    """, unsafe_allow_html=True)


def render_sidebar(market_echo_df, asset_df):
    """
    왼쪽 사이드바 렌더링
    
    Args:
        market_echo_df (pd.DataFrame): MarketEcho Index 데이터
        asset_df (pd.DataFrame): 자산 가격 데이터
    
    Returns:
        tuple: (selected_asset, selected_period)
    """
    with st.sidebar:
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center;'>
                <h1 style='color: #00ff88;'>📊</h1>
                <h2 style='color: #00ff88; margin: 10px 0;'>MarketEcho Index</h2>
                <p style='color: #888888; font-size: 12px; margin: 0;'>경제의 메아리를 통번역하다</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 1. 자산 선택
        st.subheader("📈 자산 선택")
        asset_choice = st.selectbox(
            "거시변수 선택",
            options=['gold_price', 'bond_yield', 'dollar_index'],
            format_func=lambda x: {
                'gold_price': '🥇 금 (Gold)',
                'bond_yield': '📊 국채 (Bond Yield)',
                'dollar_index': '💵 달러 지수 (USD Index)'
            }[x],
            key='asset_select'
        )
        
        # 2. 기간 필터
        st.subheader("⏱️ 기간 필터")
        period_cols = st.columns(5)
        
        periods = ['1D', '1W', '1M', '3M', '1Y']
        for i, period in enumerate(periods):
            with period_cols[i]:
                if st.button(period, use_container_width=True):
                    st.session_state.selected_period = period
        
        selected_period = st.session_state.get('selected_period', '1M')
        
        # 3. 구독 상태
        st.markdown("---")
        st.subheader("💳 구독 상태")
        st.markdown("""
            <div style='background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); 
                        padding: 15px; border-radius: 10px; 
                        border-left: 4px solid #00ff88; text-align: center;'>
                <p style='color: #00ff88; font-size: 14px; margin: 5px 0;'>🟢 Active</p>
                <p style='color: #ffffff; font-size: 16px; font-weight: bold; margin: 5px 0;'>$5/mo</p>
                <p style='color: #888888; font-size: 12px; margin: 5px 0;'>프리미엄 회원</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("Powered by MarketEcho © 2026")
    
    return asset_choice, selected_period


def render_chat_input():
    """AI 채팅 입력 영역 (Placeholder)"""
    st.markdown("""
        <div style='background: #1a1a2e; border: 2px solid #00ff88; padding: 15px; 
                    border-radius: 10px; margin-bottom: 20px;'>
            <p style='color: #888888; margin: 0; font-size: 12px;'>🤖 AI 질문 입력 (준비 중)</p>
            <input type='text' placeholder='예: 최근 환율이 상승한 이유는?' 
                   style='width: 100%; padding: 10px; margin-top: 10px; 
                          background: #0a0e27; color: #ffffff; border: 1px solid #333; 
                          border-radius: 5px;' disabled/>
        </div>
    """, unsafe_allow_html=True)


def render_left_metrics(market_echo_df, asset_df):
    """
    왼쪽 컬럼: 메트릭 정보
    
    Args:
        market_echo_df (pd.DataFrame): MarketEcho Index 데이터
        asset_df (pd.DataFrame): 자산 가격 데이터
    """
    st.subheader("📊 지표")
    
    # 최신 MarketEcho 지수 표시
    latest_index = market_echo_df['market_echo_index'].iloc[-1]
    prev_index = market_echo_df['market_echo_index'].iloc[-2]
    change = latest_index - prev_index
    
    st.metric(
        label="MarketEcho Index",
        value=f"{latest_index:.1f}",
        delta=f"{change:+.2f}" if abs(change) > 0 else "± 0",
        delta_color="off"
    )
    
    st.markdown("---")
    
    # 자산별 최신 가격
    asset_display = {
        'gold_price': ('🥇 금', f"${asset_df['gold_price'].iloc[-1]:.2f}"),
        'bond_yield': ('📊 국채', f"{asset_df['bond_yield'].iloc[-1]:.2f}%"),
        'dollar_index': ('💵 달러', f"{asset_df['dollar_index'].iloc[-1]:.2f}")
    }
    
    for asset_key, (label, value) in asset_display.items():
        st.write(f"**{label}**: {value}")


def render_right_news(news_df, selected_period):
    """
    오른쪽 컬럼: 뉴스 타임라인
    
    Args:
        news_df (pd.DataFrame): 뉴스 데이터
        selected_period (str): 선택한 기간
    """
    st.subheader("📰 주요 뉴스")
    
    # 현재 기간에 해당하는 뉴스 필터
    days_filter = {'1D': 1, '1W': 5, '1M': 21, '3M': 63, '1Y': 252}
    days = days_filter.get(selected_period, 21)
    
    filter_start_date = (datetime.now() - timedelta(days=days)).date()
    filter_end_date = datetime.now().date()
    
    filtered_news = news_df[
        (news_df['date'].dt.date >= filter_start_date) & 
        (news_df['date'].dt.date <= filter_end_date)
    ].sort_values('date', ascending=False)
    
    if len(filtered_news) == 0:
        st.warning("해당 기간의 뉴스가 없습니다.")
    else:
        for idx, row in filtered_news.iterrows():
            # 뉴스 카드
            with st.container():
                col_time, col_cat = st.columns([2, 1])
                
                with col_time:
                    st.caption(f"📅 {row['date'].strftime('%Y-%m-%d %H:%M')}")
                
                with col_cat:
                    st.caption(f"🏷️ {row['category']}")
                
                # 링크가 포함된 제목
                st.markdown(
                    f"**[{row['headline']}]({row['url']})**",
                    unsafe_allow_html=True
                )
                
                # 키워드 태그
                keywords = ', '.join(row['keywords'])
                st.caption(f"🔑 {keywords}")
                
                st.divider()


def render_footer():
    """페이지 푸터"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #888888; font-size: 12px; margin-top: 30px;'>
            <p>MarketEcho Index Dashboard v0.1 MVP | 더미 데이터 기반 시각화</p>
            <p>💡 실제 데이터는 곧 연결될 예정입니다. (Yfinance, NewsAPI)</p>
        </div>
        """,
        unsafe_allow_html=True
    )
