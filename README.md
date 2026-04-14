# 🌍 MarketEcho Index

> **경제의 메아리를 통번역하다** — Signal over Noise

최신 경제 뉴스와 주요 발언을 기반으로 거시경제 현상의 원인을 **RAG 기반 AI가 설명**하는 금융 분석 대시보드입니다.

## 🔄 최근 업데이트 (지금까지 진행된 내용)

- `requirements.txt` 정리: 코드베이스에서 사용되는 패키지를 추출해 `requirements.txt`를 업데이트하고, 현재 `.venv`에 설치된 정확한 버전으로 고정했습니다. (파일: [requirements.txt](requirements.txt))
- 가상환경 정리 및 재설치: 기존 가상환경에서 불필요한 패키지를 제거한 뒤, 필요한 패키지만 재설치하여 개발 환경을 정리했습니다. 재설치 결과는 `installed_after.txt`에 기록되어 있습니다.
- LangChain / RAG 관련 패키지 설치와 일부 대형 의존성(chromadb, onnxruntime 등) 설치 시 파일 잠금 문제가 발생하여 잠금 해제 후 재시도하여 설치를 완료했습니다.

## 🧭 다음 작업 (우선순위)

- 로컬에서 Streamlit 앱 실행 및 기능 통합 테스트(`app.py` 실행).
- `core/scraper.py`, `core/analyzer.py`, `core/rag_engine.py`의 통합 검증 및 에러 처리 보완.
- 불필요한 대형 의존성(예: `onnxruntime`, `chromadb`)에 대해 사용 여부를 재검토하고 필요시 제거하여 경량화.
- `requirements.txt`를 커밋하고, CI 환경에서 동일한 설치가 재현되는지 검증.


## 📌 프로젝트 정체성

### 🎯 핵심 비전
"**왜?**" 라고 묻는 투자자를 위한 AI 분석 시스템

- 📊 **MarketEcho Index**: 경제 뉴스의 "메아리" 즉, **파급력**을 수치화
- 🤖 **RAG 기반**: 뉴스 데이터베이스에서 근거를 찾아 **신뢰할 수 있는 답변** 제공
- 💡 **Signal over Noise**: 잡음 속에서 **핵심 신호만 추출**

### 🚀 팀 문화
- **TFITH**: 시작이 반이다 → 완성도 높은 MVP부터 시작
- **Collaborative Design**: 기획(한빈) × 개발(태영) × 분석(태영)

---

## 🏗️ 프로젝트 구조

```
MECRO/
├── .venv/                      # Python 가상환경
├── data/                       # 수집된 뉴스 및 지수 데이터
│   ├── *.csv                   # 시계열 지수 데이터
│   └── *.json                  # 뉴스 기사 메타데이터
├── core/                       # 🧠 백엔드 (태영님 담당)
│   ├── __init__.py
│   ├── scraper.py              # 야후 파이낸스 & 뉴스 API 크롤링
│   ├── analyzer.py             # 감성분석 & 통계 검증 모듈
│   └── rag_engine.py           # RAG + LLM 기반 분석 엔진
├── ui/                         # 🎨 프론트엔드 (한빈님 담당)
│   ├── __init__.py
│   ├── components.py           # Streamlit UI 컴포넌트
│   └── charts.py               # Plotly 금융 시각화
├── app.py                      # 🚀 메인 진입점 (Streamlit 앱)
├── requirements.txt            # 의존성 명시서
├── .gitignore                  # Git 무시 목록
└── README.md                   # 이 파일
```

---

## 🚀 5분 안에 시작하기

### 1️⃣ 가상환경 활성화
```bash
cd c:\Users\gimha\source\Python\Mecro
.\.venv\Scripts\Activate.ps1
```

### 2️⃣ 의존성 설치
```bash
pip install -r requirements.txt
```

### 3️⃣ 대시보드 실행
```bash
python -m streamlit run app.py
```

