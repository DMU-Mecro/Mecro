import os
import streamlit as st
import pandas as pd
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class NewsRAG:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")
        
        # 임베딩 모델 설정
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-2-preview",
            google_api_key=self.api_key
        )
        
        # 벡터 DB 연결
        self.db_path = "./data/vector_db"
        self.vector_db = Chroma(
            collection_name="macro_intelligence_db_2026",
            embedding_function=self.embeddings,
            persist_directory=self.db_path
        )

    def add_news_to_db(self, news_df):
        if news_df is None or news_df.empty:
            return
        
        # 1. 전처리: 내용이 있는 뉴스만 선별
        clean_df = news_df.dropna(subset=['context_text']).copy()
        clean_df['context_text'] = clean_df['context_text'].astype(str).str.strip()
        clean_df = clean_df[clean_df['context_text'].str.len() > 20] # 너무 짧은 뉴스(노이즈) 제거
        
        success_count = 0
        print(f"🧬 총 {len(clean_df)}건의 뉴스 벡터화 시작...")
        for _, row in clean_df.iterrows():
            try:
                doc = Document(
                    page_content=row['context_text'],
                    metadata={
                        "title": str(row.get('title', 'No Title')),
                        "source": str(row.get('source', 'Unknown')),
                        "published_at": str(row.get('published_at', '')),
                        "url": str(row.get('url', ''))
                    }
                )
                # 한 건씩 안전하게 저장
                self.vector_db.add_documents([doc])
                success_count += 1
            except Exception:
                # 에러 나는 뉴스는 조용히 건너뜁니다 (소음 제거)
                continue

        print(f"✅ {success_count}건 저장 완료 (총 {self.vector_db._collection.count()}건)")
        
    # (리포트 생성 기능)
    def generate_market_report(self, topic, index_score):
        # 2026년 표준 모델 명칭(-preview) 적용
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(model_name="gemini-3.1-flash-lite-preview")
        
        query = f"{topic} 산업 공급망과 거시경제 영향"
        retrieved_docs = self.vector_db.similarity_search(query, k=10)

        if not retrieved_docs:
            return f"💡 {topic} 관련 데이터가 부족합니다. 업데이트 버튼을 먼저 눌러주세요."
        
        context = "\n".join([f"- {doc.page_content}" for doc in retrieved_docs])

        # 2. 페르소나를 주제에 맞게 유동적으로 변경
        prompt = f"""
        당신은 {topic} 분야의 글로벌 투자 전략가입니다.
        
        [현재 MarketEcho 지수]: {index_score:.2f}
        [참조 뉴스 데이터]:
        {context}
        
        위 데이터를 바탕으로 현재 {topic} 산업의 심리 상태와 향후 투자 전략을 한국어로 상세히 작성하세요.
        특히 수집된 뉴스가 {topic} 관련 기업들에게 미칠 영향을 중심으로 서술하세요.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ 리포트 생성 중 오류 발생: {e}"

if __name__ == "__main__":
    # 테스트용
    rag = NewsRAG()
    print("🚀 NewsRAG 엔진 로드 완료!")