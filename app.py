"""
POSCO FUTURE M - AI 위험성평가 시스템
메인 진입점
"""
import streamlit as st
from pathlib import Path

from src.utils.session import init_session_state
from src.components.sidebar import render_sidebar
from src.components.progress_bar import render_progress_bar, render_step_navigation

# 새로 추가된 step1_input 모듈 임포트
from src.steps import step1_input

# ==================== 페이지 설정 ====================
st.set_page_config(
    page_title="POSCO FUTURE M - AI 위험성평가",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================== CSS 로드 ====================
def load_css():
    """커스텀 CSS 로드"""
    css_path = Path("assets/styles.css")
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==================== 각 스텝 렌더링 (임시) ====================
# step 1은 step1_input.py로 대체되었으므로 삭제됨

def render_step_2():
    st.header("🔍 Step 2: 위험요인 식별")
    st.info("👉 Step 4에서 구현 예정입니다.")

def render_step_3():
    st.header("📚 Step 3: SIF 사례 적용")
    st.info("👉 Step 5에서 구현 예정입니다.")

def render_step_4():
    st.header("📊 Step 4: 위험성평가서 작성")
    st.info("👉 Step 7에서 구현 예정입니다. (핵심 산출물)")

def render_step_5():
    st.header("🗣️ Step 5: TBM 카드 생성")
    st.info("👉 위험성평가서 기반으로 자동 생성 (참고용)")

# ==================== 메인 렌더링 로직 ====================
STEP_RENDERERS = {
    1: step1_input.render,  # step1_input.py의 render 함수 연결
    2: render_step_2,
    3: render_step_3,
    4: render_step_4,
    5: render_step_5,
}

def main():
    """메인 함수"""
    # 세션 초기화
    init_session_state()
    
    # CSS 로드
    load_css()
    
    # 사이드바 렌더링
    render_sidebar()
    
    # ===== 메인 영역 =====
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <h1 style="color: #0066CC; margin-bottom: 0;">
                🛡️ AI 위험성평가 시스템
            </h1>
            <p style="color: #666; margin-top: 5px;">
                작업 정보만 입력하면, AI가 위험요인부터 안전대책까지 자동 도출합니다
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 상단 프로세스 바
    render_progress_bar()
    
    # 현재 스텝 렌더링
    current_step = st.session_state.current_step
    renderer = STEP_RENDERERS.get(current_step)
    if renderer:
        renderer()
    
    # 하단 네비게이션 버튼
    render_step_navigation()

# ==================== 실행 ====================
if __name__ == "__main__":
    main()
