"""
상단 5단계 프로세스 바 컴포넌트
"""
import streamlit as st


STEPS = [
    {"num": 1, "title": "작업 정보 입력", "icon": "📝"},
    {"num": 2, "title": "위험요인 식별", "icon": "🔍"},
    {"num": 3, "title": "SIF 사례 적용", "icon": "📚"},
    {"num": 4, "title": "위험성평가서 작성", "icon": "📊"},
    {"num": 5, "title": "TBM 생성", "icon": "🗣️"},
]


def render_progress_bar():
    """상단 프로세스 바 렌더링"""
    current = st.session_state.current_step
    cols = st.columns(5)

    for idx, step in enumerate(STEPS):
        with cols[idx]:
            step_num = step["num"]

            if step_num < current:
                color = "#00A170"
                bg_color = "#E8F5E9"
                icon_display = "✅"
            elif step_num == current:
                color = "#0066CC"
                bg_color = "#E3F2FD"
                icon_display = step["icon"]
            else:
                color = "#9E9E9E"
                bg_color = "#F5F5F5"
                icon_display = step["icon"]

            st.markdown(
                f"""
                <div style="
                    background-color: {bg_color};
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 12px 8px;
                    text-align: center;
                    min-height: 90px;
                ">
                    <div style="font-size: 24px; margin-bottom: 4px;">
                        {icon_display}
                    </div>
                    <div style="color: {color}; font-weight: bold; font-size: 12px; margin-bottom: 2px;">
                        STEP {step_num}
                    </div>
                    <div style="color: {color}; font-size: 13px; font-weight: 500;">
                        {step["title"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)


def render_step_navigation():
    """하단 이전/다음 버튼"""
    from src.utils.session import prev_step, next_step

    current = st.session_state.current_step

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if current > 1:
            if st.button("⬅️ 이전 단계", use_container_width=True):
                prev_step()

    with col3:
        if current < 5:
            if st.button("다음 단계 ➡️", type="primary", use_container_width=True):
                next_step()
