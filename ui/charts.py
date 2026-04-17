import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_market_echo_chart(index_df, market_df, selected_asset):
    """지수와 자산 가격을 결합한 이중축 차트 생성"""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 1. 심리 지수 (Line Chart)
    if not index_df.empty:
        fig.add_trace(go.Scatter(
            x=index_df['Date'], 
            y=index_df['MarketEcho_Index'], 
            name="심리 지수", 
            line=dict(color="#2E7D32", width=3)
        ), secondary_y=False)
    
    # 2. 비교 자산 (Dotted Line)
    if not market_df.empty and selected_asset in market_df.columns:
        date_col = market_df.columns[0]
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(market_df[date_col]), 
            y=market_df[selected_asset], 
            name=selected_asset, 
            line=dict(color="#C62828", dash='dot')
        ), secondary_y=True)
        
    fig.update_layout(
        template="plotly_white", 
        hovermode="x unified", 
        height=500,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig