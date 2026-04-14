import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 우리가 만든 핵심 모듈 임포트
from core.scraper import fetch_accumulated_news, fetch_robust_market_data
from core.rag_engine import NewsRAG
from core.analyzer import NewsAnalyzer

# --- 1. 실전 데이터 로드 및 처리 ---

def load_real_data():
    """CSV 파일에서 실제 데이터를 읽어오고 분석 결과를 합산함"""
    news_path = "./data/raw/raw_news.csv"
    market_path = "./data/raw/market_prices.csv"
    sentiment_path = "./data/sentiment_results.csv"

    # 1. 뉴스 및 마켓 데이터 로드
    news_df = pd.read_csv(news_path) if os.path.exists(news_path) else pd.DataFrame()
    market_df = pd.read_csv(market_path) if os.path.exists(market_path) else pd.DataFrame()
    
    # 2. MarketEcho Index (심리 지수) 계산
    if os.path.exists(sentiment_path):
        sent_df = pd.read_csv(sentiment_path)
        sent_df['Date'] = pd.to_datetime(sent_df['Date'])
        sent_df = sent_df.sort_values('Date')
        # 날짜별 점수 합산 후 누적 합계(Cumulative Sum) 계산
        daily_sent = sent_df.groupby(sent_df['Date'].dt.date)['Score'].sum().reset_index()
        daily_sent['MarketEcho_Index'] = daily_sent['Score'].cumsum()
        daily_sent['Date'] = pd.to_datetime(daily_sent['Date'])
    else:
        daily_sent = pd.DataFrame(columns=['Date', 'MarketEcho_Index'])

    return daily_sent, market_df, news_df

def run_pipeline():
    """데이터 수집부터 분석까지 한 번에 실행"""
    with st.status("🚀 통합 데이터 엔진 가동 중...", expanded=True) as status:
        st.write("📡 1단계: 최신 뉴스 및 가격 데이터 수집...")
        raw_news = fetch_accumulated_news()
        fetch_robust_market_data()
        
        st.write("🧬 2단계: 지능형 벡터 DB 업데이트...")
        rag = NewsRAG()
        rag.add_news_to_db(raw_news)
        
        st.write("🧠 3단계: AI 전략가 감성 분석 수행...")
        analyzer = NewsAnalyzer()
        new_sentiments = analyzer.run_parallel_analysis(raw_news)
        
        if not new_sentiments.empty:
            new_sentiments.to_csv("./data/sentiment_results.csv", index=False, encoding='utf-8-sig')
            
        status.update(label="✅ 모든 데이터 업데이트 완료!", state="complete", expanded=False)
    st.rerun()

# --- 2. UI 구성 요소 ---

def render_sidebar(index_df, market_df):
    st.sidebar.title("🛠️ Control Panel")
    
    if st.sidebar.button("🔄 데이터 강제 업데이트", help="새 뉴스를 가져오고 지수를 갱신합니다."):
        run_pipeline()
    
    st.sidebar.divider()
    
    # 자산 선택 (랜덤 요소 제거, 실제 컬럼 기준)
    cols = [c for c in market_df.columns if c not in ['Date', 'Unnamed: 0']]
    selected_asset = st.sidebar.selectbox("📊 비교 자산 선택", cols if cols else ["데이터 없음"])
    
    period = st.sidebar.radio("📅 분석 기간", ["1주", "1개월", "전체"], index=1)
    return selected_asset, period

def create_chart(index_df, market_df, selected_asset, period):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # MarketEcho Index (실제 심리 지수)
    if not index_df.empty:
        fig.add_trace(go.Scatter(x=index_df['Date'], y=index_df['MarketEcho_Index'], 
                                 name="심리 지수 (MarketEcho)", line=dict(color="#2E7D32", width=3)), secondary_y=False)
    
    # 실제 자산 가격
    if selected_asset in market_df.columns:
        # 첫 번째 컬럼을 날짜로 간주
        date_col = market_df.columns[0]
        fig.add_trace(go.Scatter(x=pd.to_datetime(market_df[date_col]), y=market_df[selected_asset], 
                                 name=selected_asset, line=dict(color="#C62828", dash='dot')), secondary_y=True)
        
    fig.update_layout(template="plotly_white", hovermode="x unified", height=500,
                      margin=dict(l=20, r=20, t=30, b=20))
    return fig

# --- 3. 메인 애플리케이션 ---

def main():
    st.set_page_config(page_title="MarketEcho", layout="wide", page_icon="📈")
    index_df, market_df, news_df = load_real_data()

    current_val = index_df['MarketEcho_Index'].iloc[-1] if not index_df.empty else 0.0

    selected_asset, selected_period = render_sidebar(index_df, market_df)
    # 상단 헤더
    st.title("📈 MarketEcho Index Dashboard")
    st.caption("실시간 매크로 심리와 자산 가격을 결합한 지능형 분석 시스템")

    # 레이아웃 구성 (한빈 님 스타일 계승)
    col_left, col_main, col_right = st.columns([0.7, 4, 1.5])

    with col_left:
        st.metric("현재 심리 지수", f"{current_val:.2f}")
        st.write("---")
        st.caption("AI가 분석한 시장의 누적 심리 신호입니다.")

    with col_main:
        st.subheader("📊 지수 추이 및 자산 상관관계")
        if not index_df.empty or not market_df.empty:
            fig = create_chart(index_df, market_df, selected_asset, selected_period)
            st.plotly_chart(fig, width='stretch')
        else:
            st.warning("데이터가 없습니다. 사이드바의 업데이트 버튼을 눌러주세요.")

        st.write("---")
        st.subheader("🤖 AI 맞춤형 매크로 분석")
        
        analysis_topic = st.text_input("🎯 분석하고 싶은 산업/주제를 입력하세요 (예: 반도체")
        
        if st.checkbox(f"🔍 {analysis_topic} 리포트 생성하기"):
            with st.spinner(f"AI가 {analysis_topic} 관련 뉴스를 분석 중입니다..."):
                rag = NewsRAG()
                report = rag.generate_market_report(analysis_topic, current_val)
                st.markdown(report)

    with col_right:
        st.subheader("📰 최신 뉴스 피드")
        if not news_df.empty:
            for _, row in news_df.head(15).iterrows():
                with st.expander(f"[{row['source']}] {row['title'][:25]}..."):
                    st.caption(f"날짜: {row['published_at']}")
                    st.link_button("뉴스 원문 읽기", row['url'])
        else:
            st.write("수집된 뉴스가 없습니다.")

    st.divider()
    st.caption(f"최종 데이터 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()