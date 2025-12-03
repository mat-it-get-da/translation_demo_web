"""
Google Translate를 사용한 번역 모듈 (deep-translator 사용)
"""

from fastapi import HTTPException

try:
    from deep_translator import GoogleTranslator
    GOOGLE_AVAILABLE = True
    print("[OK] Google Translate 모듈 로드 성공 (deep-translator)")
except ImportError:
    GOOGLE_AVAILABLE = False
    print("[WARNING] deep-translator가 설치되지 않았습니다.")
    print("[INFO] 설치: rye add deep-translator")


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
    if not GOOGLE_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="Google Translate가 설치되지 않았습니다. deep-translator 패키지를 설치하세요.",
        )
    
    try:
        # deep-translator의 GoogleTranslator 사용
        translator = GoogleTranslator(
            source=source_lang if source_lang != "auto" else "auto",
            target=target_lang,
        )
        result = translator.translate(text)
        return result
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Google 번역 실패: {str(e)}",
        )
