"""
core/__init__.py
백엔드 모듈 패키지
"""

from .scraper import (
    generate_market_echo_index,
    generate_asset_prices,
    generate_dummy_news
)

__all__ = [
    'generate_market_echo_index',
    'generate_asset_prices',
    'generate_dummy_news'
]
