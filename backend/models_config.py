"""
OpenAI API 모델 설정 및 매핑

프론트엔드에 표시될 모델명과 실제 OpenAI 모델 ID를 매핑합니다.
"""

from typing import Dict, List

# 사용 가능한 OpenAI 모델 정의
AVAILABLE_MODELS: Dict[str, Dict[str, str]] = {
    "gpt-3.5-turbo": {
        "display_name": "GPT-3.5 Turbo",
        "description": "OpenAI의 가성비 좋은 모델 - 빠른 응답 속도",
    },
    "gpt-4o-mini": {
        "display_name": "GPT-4o Mini",
        "description": "OpenAI의 빠르고 저렴한 최신 모델 - 번역에 최적화",
    },
    "gpt-4o": {
        "display_name": "GPT-4o",
        "description": "OpenAI의 가장 강력한 모델 - 최고 품질 번역",
    },
}

# 언어 코드 매핑 (전체 이름 -> 코드)
LANGUAGE_MAPPING: Dict[str, str] = {
    "한국어": "ko",
    "English": "en",
    "日本語": "ja",
    "中文": "zh",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
}

# 역 매핑 (코드 -> 전체 이름)
LANGUAGE_NAMES: Dict[str, str] = {
    "ko": "Korean",
    "en": "English",
    "ja": "Japanese",
    "zh": "Chinese",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
}


def get_model_list() -> List[Dict[str, str]]:
    """
    프론트엔드에서 사용할 모델 목록 반환
    
    Returns
    -------
    List[Dict[str, str]]
        모델 정보 리스트
    """
    return [
        {
            "id": model_id,
            "name": info["display_name"],
            "description": info.get("description", ""),
        }
        for model_id, info in AVAILABLE_MODELS.items()
    ]


def get_full_model_name(model_id: str) -> str:
    """
    모델 ID 유효성 검사 및 반환
    
    OpenAI API는 모델 ID를 그대로 사용하므로 
    유효성 검사 후 동일한 ID를 반환합니다.
    
    Parameters
    ----------
    model_id : str
        모델 ID (예: "gpt-4o-mini")
    
    Returns
    -------
    str
        검증된 모델 ID (입력값과 동일)
    
    Raises
    ------
    ValueError
        유효하지 않은 모델 ID인 경우
    """
    if model_id not in AVAILABLE_MODELS:
        available = ", ".join(AVAILABLE_MODELS.keys())
        raise ValueError(
            f"Invalid model_id: {model_id}. Available models: {available}"
        )
    
    return model_id


def get_language_code(language_name: str) -> str:
    """
    언어 전체 이름을 코드로 변환
    
    Parameters
    ----------
    language_name : str
        언어 전체 이름 (예: "한국어", "English")
    
    Returns
    -------
    str
        언어 코드 (예: "ko", "en")
    """
    return LANGUAGE_MAPPING.get(language_name, language_name)


def get_language_name(language_code: str) -> str:
    """
    언어 코드를 영어 이름으로 변환
    
    Parameters
    ----------
    language_code : str
        언어 코드 (예: "ko", "en")
    
    Returns
    -------
    str
        영어 언어 이름 (예: "Korean", "English")
    """
    return LANGUAGE_NAMES.get(language_code, language_code)

