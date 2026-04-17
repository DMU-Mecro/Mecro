import os
import time
import pandas as pd
import yfinance as yf
import feedparser
from datetime import datetime, timedelta

# 0. 한국 시간 설정 (UTC+9)
kst_now = datetime.utcnow() + timedelta(hours=9)

# 1. 로컬 경로 및 전역 설정
DATA_PATH = "./data/raw"
os.makedirs(DATA_PATH, exist_ok=True)

RSS_SOURCES = {
    "Yahoo_Main": "https://finance.yahoo.com/news/rss",
    "Yahoo_CentralBank": "https://finance.yahoo.com/news/category-central-banks/rss",
    "Yahoo_Economy": "https://finance.yahoo.com/news/category-economy/rss"
}

# 2. 거시경제 뉴스 필터링
def is_macro_news(title):
    exclude_keywords = [
        'CD rates', 'Credit score', 'Sallie Mae', 'Personal Finance',
        'Tax refund', 'Best banks', 'HELOC', 'Mortgage rates today',
        'Credit card', 'Savings account'
    ]
    return not any(keyword.lower() in title.lower() for keyword in exclude_keywords)

# 3. 뉴스 수집 엔진 (로컬 최적화 버전)
def fetch_accumulated_news(limit_year="2026"):
    all_news = []
    now_kst = datetime.utcnow() + timedelta(hours=9)
    
    for name, url in RSS_SOURCES.items():
        print(f"📡 {name} 피드 분석 중...")
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            # 1단계: 매크로 필터링
            if not is_macro_news(entry.title): continue

            # 2단계: 날짜 처리 (KST 기준)
            try:
                pub_time = datetime(*entry.published_parsed[:6]) + timedelta(hours=9)
                published_at = pub_time.strftime('%Y-%m-%d %H:%M:%S')
            except:
                published_at = now_kst.strftime('%Y-%m-%d %H:%M:%S')

            if not published_at.startswith(limit_year): continue

            all_news.append({
                "title": entry.title,
                "url": entry.link,
                "published_at": published_at,
                "source": name,
                "context_text": f"[{published_at}] {name}: {entry.title}. Summary: {getattr(entry, 'summary', '')}"
            })

    file_path = os.path.join(DATA_PATH, "raw_news.csv")
    if not all_news:
        print("💡 수집된 신규 거시경제 뉴스가 없습니다.")
        return pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame()

    new_df = pd.DataFrame(all_news)

    # 기존 데이터와 병합 로직 (누적)
    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        old_df = old_df[old_df['published_at'].str.startswith(limit_year)]
        new_only_df = new_df[~new_df['url'].isin(old_df['url'])].copy()
        final_df = pd.concat([old_df, new_only_df]).drop_duplicates(subset=['url'], keep='first')
    else:
        final_df = new_df

    final_df.sort_values(by='published_at', ascending=False, inplace=True)
    final_df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"✅ 뉴스 업데이트 완료: 총 {len(final_df)}개")
    return final_df

# 4. 마켓 데이터 수집 엔진
def fetch_robust_market_data(period="1mo"):
    tickers = {
        "10Y_Bond": "^TNX", "Gold": "GC=F", "Silver": "SI=F",
        "Copper": "HG=F", "USD_Index": "DX-Y.NYB", "Aluminum": "ALI=F"
    }
    all_data = []
    for name, ticker in tickers.items():
        print(f"📈 {name} 로드 중...")
        try:
            df = yf.Ticker(ticker).history(period=period, interval="1h")
            if not df.empty:
                df = df[['Close']].rename(columns={'Close': name})
                df.index = df.index.tz_localize(None).floor('h')
                all_data.append(df)
        except Exception as e:
            print(f"⚠️ {name} 실패: {e}")

    if not all_data: return pd.DataFrame()

    market_df = pd.concat(all_data, axis=1)
    market_df = market_df[~market_df.index.duplicated(keep='first')]
    
    # 결측치 보간 처리
    full_index = pd.date_range(start=market_df.index.min(), end=market_df.index.max(), freq='h')
    market_df = market_df.reindex(full_index).ffill().bfill()

    market_df.to_csv(os.path.join(DATA_PATH, "market_prices.csv"))
    print(f"✅ 마켓 데이터 완료: {len(market_df)} 행")
    return market_df

if __name__ == "__main__":
    # 독립 실행 테스트용
    fetch_accumulated_news()
    fetch_robust_market_data()