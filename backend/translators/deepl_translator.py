"""
DeepL을 사용한 번역 모듈
"""

import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

try:
    import deepl
    DEEPL_AVAILABLE = True
    print("[OK] DeepL 모듈 로드 성공")
except ImportError:
    DEEPL_AVAILABLE = False
    print("[WARNING] deepl이 설치되지 않았습니다.")
    print("[INFO] 설치: rye add deepl")

# DeepL 클라이언트
deepl_translator = None


def init_deepl_client():
    """DeepL 클라이언트를 초기화합니다."""
    global deepl_translator
    
    if not DEEPL_AVAILABLE:
        print("[WARNING] DeepL 라이브러리가 없어 초기화를 건너뜁니다.")
        return
    
    deepl_api_key = os.getenv("DEEPL_API_KEY")
    
    if deepl_api_key:
        try:
            deepl_translator = deepl.Translator(deepl_api_key)
            print("[OK] DeepL 클라이언트 초기화 성공")
        except Exception as e:
            print(f"[ERROR] DeepL 클라이언트 초기화 실패: {e}")
            deepl_translator = None
    else:
        print("[WARNING] DEEPL_API_KEY가 설정되지 않았습니다.")


def translate_with_deepl(
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
    if not DEEPL_AVAILABLE:
        raise HTTPException(
            status_code=503,
            detail="DeepL이 설치되지 않았습니다. deepl 패키지를 설치하세요.",
        )
    
    if not deepl_translator:
        raise HTTPException(
            status_code=503,
            detail="DeepL 클라이언트가 초기화되지 않았습니다. DEEPL_API_KEY를 확인하세요.",
        )
    
    try:
        # DeepL은 언어 코드를 대문자로 사용
        source_lang_upper = source_lang.upper() if source_lang != "auto" else None
        target_lang_upper = target_lang.upper()
        
        # DeepL 특수 처리 (EN -> EN-US, PT -> PT-BR 등)
        if target_lang_upper == "EN":
            target_lang_upper = "EN-US"
        elif target_lang_upper == "PT":
            target_lang_upper = "PT-BR"
        
        result = deepl_translator.translate_text(
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

