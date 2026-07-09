# 🛡️ POSCO FUTURE M - AI 위험성평가 시스템

포스코퓨처엠의 이차전지소재·첨단화학·산업기초소재 사업장을 위한 
AI 기반 위험성평가 자동화 도구입니다.

## ✨ 주요 기능

- 🔍 **AI 위험요인 자동 식별**: 작업 설명만으로 잠재 위험 도출
- 📚 **SIF 사례 검색**: 4,400건 이상의 중대재해 사례 참조
- 📊 **5×5 위험성 매트릭스**: KOSHA 표준 기반 등급 산정
- 📤 **원클릭 내보내기**: Excel/PDF 결재 문서 자동 생성

## 🚀 실행 방법

### 로컬 실행
```bash
# 1. 저장소 복제
git clone https://github.com/[YOUR_ID]/posco-future-m-safety-air.git
cd posco-future-m-safety-air

# 2. 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 환경변수 설정
cp .env.example .env
# .env 파일 편집하여 API 키 입력

# 5. 실행
streamlit run app.py
```

## 📋 사용 흐름

1. **작업 정보 입력** → 2. **위험요인 식별** → 3. **SIF 사례 적용**  
→ 3.5. **공정 리뷰** → 4. **평가서 작성** → 5. **TBM 생성**

## 🏗️ 기술 스택

- **Frontend**: Streamlit
- **AI**: OpenAI GPT-4 / Anthropic Claude
- **Data**: JSON, Pandas
- **Deploy**: Streamlit Cloud

## 📜 라이선스

Copyright © 2025 POSCO FUTURE M. All rights reserved.
