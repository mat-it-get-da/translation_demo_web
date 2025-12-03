"""
OpenAI API를 사용한 번역 모듈
"""

import os
from openai import OpenAI
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# OpenAI 클라이언트 초기화
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    try:
        openai_client = OpenAI(api_key=openai_api_key)
        print("[OK] OpenAI 클라이언트 초기화 성공")
        print(f"[INFO] API 키: {openai_api_key[:8]}...")
    except Exception as e:
        print(f"[ERROR] OpenAI 클라이언트 초기화 실패: {e}")
        openai_client = None
else:
    print("[WARNING] OPENAI_API_KEY가 설정되지 않았습니다.")
    openai_client = None


def translate_with_openai(
    text: str,
    source_lang: str,
    target_lang: str,
    model: str,
    source_name: str,
    target_name: str,
) -> str:
    """
    OpenAI API를 사용하여 텍스트를 번역합니다.
    
    Parameters
    ----------
    text : str
        번역할 텍스트
    source_lang : str
        원본 언어 코드 (예: "en")
    target_lang : str
        목표 언어 코드 (예: "ko")
    model : str
        사용할 OpenAI 모델 ID (예: "gpt-4o-mini")
    source_name : str
        원본 언어 이름 (예: "English")
    target_name : str
        목표 언어 이름 (예: "Korean")
    
    Returns
    -------
    str
        번역된 텍스트
    
    Raises
    ------
    HTTPException
        번역 실패 시
    """
    if not openai_client:
        raise HTTPException(
            status_code=500,
            detail="OpenAI 클라이언트가 초기화되지 않았습니다. OPENAI_API_KEY를 확인하세요.",
        )
    
    # 번역 프롬프트 생성
    system_prompt = f"""You are a professional translator. Translate the given text from {source_name} to {target_name}.
Provide ONLY the translated text without any explanations or additional comments."""
    
    user_message = f"Translate this text to {target_name}:\n\n{text}"
    
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,  # 번역은 창의성이 덜 필요
            max_tokens=512,
        )
        
        translated_text = response.choices[0].message.content.strip()
        return translated_text
    
    except Exception as e:
        error_msg = str(e)
        
        # 에러 타입별 처리
        if "NOT_FOUND" in error_msg or "not found" in error_msg.lower():
            raise HTTPException(
                status_code=404,
                detail=f"모델을 찾을 수 없습니다: {model}",
            )
        elif "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            raise HTTPException(
                status_code=401,
                detail="OpenAI API 키가 유효하지 않습니다.",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"OpenAI 번역 실패: {error_msg}",
            )

