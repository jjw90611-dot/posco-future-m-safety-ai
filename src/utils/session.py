"""
세션 상태 초기화 및 관리
"""
import streamlit as st


def init_session_state():
    """앱 시작 시 세션 상태 초기화"""
    if "current_step" not in st.session_state:
        st.session_state.current_step = 1

    if "work_info" not in st.session_state:
        st.session_state.work_info = {
            "work_name": "",
            "work_description": "",
            "department": "",
            "location": "",
            "worker_count": 0,
            "work_date": None,
        }

    if "hazards" not in st.session_state:
        st.session_state.hazards = []

    if "selected_sif" not in st.session_state:
        st.session_state.selected_sif = []

    if "processes" not in st.session_state:
        st.session_state.processes = []

    if "assessment" not in st.session_state:
        st.session_state.assessment = []

    if "tbm_card" not in st.session_state:
        st.session_state.tbm_card = {}

    if "saved_assessments" not in st.session_state:
        st.session_state.saved_assessments = []


def go_to_step(step_num: int):
    if 1 <= step_num <= 5:
        st.session_state.current_step = step_num
        st.rerun()


def next_step():
    if st.session_state.current_step < 5:
        st.session_state.current_step += 1
        st.rerun()


def prev_step():
    if st.session_state.current_step > 1:
        st.session_state.current_step -= 1
        st.rerun()


def reset_session():
    keys_to_reset = [
        "current_step", "work_info", "hazards",
        "selected_sif", "processes", "assessment", "tbm_card"
    ]
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]
    init_session_state()
