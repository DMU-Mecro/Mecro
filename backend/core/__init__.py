"""
NewsDoc 핵심 백엔드 패키지
"""
# 패키지 초기화를 위해 내용을 비워두거나, 
from .scraper import fetch_accumulated_news, fetch_robust_market_data
from .rag_engine import NewsRAG
from .analyzer import NewsAnalyzer