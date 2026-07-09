import openai
import streamlit as st
import json
import time
import base64

def get_posco_client():
    """포스코 사내 API용 클라이언트 생성 (Base64 + Bearer 토큰)"""
    if "OPENAI_API_KEY" not in st.secrets or not st.secrets["OPENAI_API_KEY"]:
        return None
        
    api_key = st.secrets["OPENAI_API_KEY"]
    company_code = st.secrets.get("COMPANY_CODE", "01") # 설정이 없으면 기본값 "01"
    
    # 1. Base64 변환 (놀이공원 팔찌 만들기)
    raw_token = f"{api_key}:{company_code}"
    encoded_token = base64.b64encode(raw_token.encode('utf-8')).decode('utf-8')
    
    # 2. 사내 API 클라이언트 설정
    # (주의: 사내 API 전용 URL이 별도로 있다면 아래 base_url 주석을 풀고 주소를 입력하세요)
    client = openai.OpenAI(
        api_key=api_key, 
        default_headers={"Authorization": f"Bearer {encoded_token}"}
        # base_url="https://사내_API_주소/v1" 
    )
    return client

def get_hazards_from_ai(task_info):
    """OpenAI API를 호출하여 위험요인을 분석합니다."""
    client = get_posco_client()
    
    if not client:
        st.warning("⚠️ API 키가 설정되지 않아 임시(Mock) 데이터를 보여드립니다.")
        time.sleep(1)
        return [
            {"위험분류": "추락", "위험요인": "[임시] 비계 위 작업 중 발판 불량으로 인한 추락", "현재_안전조치": "안전대 지급"},
            {"위험분류": "협착", "위험요인": "[임시] 크레인 하물과 구조물 사이에 끼임", "현재_안전조치": "신호수 배치"}
        ]
    
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
            {{"위험분류": "추락/협착/전도/충돌/화재/폭발/감전/질식/기타 중 택1", "위험요인": "구체적인 위험 상황 설명", "현재_안전조치": "필요한 안전조치"}}
        ]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # 사내에서 지원하는 모델명으로 변경이 필요할 수 있습니다.
            messages=[
                {"role": "system", "content": "You are a helpful safety expert. Output strictly in JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        return result_json.get("hazards", [])
        
    except Exception as e:
        st.error(f"AI 분석 중 오류가 발생했습니다: {e}")
        return []

def get_sif_analysis_from_ai(hazards):
    """도출된 위험요인을 바탕으로 중대재해(SIF) 가능성을 분석합니다."""
    client = get_posco_client()
    
    if not client:
        time.sleep(1)
        return [
            {"위험요인": hazards[0].get("위험요인", "[임시]"), "SIF_해당여부": "O", "SIF_사례_및_이유": "[임시] 과거 유사 추락 사망사고 발생 이력 있음", "강화된_안전조치": "2중 안전대 체결 및 생명줄 설치"}
        ]
    
    prompt = f"""
    당신은 포스코퓨처엠의 산업안전보건 전문가입니다.
    다음은 식별된 위험요인 리스트입니다. 이 중 '중대재해(SIF, 사망 또는 심각한 장애를 초래할 수 있는 사고)'로 이어질 가능성이 높은 항목을 선별하고 평가해주세요.
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
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful safety expert. Output strictly in JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        return result_json.get("sif_analysis", [])
        
    except Exception as e:
        st.error(f"SIF 분석 중 오류가 발생했습니다: {e}")
        return []
