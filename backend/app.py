# --- 0. 배포 환경(리눅스) SQLite 패치 (가장 먼저!) ---
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# 💡 우리가 만든 UI 모듈 임포트
from ui.charts import create_market_echo_chart
from ui.components import render_news_section, render_ai_report_area

# 💡 핵심 엔진 모듈 임포트
from core.scraper import fetch_accumulated_news, fetch_robust_market_data
from core.rag_engine import NewsRAG
from core.analyzer import NewsAnalyzer

# --- 1. 엔진 최적화 (Caching) ---
@st.cache_resource
def get_rag_engine():
    """RAG 엔진을 한 번만 로드하여 메모리 낭비를 방지함"""
    return NewsRAG()

@st.cache_resource
def get_analyzer():
    """감성 분석 엔진을 캐싱함"""
    return NewsAnalyzer()

# --- 2. 데이터 로드 및 파이프라인 ---
def load_real_data():
    """CSV 파일에서 데이터를 읽어오고 심리 지수를 계산함"""
    os.makedirs("./data/raw", exist_ok=True)
    news_path = "./data/raw/raw_news.csv"
    market_path = "./data/raw/market_prices.csv"
    sentiment_path = "./data/sentiment_results.csv"

    news_df = pd.read_csv(news_path) if os.path.exists(news_path) else pd.DataFrame()
    market_df = pd.read_csv(market_path) if os.path.exists(market_path) else pd.DataFrame()
    
    if os.path.exists(sentiment_path):
        sent_df = pd.read_csv(sentiment_path)
        sent_df['Date'] = pd.to_datetime(sent_df['Date'])
        sent_df = sent_df.sort_values('Date')
        # 날짜별 점수 합산 후 누적 합계 계산
        daily_sent = sent_df.groupby(sent_df['Date'].dt.date)['Score'].sum().reset_index()
        daily_sent['MarketEcho_Index'] = daily_sent['Score'].cumsum()
        daily_sent['Date'] = pd.to_datetime(daily_sent['Date'])
    else:
        daily_sent = pd.DataFrame(columns=['Date', 'MarketEcho_Index'])

    return daily_sent, market_df, news_df

def run_pipeline():
    """데이터 수집 및 분석 파이프라인 실행"""
    with st.status("🚀 통합 데이터 엔진 가동 중...", expanded=True) as status:
        st.write("📡 1단계: 최신 뉴스 및 가격 데이터 수집...")
        raw_news = fetch_accumulated_news()
        fetch_robust_market_data()
        
        st.write("🧬 2단계: 지능형 벡터 DB 업데이트...")
        get_rag_engine().add_news_to_db(raw_news)
        
        st.write("🧠 3단계: AI 전략가 감성 분석 수행...")
        new_sentiments = get_analyzer().run_parallel_analysis(raw_news)
        
        if not new_sentiments.empty:
            sentiment_path = "./data/sentiment_results.csv"
            if os.path.exists(sentiment_path):
                old_sent = pd.read_csv(sentiment_path)
                pd.concat([old_sent, new_sentiments]).drop_duplicates().to_csv(sentiment_path, index=False, encoding='utf-8-sig')
            else:
                new_sentiments.to_csv(sentiment_path, index=False, encoding='utf-8-sig')
            
        status.update(label="✅ 모든 데이터 업데이트 완료!", state="complete")
    st.rerun()

# --- 3. 메인 UI 조립 ---
def main():
    st.set_page_config(page_title="MarketEcho", layout="wide", page_icon="📈")
    
    # 데이터 로드
    index_df, market_df, news_df = load_real_data()
    
    # 1) 사이드바 제어 및 필터링 변수 획득
    st.sidebar.title("🛠️ Control Panel")
    if st.sidebar.button("🔄 데이터 강제 업데이트"):
        run_pipeline()
    
    st.sidebar.divider()
    
    # 자산 선택
    cols = [c for c in market_df.columns if c not in ['Date', 'Unnamed: 0']]
    selected_asset = st.sidebar.selectbox("📊 비교 자산 선택", cols if cols else ["데이터 없음"])
    
    # 💡 분석 기간 선택 (신호 획득)
    period = st.sidebar.radio("📅 분석 기간", ["1주", "1개월", "전체"], index=1)

    # 💡 데이터 필터링 로직 (신호 처리)
    today = datetime.now()
    if period == "1주":
        start_date = today - timedelta(days=7)
    elif period == "1개월":
        start_date = today - timedelta(days=30)
    else:
        start_date = datetime(2000, 1, 1) # 전체 기간

    # 날짜 필터링 적용
    filtered_index = index_df[index_df['Date'] >= start_date]
    
    # 마켓 데이터의 첫 번째 컬럼(날짜)을 기준으로 필터링
    if not market_df.empty:
        date_col = market_df.columns[0]
        market_df[date_col] = pd.to_datetime(market_df[date_col])
        filtered_market = market_df[market_df[date_col] >= start_date]
    else:
        filtered_market = market_df

    # 현재 지수 값 (필터링되지 않은 최신값 기준)
    current_val = index_df['MarketEcho_Index'].iloc[-1] if not index_df.empty else 0.0

    # 2) 메인 헤더
    st.title("📈 MarketEcho Index Dashboard")
    st.caption("실시간 매크로 심리와 자산 가격을 결합한 지능형 분석 시스템")

    # 3) 3단 레이아웃 (0.7 : 4 : 1.5)
    col_left, col_main, col_right = st.columns([0.7, 4, 1.5])

    with col_left:
        st.metric("현재 심리 지수", f"{current_val:.2f}")
        st.divider()
        st.caption(f"AI 분석 {period} 누적 지표")

    with col_main:
        st.subheader(f"📊 {period} 지수 추이 및 상관관계")
        if not filtered_index.empty:
            # 💡 필터링된 데이터를 차트 모듈에 전달
            fig = create_market_echo_chart(filtered_index, filtered_market, selected_asset)
            st.plotly_chart(fig, width='stretch')
        else:
            st.warning(f"⚠️ {period} 이내의 수집된 데이터가 부족합니다. 업데이트를 진행해 주세요.")

        st.divider()
        st.subheader("🤖 AI 맞춤형 매크로 분석")
        topic = st.text_input("🎯 분석하고 싶은 산업/주제를 입력하세요", placeholder="예: 반도체, 유가, 금리")
        if topic and st.checkbox(f"🔍 {topic} 리포트 생성하기"):
            with st.spinner(f"AI가 {topic} 관련 지식을 조합 중입니다..."):
                report = get_rag_engine().generate_market_report(topic, current_val)
                render_ai_report_area(report)

    with col_right:
        render_news_section(news_df)

    st.divider()
    st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Developed by Kim Han-bin")

if __name__ == '__main__':
    main()