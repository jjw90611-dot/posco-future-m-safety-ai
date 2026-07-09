import streamlit as st
import pandas as pd
from src.utils.ai import get_hazards_from_ai

def render():
    st.header("🔍 Step 2: 위험요인 식별")
    
    if "task_info" not in st.session_state or not st.session_state.task_info.get("task_name"):
        st.warning("⚠️ Step 1에서 작업 정보를 먼저 입력해주세요.")
        return

    task = st.session_state.task_info
    
    st.markdown(f"**대상 작업:** `{task['task_name']}` ({task['department']})")
    st.markdown("입력된 작업 정보를 바탕으로 AI가 잠재적인 위험요인을 분석합니다.")

    # AI 분석 버튼
    if st.button("🤖 AI 위험요인 분석 실행", type="primary"):
        with st.spinner("AI가 작업 정보를 분석하여 위험요인을 도출하고 있습니다... (약 3~5초 소요)"):
            
            # utils/ai.py 에 작성한 함수를 호출하여 진짜 AI 결과 받아오기
            ai_hazards = get_hazards_from_ai(task)
            
            if ai_hazards:
                st.session_state.hazards = ai_hazards
                st.success("✅ AI 분석이 완료되었습니다!")
            else:
                st.warning("결과를 가져오지 못했습니다. 다시 시도해주세요.")

    # 분석 결과 출력 및 편집기 제공
    if "hazards" in st.session_state and st.session_state.hazards:
        st.subheader("📋 도출된 위험요인 리스트")
        st.caption("💡 AI가 도출한 결과를 확인하고, 필요시 직접 내용을 수정하거나 행을 추가/삭제할 수 있습니다.")
        
        df = pd.DataFrame(st.session_state.hazards)
        
        edited_df = st.data_editor(
            df, 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "위험분류": st.column_config.SelectboxColumn(
                    "위험분류",
                    options=["추락", "협착", "전도", "충돌", "화재", "폭발", "감전", "질식", "기타"],
                    required=True
                ),
                "위험요인": st.column_config.TextColumn("위험요인 (상세)", required=True),
                "현재_안전조치": st.column_config.TextColumn("현재 안전조치", required=True)
            }
        )
        
        st.session_state.hazards = edited_df.to_dict('records')

        st.markdown("---")
        if st.button("저장 및 다음 단계로 (SIF 사례 적용)"):
            st.session_state.current_step = 3
            st.rerun()
