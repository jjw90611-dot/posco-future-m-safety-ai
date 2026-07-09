import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="AI 위험성평가 시스템 | POSCO FUTURE M",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 폰트 및 글자 크기 변경 CSS 주입
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');
    
    /* 전체 폰트 적용 및 기본 글자 크기 확대 */
    * {
        font-family: 'Nanum Gothic', sans-serif !important;
    }
    p, div, span, li, input, textarea, select {
        font-size: 16px !important;
    }
    h1 { font-size: 2.5rem !important; }
    h2 { font-size: 2.0rem !important; }
    h3 { font-size: 1.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# 사이드바 구성
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c6/Posco_logo.svg/512px-Posco_logo.svg.png", width=150)
    st.markdown("### AI 위험성평가 시스템")
    st.divider()
    
    st.markdown("### 📋 메뉴")
    st.button("🆕 새 평가서 작성", use_container_width=True)
    st.button("📁 나의 평가서", use_container_width=True)
    st.button("📊 대시보드", use_container_width=True)
    
    st.divider()
    st.markdown("### ⚙️ 설정")
    st.button("📖 사용 매뉴얼", use_container_width=True)
    
    # 연도 2026년으로 수정됨!
    st.markdown("<br><br><br><br><br><p style='text-align: center; color: gray; font-size: 12px !important;'>© 2026 POSCO FUTURE M</p>", unsafe_allow_html=True)

# 메인 화면 타이틀
st.title("🛡️ AI 위험성평가 시스템")
st.markdown("작업 정보만 입력하면, AI가 위험요인부터 안전대책까지 자동 도출합니다.")

# 프로세스 바 (임시 텍스트)
st.info("상단 프로세스 바 및 페이지 이동 기능은 다음 단계에서 연결됩니다.")

# Step 1 화면 불러오기
from pages import step1
step1.render()
