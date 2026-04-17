import os
import streamlit as st
import json
import pandas as pd
import concurrent.futures
import google.generativeai as genai
from dotenv import load_dotenv

# 팀의 .env 설정 로드 (비용 계정 유지)
load_dotenv()

class NewsAnalyzer:
    def __init__(self):
        # API 키 설정 및 유효성 검사
        self.api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")
        genai.configure(api_key=self.api_key)

    # 1. Gemini를 이용한 단일 뉴스 감성 분석 (팀 표준 로직)
    def analyze_sentiment(self, title):
        model = genai.GenerativeModel(model_name='gemini-3.1-flash-lite-preview')
        prompt = f'''
        당신은 10년 차 글로벌 매크로 전략가입니다. 뉴스 제목을 읽고 시장의 '심리적 온도'를 -1.0에서 1.0 사이로 측정하세요.
        [뉴스 제목]: {title}
        분석 가이드:
        - 매파적(긴축/강달러/성장) 뉘앙스: 0.1 ~ 1.0
        - 비둘기파적(완화/약달러/침체) 뉘앙스: -0.1 ~ -1.0
        - 경제와 무관한 중립 정보: 0.0
        결과는 반드시 아래 JSON 형식으로만 답변하세요:
        {{ "sentiment_score": (수치), "analysis": "한 줄 이유" }}
        '''
        try:
            response = model.generate_content(prompt)
            # JSON 텍스트 정제 및 파싱
            res_text = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(res_text)
        except Exception as e:
            # 에러 발생 시 로그만 출력하고 프로그램은 유지
            print(f"⚠️ 분석 실패 ({title[:20]}...): {e}")
            return None

    # 2. 고속 병렬 분석 파이프라인 (팀의 효율적 분석 로직)
    def run_parallel_analysis(self, to_analyze_df, max_workers=10):
        if to_analyze_df is None or to_analyze_df.empty:
            return pd.DataFrame()

        results = []
        def process_row(row):
            res = self.analyze_sentiment(row['title'])
            if res:
                return {
                    'Date': row['published_at'],
                    'Score': res.get('sentiment_score', 0.0),
                    'Title': row['title'],
                    'URL': row['url']
                }
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_row, row) for _, row in to_analyze_df.iterrows()]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res: results.append(res)

        return pd.DataFrame(results)

if __name__ == "__main__":
    # 팀 표준 모델 작동 테스트
    try:
        analyzer = NewsAnalyzer()
        test_title = "Fed hints at potential rate cuts as inflation cools"
        print("🔍 팀 표준 모델(gemini-1.5-flash) 테스트 중...")
        result = analyzer.analyze_sentiment(test_title)
        print(f"✅ 테스트 결과: {result}")
    except Exception as e:
        print(f"❌ 분석기 가동 실패: {e}")