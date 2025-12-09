"""
DeepL을 사용한 번역 모듈
"""

import os
import asyncio
from fastapi import HTTPException
from dotenv import load_dotenv

from deepl import Translator

load_dotenv()

# DeepL 클라이언트
deepl_translator: Translator | None = None


def get_deepl_client():
    """
    DeepL 클라이언트를 반환합니다. 초기화되지 않았다면 자동으로 초기화합니다.

    Returns
    -------
    Translator
        초기화된 DeepL Translator 클라이언트

    Raises
    ------
    ValueError
        DEEPL_API_KEY가 설정되지 않은 경우
    """
    global deepl_translator

    if deepl_translator is None:
        deepl_api_key = os.getenv("DEEPL_API_KEY")

        if not deepl_api_key:
            raise ValueError("DEEPL_API_KEY가 설정되지 않았습니다.")

        deepl_translator = Translator(deepl_api_key)
        print("[OK] DeepL 클라이언트 초기화 성공")

    return deepl_translator


async def translate_with_deepl(
    text: str,
    source_lang: str,
    target_lang: str,
) -> str:
    """
    DeepL을 사용하여 텍스트를 번역합니다.

    Parameters
    ----------
    text : str
        번역할 텍스트
    source_lang : str
        원본 언어 코드 (예: "en", "auto"면 자동 감지)
    target_lang : str
        목표 언어 코드 (예: "ko")

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
        client = get_deepl_client()

        # DeepL은 언어 코드를 대문자로 사용
        source_lang_upper = source_lang.upper() if source_lang != "auto" else None
        target_lang_upper = target_lang.upper()

        # DeepL 특수 처리 (EN -> EN-US, PT -> PT-BR 등)
        if target_lang_upper == "EN":
            target_lang_upper = "EN-US"
        elif target_lang_upper == "PT":
            target_lang_upper = "PT-BR"

        # 동기 함수를 비동기로 실행
        result = await asyncio.to_thread(
            client.translate_text,
            text,
            source_lang=source_lang_upper,
            target_lang=target_lang_upper,
        )

        return result.text

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"DeepL 번역 실패: {str(e)}",
        )
