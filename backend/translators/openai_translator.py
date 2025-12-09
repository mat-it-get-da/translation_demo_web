"""
OpenAI API를 사용한 번역 모듈
"""

import os
import asyncio
from openai import OpenAI
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# OpenAI 클라이언트
openai_client: OpenAI | None = None


def get_openai_client():
    """OpenAI 클라이언트를 반환합니다. 초기화되지 않았다면 자동으로 초기화합니다."""
    global openai_client

    if openai_client is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")

        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")

        openai_client = OpenAI(api_key=openai_api_key)
        print("[OK] OpenAI 클라이언트 초기화 성공")
        print(f"[INFO] API 키: {openai_api_key[:8]}...")

    return openai_client


async def translate_with_openai(
    text: str,
    source_lang: str,
    target_lang: str,
    model: str,
) -> str:
    """
    OpenAI API를 사용하여 텍스트를 번역합니다.

    Parameters
    ----------
    text : str
        번역할 텍스트
    source_lang : str
        원본 언어 코드 (예: "en", "ko")
    target_lang : str
        목표 언어 코드 (예: "en", "ko")
    model : str
        사용할 OpenAI 모델 ID (예: "gpt-4o-mini")

    Returns
    -------
    str
        번역된 텍스트

    Raises
    ------
    HTTPException
        번역 실패 시
    """
    try:
        # 클라이언트 가져오기 (자동 초기화)
        client = get_openai_client()

        # 번역 프롬프트 생성
        system_prompt = """You are a professional translator. Translate the given text from the source language to the target language.

IMPORTANT CONSTRAINTS:
- You MUST use the full language names (e.g., "English", "Korean", "Japanese") in your response, NOT language codes (e.g., "en", "ko", "ja")
- When referring to languages in your translation output, always use the complete language name
- Provide ONLY the translated text without any explanations, additional comments, or language code annotations
- The translation should be natural and fluent in the target language"""

        user_message = f"""Translate the following text from {source_lang} to {target_lang}.

Text to translate:
{text}

Remember: Use full language names (not codes) when referring to languages, and provide only the translated text."""

        # 동기 함수를 비동기로 실행
        response = await asyncio.to_thread(
            client.chat.completions.create,
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.3,
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
