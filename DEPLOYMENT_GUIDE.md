# Vercel 배포 체크리스트 및 설정 가이드

## 📋 배포 전 체크리스트

### 1단계: 로컬 환경 최종 확인
- [ ] `requirements.txt` 정제 완료 (필수 패키지만 포함)
- [ ] `vercel.json` 생성 완료
- [ ] `runtime.txt` 생성 완료
- [ ] `api/index.py` 생성 완료
- [ ] `.gitignore` 수정 완료 (data/ 폴더 포함)
- [ ] `.streamlit/config.toml` 생성 완료

### 2단계: Git 커밋 및 푸시
```bash
# 모든 변경사항 스테이징
git add .

# 병합 전 feature 브랜치에서 커밋
git commit -m "feat: Vercel 배포 설정 추가 (requirements.txt 정제, vercel.json, api/index.py)"

# main 브랜치로 변경
git checkout main

# feature 브랜치를 main으로 병합
git merge feature/data-factory

# 원격 저장소에 푸시
git push origin main
```

### 3단계: Vercel 연결 및 배포
- [ ] Vercel 대시보드 접속 (https://vercel.com)
- [ ] "Import Project" 클릭
- [ ] GitHub 저장소 선택
- [ ] 프로젝트 설정:
  - Framework: "Other"
  - Build Command: `pip install -r requirements.txt`
  - Output Directory: `.streamlit`
  - Install Command: `pip install -r requirements.txt`

### 4단계: 환경 변수 등록 (필요 시)
Vercel Dashboard → Settings → Environment Variables에 추가:
```
# OpenAI API 키 (RAG 엔진 준비)
OPENAI_API_KEY=sk-...

# LangChain API 키 (미래 사용)
LANGCHAIN_API_KEY=...

# 기타 필요한 API 키
```

### 5단계: 배포 모니터링
- [ ] Deployment 로그 확인
- [ ] 빌드 오류 확인
- [ ] 배포 완료 후 URL 테스트

---

## 🔧 파일 구조 (Vercel 배포용)

```
NewsDoc/
├── api/
│   └── index.py              # Vercel 브릿지 파일 (이 파일에서 Streamlit 실행)
├── core/
│   ├── analyzer.py
│   ├── rag_engine.py
│   └── scraper.py
├── ui/
│   ├── charts.py
│   └── components.py
├── data/
│   └── raw/
│       ├── market_prices.csv # 배포 시 포함 (샘플 데이터)
│       └── raw_news.csv      # 배포 시 포함 (샘플 데이터)
├── .streamlit/
│   └── config.toml           # Streamlit 설정
├── app.py                    # 로컬 실행용 (참고만)
├── requirements.txt          # 정제된 의존성 (5개 패키지)
├── vercel.json              # Vercel 설정
├── runtime.txt              # Python 버전
└── .gitignore               # data/ 폴더 포함하도록 수정

```

---

## ⚠️ 주의사항

1. **데이터 영구 저장**: 
   - Vercel은 서버리스 환경이므로 배포 후 생성되는 파일은 저장되지 않음
   - 새로운 데이터는 외부 DB (Supabase, MongoDB 등)에 저장해야 함

2. **환경 변수**:
   - 코드에 API 키를 직접 작성하면 안 됨
   - 반드시 Vercel 대시보드의 Environment Variables에 등록

3. **빌드 시간**:
   - 첫 빌드는 5~10분 소요 가능
   - 패키지가 많으면 더 오래 걸릴 수 있음

4. **메모리 제한**:
   - Vercel 함수는 3GB 메모리 제한
   - 대용량 데이터 처리 시 최적화 필요

---

## 🚀 배포 후 다음 스텝

1. **MarketEcho Index 계산 로직** 구현 (core/analyzer.py)
2. **RAG 엔진** 연결 (core/rag_engine.py + OpenAI)
3. **외부 DB** 연결 (Supabase 또는 MongoDB)
4. **자동 데이터 갱신** 스케줄링 (GitHub Actions 또는 cronjob)

---

## 💬 트러블슈팅

### 배포 실패 (Build Error)
- [ ] `requirements.txt` 문법 확인
- [ ] Python 버전 호환성 확인
- [ ] 의존성 충돌 확인

### 런타임 오류 (Runtime Error)
- [ ] 로그 확인: Vercel Dashboard → Deployments
- [ ] 환경 변수 누락 확인
- [ ] 파일 경로 확인 (상대 경로 사용)

### Streamlit 실행 안 됨
- [ ] `api/index.py` 생성 확인
- [ ] `vercel.json` 설정 확인
- [ ] 포트 번호 (기본 8501) 확인