🌐 브라우저에서 **http://localhost:8501** 접속

---

## ✨ 핵심 기능

### 📈 MarketEcho Index 차트
- **이중축 시각화**: 경제 지수 vs 자산 가격 실시간 비교
- **상승/하락 인디케이터**: Neon Green(상승) / Red(하락)
- **호버 정보**: 차트 위에 마우스 올리면 해당 시점 핵심 뉴스 키워드 표시

### 🎯 지능형 필터
- **자산 선택**: 국채 수익률, 금 가격, 달러 지수 중 선택
- **시간대 선택**: 1D, 1W, 1M, 3M, 1Y (버튼식 선택)
- **실시간 업데이트**: 필터 변경 시 차트& 뉴스 즉시 갱신

### 📰 뉴스 타임라인
- **기간별 자동 필터링**: 선택한 기간의 주요 뉴스만 표시
- **카테고리 태그**: 금융/거시경제/에너지/통화정책/인플레이션
- **외부 링크**: 기사 제목 클릭 → Yahoo Finance 원문 이동

### 💬 AI 해석 (준비 중 - Phase 3)
- **RAG 기반**: "왜 환율이 올랐을까?" → 관련 뉴스 검색 후 AI 분석
- **근거 제시**: 분석 결과 옆에 근거 뉴스 제시
- **자연어 처리**: 자유로운 질문 입력 가능

---

## 🛠️ 기술 스택

| 카테고리 | 기술 | 버전 |
|---------|------|------|
| **프론트엔드** | Streamlit | 1.35.0 |
| **시각화** | Plotly | 5.18.0 |
| **데이터 처리** | Pandas, NumPy | 2.2.0, 2.4.4 |
| **백엔드** | Python | 3.12.2 |
| **예정 기술** | LangChain, ChromaDB, OpenAI API | TBD |

---

## 📋 개발 로드맵

### ✅ Phase 1: MVP 완성 (완료)
- [x] Streamlit 기본 레이아웃 (3단 컬럼)
- [x] 더미 데이터 시각화
- [x] 모듈화 구조 설계
- [x] 사이드바 필터 기능

### 🔄 Phase 2: 실데이터 연결 (2-3일)
- [ ] Yfinance API 통합 (자산 가격)
- [ ] NewsAPI 통합 (뉴스 수집)
- [ ] 데이터 저장소 (CSV/JSON)
- [ ] 일일 업데이트 자동화

### 🤖 Phase 3: AI 기능 활성화 (3-4일)
- [ ] ChromaDB 벡터 스토어
- [ ] 뉴스 임베딩 & 인덱싱
- [ ] OpenAI/Claude API 연동
- [ ] RAG 파이프라인 구현

### 🔐 Phase 4: 백엔드 시스템 (3-4일)
- [ ] PostgreSQL 데이터베이스
- [ ] 사용자 인증 (로그인/가입)
- [ ] 구독 시스템 ($5/월)
- [ ] 사용자 히스토리 저장

### 🌐 Phase 5: 클라우드 배포 (1-2일)
- [ ] Streamlit Cloud 배포
- [ ] Docker 컨테이너화
- [ ] GitHub CI/CD 파이프라인
- [ ] 도메인 설정

---

## 📂 파일 가이드

### `core/scraper.py` 🧠 데이터 수집
```python
generate_market_echo_index()   # 경제 지수 시뮬레이션
generate_asset_prices()        # 자산 가격 시뮬레이션  
generate_dummy_news()          # 뉴스 데이터 생성
```
**담당**: 태영님 | **향후**: Yfinance, NewsAPI, 웹 스크래핑

### `ui/charts.py` 📊 차트 생성
```python
create_market_echo_chart()     # Plotly 이중축 차트 (MarketEcho Index + 자산)
```
**담당**: 한빈님 | **특징**: 색상 코딩, 호버 정보, 기간별 필터

