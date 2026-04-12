"""
ui/charts.py
Plotly 금융 차트 생성 및 시각화 함수
"""

import plotly.graph_objects as go
import pandas as pd


def create_market_echo_chart(market_echo_df, asset_df, selected_asset='gold_price', selected_period='1M'):
    """
    이중축 Plotly 차트 생성
    - 좌축: MarketEcho Index (라인, Neon Green/Red)
    - 우축: 선택한 자산 가격
    
    Args:
        market_echo_df (pd.DataFrame): MarketEcho Index 데이터
        asset_df (pd.DataFrame): 자산 가격 데이터
        selected_asset (str): 선택한 자산 ('gold_price', 'bond_yield', 'dollar_index')
        selected_period (str): 선택한 기간 ('1D', '1W', '1M', '3M', '1Y')
    
    Returns:
        plotly.graph_objects.Figure: Plotly 차트 객체
    """
    
    # 기간 필터 적용
    days_filter = {
        '1D': 1,
        '1W': 5,
        '1M': 21,
        '3M': 63,
        '1Y': 252
    }
    
    days = days_filter.get(selected_period, 21)
    filtered_market = market_echo_df.tail(days).reset_index(drop=True)
    filtered_asset = asset_df.tail(days).reset_index(drop=True)
    
    # 색상 결정 (상승: Neon Green, 하락: Red)
    index_colors = ['#00ff88' if i == 0 or filtered_market['market_echo_index'].iloc[i] >= filtered_market['market_echo_index'].iloc[i-1] 
                    else '#ff3333' 
                    for i in range(len(filtered_market))]
    
    # 이중축 차트 생성
    fig = go.Figure()
    
    # 1. MarketEcho Index (좌축)
    fig.add_trace(go.Scatter(
        x=filtered_market['date'],
        y=filtered_market['market_echo_index'],
        mode='lines+markers',
        name='MarketEcho Index',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=5, color=index_colors),
        yaxis='y1',
        hovertemplate='<b>MarketEcho Index</b><br>날짜: %{x|%Y-%m-%d}<br>지수: %{y:.2f}<extra></extra>'
    ))
    
    # 2. 자산 가격 (우축)
    asset_names = {
        'bond_yield': ('국채 수익률 (%)', '#00aaff'),
        'gold_price': ('금 가격 (USD/oz)', '#ffd700'),
        'dollar_index': ('달러 지수', '#ff6b9d')
    }
    
    asset_label, asset_color = asset_names.get(selected_asset, ('자산 가격', '#888888'))
    
    fig.add_trace(go.Scatter(
        x=filtered_asset['date'],
        y=filtered_asset[selected_asset],
        mode='lines',
        name=asset_label,
        line=dict(color=asset_color, width=2, dash='dash'),
        yaxis='y2',
        hovertemplate=f'<b>{asset_label}</b><br>날짜: %{{x|%Y-%m-%d}}<br>가격: %{{y:.2f}}<extra></extra>'
    ))
    
    # 레이아웃 설정
    fig.update_layout(
        title=dict(
            text="📊 MarketEcho Index vs 실제 자산 가격 추이",
            font=dict(size=20, color='#00ff88')
        ),
        plot_bgcolor='#0a0e27',
        paper_bgcolor='#0a0e27',
        font=dict(color='#ffffff', size=12),
        hovermode='x unified',
        legend=dict(
            bgcolor='rgba(0, 0, 0, 0.5)',
            bordercolor='#00ff88',
            borderwidth=1
        ),
        xaxis=dict(
            gridcolor='#333333',
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text='MarketEcho Index (0~100)', font=dict(color='#00ff88')),
            tickfont=dict(color='#00ff88'),
            gridcolor='#333333',
            zeroline=False,
        ),
        yaxis2=dict(
            title=dict(text=asset_label, font=dict(color=asset_color)),
            tickfont=dict(color=asset_color),
            overlaying='y',
            side='right',
            zeroline=False,
        ),
        margin=dict(l=50, r=50, t=100, b=50),
        height=500
    )
    
    return fig
