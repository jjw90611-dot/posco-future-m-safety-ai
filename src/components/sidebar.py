"""
사이드바 네비게이션 컴포넌트
"""
import streamlit as st
from src.utils.session import reset_session, go_to_step


def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding: 10px 0;">
                <h2 style="color: #0066CC; margin: 0;">
                    🛡️ POSCO FUTURE M
                </h2>
                <p style="color: #666; font-size: 13px; margin: 5px 0;">
                    AI 위험성평가 시스템
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown("### 📋 메뉴")

        if st.button("🆕 새 평가서 작성", use_container_width=True):
            reset_session()

        if st.button("📁 나의 평가서", use_container_width=True):
            st.session_state.view = "my_assessments"

        if st.button("📊 대시보드", use_container_width=True):
            st.session_state.view = "dashboard"

        st.markdown("---")
        st.markdown("### 🚀 빠른 이동")

        step_options = {
            "1. 작업 정보 입력": 1,
            "2. 위험요인 식별": 2,
            "3. SIF 사례 적용": 3,
            "4. 위험성평가서 작성": 4,
            "5. TBM 생성": 5,
        }
        selected = st.selectbox(
            "단계 선택",
            options=list(step_options.keys()),
            index=st.session_state.current_step - 1,
            label_visibility="collapsed",
        )
        if step_options[selected] != st.session_state.current_step:
            go_to_step(step_options[selected])

        st.markdown("---")
        st.markdown("### ⚙️ 설정")

        with st.expander("📖 사용 매뉴얼"):
            st.markdown("""
            **사용 순서:**
            1. 작업 정보를 입력하세요
            2. AI가 위험요인을 식별합니다
            3. 유사 SIF 사례를 참고하세요
            4. 위험성평가서를 완성하세요
            5. TBM 카드를 생성/공유하세요
            """)

        with st.expander("ℹ️ 시스템 정보"):
            st.markdown("""
            - **버전**: v0.1.0 (개발중)
            - **최종 업데이트**: 2025.01
            """)

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.caption("© 2025 POSCO FUTURE M")
