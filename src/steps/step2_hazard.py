import streamlit as st
import time
import pandas as pd

def render():
    st.header("🔍 Step 2: 위험요인 식별")
    
    # Step 1에서 입력한 정보 확인
    if "task_info" not in st.session_state or not st.session_state.task_info.get("task_name"):
        st.warning("⚠️ Step 1에서 작업 정보를 먼저 입력해주세요.")
        return

    task = st.session_state.task_info
    
    st.markdown(f"**대상 작업:** `{task['task_name']}` ({task['department']})")
    st.markdown("입력된 작업 정보를 바탕으로 AI가 잠재적인 위험요인을 분석합니다.")

    # AI 분석 버튼
    if st.button("🤖 AI 위험요인 분석 실행", type="primary"):
        with st.spinner("AI가 KOSHA 데이터베이스와 과거 사례를 분석 중입니다..."):
            time.sleep(2) # 가짜 지연 시간 (추후 실제 API 연동 시 제거)
            
            # 임시(Mock) 데이터 생성
            mock_hazards = [
                {"위험분류": "추락", "위험요인": "비계 위 작업 중 발판 불량으로 인한 추락", "현재_안전조치": "안전대 지급"},
                {"위험분류": "협착", "위험요인": "크레인 하물과 구조물 사이에 끼임", "현재_안전조치": "신호수 배치"},
                {"위험분류": "화재", "위험요인": "용접 불티 비산으로 인한 주변 가연물 화재", "현재_안전조치": "소화기 비치"}
            ]
            st.session_state.hazards = mock_hazards
            st.success("✅ AI 분석이 완료되었습니다!")

    # 분석 결과 출력 및 편집기 제공
    if "hazards" in st.session_state:
        st.subheader("📋 도출된 위험요인 리스트")
        st.caption("💡 AI가 도출한 결과를 확인하고, 필요시 직접 내용을 수정하거나 행을 추가/삭제할 수 있습니다.")
        
        df = pd.DataFrame(st.session_state.hazards)
        
        # 데이터프레임 편집 가능하게 표시 (사용자가 수정/추가 가능하도록)
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
        
        # 변경된 데이터를 세션에 다시 저장
        st.session_state.hazards = edited_df.to_dict('records')

        st.markdown("---")
        if st.button("저장 및 다음 단계로 (SIF 사례 적용)"):
            st.session_state.current_step = 3
            st.rerun()
