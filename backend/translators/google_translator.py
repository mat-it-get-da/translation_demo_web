"""
Google Translate를 사용한 번역 모듈 (googletrans 사용)
"""

import asyncio
from fastapi import HTTPException
from googletrans import Translator


def translate(text: str, src: str, dest: str) -> str:
    """
    Google Translate를 사용하여 텍스트를 번역합니다.

    Parameters
    ----------
    text : str
        번역할 텍스트
    src : str
        원본 언어 코드 (예: "en", "auto")
    dest : str
        목표 언어 코드 (예: "ko")

    Returns
    -------
    str
        번역된 텍스트
    """
    translator = Translator()
    result = translator.translate(text, src=src, dest=dest)
    return result.text


async def translate_with_google(
    text: str,
    source_lang: str,
    target_lang: str,
) -> str:
    """
    Google Translate를 사용하여 텍스트를 번역합니다.

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
        # source_lang이 "auto"인 경우 src를 생략하거나 "auto"로 설정
        src = source_lang if source_lang != "auto" else "auto"

        # 동기 함수를 비동기로 실행
        result = await asyncio.to_thread(translate, text, src, target_lang)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Google 번역 실패: {str(e)}",
        )
