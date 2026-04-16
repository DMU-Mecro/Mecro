"""
core/scraper.py
더미 데이터 수집 및 생성 엔진 (실제 API 연동 예정)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_market_echo_index(days=252, volatility=5):
    """
    MarketEcho Index 생성 (0~100 범위의 난수)
    
    Args:
        days (int): 생성할 날짜 수
        volatility (float): 변동성 (표준편차)
    
    Returns:
        pd.DataFrame: 날짜와 지수값이 포함된 데이터프레임
    """
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')  # Daily
    
    # 랜덤 워크 시뮬레이션
    base_index = 50
    changes = np.random.randn(days) * volatility
    index_values = base_index + np.cumsum(changes)
    index_values = np.clip(index_values, 0, 100)  # 0~100 범위로 제한
    
    return pd.DataFrame({
        'date': dates,
        'market_echo_index': index_values
    })


def generate_asset_prices(days=252):
    """
    자산별 가격 시뮬레이션 (국채, 금, 달러)
    
    Args:
        days (int): 생성할 날짜 수
    
    Returns:
        pd.DataFrame: 자산별 가격 데이터프레임
    """
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    # 국채 (Bond Yield % per annum)
    bond_base = 4.5
    bond_changes = np.random.randn(days) * 0.1
    bond_yield = bond_base + np.cumsum(bond_changes) / 100
    bond_yield = np.clip(bond_yield, 2, 6)
    
    # 금 가격 (Gold, USD/oz)
    gold_base = 2000
    gold_changes = np.random.randn(days) * 50
    gold_price = gold_base + np.cumsum(gold_changes)
    gold_price = np.clip(gold_price, 1500, 2500)
    
    # 달러 지수 (USD Index)
    dollar_base = 100
    dollar_changes = np.random.randn(days) * 0.5
    dollar_index = dollar_base + np.cumsum(dollar_changes)
    dollar_index = np.clip(dollar_index, 95, 110)
    
    return pd.DataFrame({
        'date': dates,
        'bond_yield': bond_yield,
        'gold_price': gold_price,
        'dollar_index': dollar_index
    })


def generate_dummy_news(days=252, num_news=15):
    """
    뉴스 항목 생성 (더미 데이터)
    
    Args:
        days (int): 데이터 범위 (일)
        num_news (int): 생성할 뉴스 개수
    
    Returns:
        pd.DataFrame: 뉴스 데이터프레임
    """
    categories = ['금융', '거시경제', '에너지', '통화정책', '인플레이션']
    headlines = [
        "연준, 기준금리 유지 결정...앞으로의 방향성은?",
        "금값이 2025년 이래 최고가 경신",
        "달러 약세 지속으로 신흥시장 자산 강세",
        "유로존 경제지표 좋은 신호",
        "국채 수익률 급등, 채권 투자자 긴장",
        "유가 상승 추세 계속, 수입물가 우려",
        "미중 무역 긴장 고조, 환율 변동성 증가",
        "ECB, 통화정책 정상화 가속화",
        "인플레이션 지표 3개월 연속 상승",
        "기술주 약세로 주가지수 조정",
    ]
    
    base_date = datetime.now() - timedelta(days=days)
    news_data = []
    
    for i in range(num_news):
        news_date = base_date + timedelta(days=random.randint(0, days-1))
        news_data.append({
            'date': news_date,
            'headline': random.choice(headlines),
            'category': random.choice(categories),
            'url': f"https://finance.yahoo.com/news/article-{i+1}",
            'keywords': random.sample(['금리', '환율', '인플레이션', '채권'], 2)
        })
    
    return pd.DataFrame(news_data).sort_values('date', ascending=False)
