"""
api/index.py
Vercel 배포용 Streamlit 애플리케이션 진입점
"""

import sys
import os

# 프로젝트 루트 경로 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

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
    
    # 실제 데이터 로드 (CSV 파일에서)
    try:
        asset_df = pd.read_csv('./data/raw/market_prices.csv', index_col=0, parse_dates=True)
        asset_df = asset_df.reset_index().rename(columns={'Datetime': 'date'})  # index를 date 컬럼으로
        news_df = pd.read_csv('./data/raw/raw_news.csv')
        news_df['date'] = pd.to_datetime(news_df['collected_at'])  # date 컬럼 추가
        news_df['category'] = '경제'  # category 컬럼 추가
        news_df = news_df.rename(columns={'title': 'headline'})  # headline 컬럼 매핑
        news_df['keywords'] = [['경제', '시장']] * len(news_df)  # keywords 컬럼 추가 (리스트)
        # 컬럼 이름 매핑 (노트북 데이터에 맞게)
        asset_df = asset_df.rename(columns={
            '10Y_Bond': 'bond_yield',
            'Gold': 'gold_price',
            'Copper': 'copper_price',
            'USD_Index': 'dollar_index',
            'Aluminum': 'aluminum_price'
        })
        # MarketEcho Index는 임시로 더미 데이터 사용 (실제 계산 로직 추가 필요)
        market_echo_df = generate_market_echo_index(days=len(asset_df))
    except FileNotFoundError:
        st.error("데이터 파일을 찾을 수 없습니다. 노트북을 실행해 데이터를 생성하세요.")
        # 폴백으로 더미 데이터 사용
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
