import openai
import streamlit as st
import json
import time

def get_hazards_from_ai(task_info):
    """OpenAI API를 호출하여 위험요인을 분석합니다."""
    
    # 1. API 키 확인 (없으면 안전장치로 임시 데이터 반환)
    if "OPENAI_API_KEY" not in st.secrets or not st.secrets["OPENAI_API_KEY"].startswith("sk-"):
        st.warning("⚠️ OpenAI API 키가 설정되지 않아 임시(Mock) 데이터를 보여드립니다. `.streamlit/secrets.toml` 파일에 키를 입력해주세요.")
        time.sleep(1)
        return [
            {"위험분류": "떨어짐", "위험요인": "[임시] 비계 위 작업 중 발판 불량으로 인한 떨어짐", "현재_안전조치": "안전대 지급"},
            {"위험분류": "끼임", "위험요인": "[임시] 크레인 하물과 구조물 사이에 끼임", "현재_안전조치": "신호수 배치"}
        ]
    
    # 2. OpenAI 클라이언트 생성
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    
    # 3. AI에게 내릴 명령(프롬프트) 작성
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
            {{"위험분류": "떨어짐/끼임/넘어짐/부딪힘/화재/폭발/감전/질식/기타 중 택1", "위험요인": "구체적인 위험 상황 설명", "현재_안전조치": "필요한 안전조치"}}
        ]
    }}
    """
    
    try:
        # 4. AI 호출 (빠르고 똑똑한 gpt-4o-mini 모델 사용)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful safety expert. Output strictly in JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        # 5. 결과 파싱 (JSON 텍스트를 파이썬 딕셔너리로 변환)
        result_text = response.choices[0].message.content
        result_json = json.loads(result_text)
        return result_json.get("hazards", [])
        
    except Exception as e:
        st.error(f"AI 분석 중 오류가 발생했습니다: {e}")
        return []
