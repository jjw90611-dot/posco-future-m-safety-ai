import os
import openai
import streamlit as st
import json
import time
import httpx  # 추가됨

def get_posco_client():
    """포스코 사내 API 가이드에 맞춘 클라이언트 생성 (프록시 완벽 차단)"""
    
    api_key = os.environ.get("PGPT_API_KEY")
    
    if not api_key and "PGPT_API_KEY" in st.secrets:
        api_key = st.secrets["PGPT_API_KEY"]
        
    if not api_key:
        st.warning("⚠️ API 키(PGPT_API_KEY)가 설정되지 않았습니다.")
        return None
    
    try:
        # 💡 핵심 조치: 파이썬이 사내 프록시를 절대 타지 않도록 강제 설정
        custom_http_client = httpx.Client(
            proxies=None,      # 프록시 사용 안 함
            trust_env=False    # 윈도우 시스템의 프록시 환경변수 무시
        )
        
        client = openai.OpenAI(
            api_key=api_key, 
            base_url="http://aigpt.posco.net/gpgpta01-gpt/v1",
            http_client=custom_http_client  # 커스텀 클라이언트 주입
        )
        return client
    except Exception as e:
        st.error(f"🚨 클라이언트 생성 중 오류 발생: {e}")
        return None

# (이하 get_hazards_from_ai 등 나머지 함수는 기존과 동일하게 유지)