### `ui/components.py` 🎨 UI 컴포넌트
```python
render_page_config()      # Streamlit 설정 (다크 테마 포함)
render_sidebar()          # 왼쪽 사이드바 (필터, 구독 상태)
render_left_metrics()     # 좌측: MarketEcho 지수 & 자산 메트릭
render_right_news()       # 우측: 뉴스 타임라인
render_footer()           # 페이지 하단
```
**담당**: 한빈님 | **특징**: 재사용 가능, 다크 테마

### `app.py` 🚀 메인 애플리케이션
**역할**:
1. 모든 모듈 임포트
2. 더미 데이터 생성
3. 3단 레이아웃 구성
4. 사용자 상호작용 처리

---

## 👥 팀 분담 & 협업 방식

| 역할 | 담당자 | 주요 파일 | 최우선 | 향후 |
|------|--------|---------|--------|------|
| **기획/설계** | 한빈님 | 전체 비전, README | UI/UX 개선 | 사용자 피드백 |
| **백엔드/데이터** | 태영님 | core/ | 데이터 파이프라인 | LLM 통합 |
| **프론트엔드** | 한빈님 | ui/ | 차트 개선 | 인터랙션 추가 |

### 💡 협업 원칙
- **코드 리뷰**: PR 전에 상호 검토
- **문제 공유**: Slack/메일로 주요 이슈 공유
- **주간 회의**: 화요일 10:00 (진행 상황 점검)

---

## 🎯 비전 & 미션

### 한 줄 미션
"**노이즈가 아닌 시그널을 찾는 투자자**를 위한 AI 분석 도구"

### 왜 MarketEcho Index인가?
- 📣 **Echo (메아리)**: 뉴스가 시장에 미치는 영향을 추적
- 🎯 **Index (지수)**: 정량화된 지표로 객관성 확보
- 🌊 **Market**: 글로벌 금융시장의 핵심 신호

### 성공의 정의
1. **Signal Detection Rate > 80%**: 주요 경제 이벤트를 지수가 90% 이상 반영
2. **사용자 만족도 > 4.5/5**: 투자자들이 실제 매매 결정에 사용
3. **DAU > 1,000명**: 월간 활성 사용자 1,000명 이상

---

## 📚 주요 문서 참고

| 문서 | 작성자 | 링크 |
|------|--------|------|
| 프로젝트 제안서 | 한빈님 | `고급인공지능_팀_프로젝트_및_작업_공간.pdf` |
| 기술 아키텍처 | 태영님 | TBD |
| 사용자 가이드 | 한빈님 | TBD |

---

## 🐛 문제 해결

### Streamlit이 안 실행될 때
```bash
# 캐시 삭제
rm -r .streamlit
# 다시 실행
python -m streamlit run app.py
```

### 포트 8501이 이미 사용 중일 때
```bash
python -m streamlit run app.py --server.port 8502
```

### 모듈 임포트 에러
```bash
# Python 경로 확인
python -c "import sys; print(sys.path)"
# 또는 재설치
pip install -r requirements.txt
```

---

## 🤝 기여하기

1. **코드 작성**: 기능 추가 후 테스트
2. **커밋**: `git commit -m "feat: 기능명"`
3. **PR 생성**: 상호 코드 리뷰
4. **머지**: 승인 후 main에 통합

---

## 📞 연락처

| 역할 | 이름 | 역할 | Slack |
|------|------|------|-------|
| PM/기획 | 한빈님 | 전체 기획 & UI/UX | @hanbin |
| 개발/분석 | 태영님 | 백엔드 & AI | @taeyoung |

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 🎉 감사의 말

### TFITH (시작이 반이다) 정신으로
- 완성도 높은 MVP부터 시작 ✅
- 빠른 실행과 지속적인 개선
- 팀 협력의 힘으로 성장

**MarketEcho Index** — Where Economics Meets AI  
*Made with ❤️ by the MECRO Team*
