import os
import openai
import streamlit as st
import json
import time

# 사내망(aigpt.posco.net) 접속 시 외부 프록시를 거치지 않도록 설정
os.environ['NO_PROXY'] = 'aigpt.posco.net'
os.environ['no_proxy'] = 'aigpt.posco.net'

def get_posco_client():
    """포스코 사내 API 가이드에 맞춘 클라이언트 생성"""
    api_key = os.environ.get("PGPT_API_KEY")
    
    if not api_key and "PGPT_API_KEY" in st.secrets:
        api_key = st.secrets["PGPT_API_KEY"]
        
    if not api_key:
        st.warning("⚠️ API 키(PGPT_API_KEY)가 설정되지 않았습니다.")
        return None
    
    try:
        # 가이드라인과 동일한 순정 클라이언트 설정
        client = openai.OpenAI(
            api_key=api_key, 
            base_url="http://aigpt.posco.net/gpgpta01-gpt/v1"
        )
        return client
    except Exception as e:
        st.error(f"🚨 클라이언트 생성 중 오류 발생: {e}")
        return None

def get_hazards_from_ai(task_info):
    """OpenAI API를 호출하여 위험요인을 분석합니다."""
    client = get_posco_client()
    if not client: return []
    
    prompt = f"""
    당신은 포스코퓨처엠의 산업안전보건 전문가입니다. 
    다음 작업 정보를 바탕으로 발생 가능한 위험요인과 현재 필요한 안전조치를 도출해주세요.
    반드시 아래 JSON 형식으로만 답변해주세요.
    
    [작업 정보]
    - 공정/부서: {task_info.get('department', '')}
    - 작업명: {task_info.get('task_name', '')}
    - 작업내용: {task_info.get('task_desc', '')}
    - 사용장비/도구: {task_info.get('tools', '')}
    
    [출력 형식 (JSON)]
    {{
        "hazards": [
            {{"위험분류": "떨어짐/끼임/부딪힘/맞음/넘어짐/화재/폭발/감전/질식/기타 중 택1", "위험요인": "구체적인 위험 상황 설명", "현재_안전조치": "필요한 안전조치"}}
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2", 
            messages=[
                {"role": "system", "content": "You are a helpful safety expert. Output strictly in JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        return json.loads(result_text).get("hazards", [])
        
    except Exception as e:
        st.error(f"🚨 AI 분석 중 통신 오류가 발생했습니다: {str(e)}")
        return []

def get_sif_analysis_from_ai(hazards):
    """도출된 위험요인을 바탕으로 중대재해(SIF) 가능성을 분석합니다."""
    client = get_posco_client()
    if not client: return []
    
    prompt = f"""
    당신은 포스코퓨처엠의 산업안전보건 전문가입니다.
    다음은 식별된 위험요인 리스트입니다. 이 중 '중대재해(SIF)'로 이어질 가능성이 높은 항목을 선별하고 평가해주세요.
    반드시 아래 JSON 형식으로만 답변해주세요.
    
    [위험요인 리스트]
    {json.dumps(hazards, ensure_ascii=False)}
    
    [출력 형식 (JSON)]
    {{
        "sif_analysis": [
            {{"위험요인": "원래 위험요인 내용", "SIF_해당여부": "O 또는 X", "SIF_사례_및_이유": "왜 SIF에 해당하는지 또는 관련 사례", "강화된_안전조치": "기존보다 강화된 추가 안전조치"}}
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-5.2", 
            messages=[
                {"role": "system", "content": "You are a helpful safety expert. Output strictly in JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        result_text = result_text.replace("```json", "").replace("```", "").strip()
        return json.loads(result_text).get("sif_analysis", [])
        
    except Exception as e:
        st.error(f"🚨 SIF 분석 중 통신 오류가 발생했습니다: {str(e)}")
        return []
