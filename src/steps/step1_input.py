import streamlit as st
from datetime import datetime

def render():
    st.header("📝 Step 1: 작업 정보 입력")
    st.markdown("위험성평가를 진행할 작업의 기본 정보를 입력해주세요. 상세히 적을수록 AI가 더 정확한 위험요인을 도출합니다.")

    # 세션 스테이트 초기화 (입력 데이터 유지용)
    if "task_info" not in st.session_state:
        st.session_state.task_info = {
            "date": datetime.today(),
            "department": "양극재생산부",
            "task_name": "",
            "task_desc": "",
            "tools": ""
        }

    # 입력 폼 생성
    with st.form("task_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("작업 일자", value=st.session_state.task_info["date"])
            department = st.selectbox(
                "담당 부서", 
                ["양극재생산부", "음극재생산부", "설비기술부", "품질관리부", "안전환경부", "기타"],
                index=["양극재생산부", "음극재생산부", "설비기술부", "품질관리부", "안전환경부", "기타"].index(st.session_state.task_info["department"])
            )
        
        with col2:
            task_name = st.text_input("작업명", value=st.session_state.task_info["task_name"], placeholder="예: 소성로 내화물 교체 작업")
            tools = st.text_input("사용 장비/도구", value=st.session_state.task_info["tools"], placeholder="예: 크레인, 용접기, 수공구")

        task_desc = st.text_area(
            "작업 상세 설명", 
            value=st.session_state.task_info["task_desc"], 
            placeholder="작업의 순서, 방법, 작업 장소의 특징 등을 상세히 적어주세요.",
            height=150
        )

        # 제출 버튼
        submitted = st.form_submit_button("저장 및 다음 단계로", type="primary")

        if submitted:
            if not task_name or not task_desc:
                st.warning("⚠️ 작업명과 작업 상세 설명은 필수 입력 항목입니다.")
            else:
                # 세션 스테이트에 데이터 저장
                st.session_state.task_info.update({
                    "date": date,
                    "department": department,
                    "task_name": task_name,
                    "task_desc": task_desc,
                    "tools": tools
                })
                st.success("✅ 작업 정보가 성공적으로 저장되었습니다!")
                
                # 다음 스텝(Step 2)으로 자동 이동
                st.session_state.current_step = 2
                st.rerun()
