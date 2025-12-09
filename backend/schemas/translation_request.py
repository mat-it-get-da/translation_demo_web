"""
번역 요청 스키마 모델
"""

from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    """
    번역 요청 모델

    클라이언트로부터 받는 번역 요청 데이터를 정의합니다.

    Parameters
    ----------
    text : str
        번역할 텍스트. 최소 1자 이상이어야 합니다.
    source_lang : str
        원본 언어 코드. 예: "en", "ko", "ja" 등.
        언어 이름(예: "English", "한국어")도 지원합니다.
    target_lang : str
        목표 언어 코드. 예: "en", "ko", "ja" 등.
        언어 이름(예: "English", "한국어")도 지원합니다.
    model : str
        사용할 번역 모델 ID. 예: "gpt-4o-mini", "google-translate", "deepl-nmt" 등.

    Examples
    --------
    >>> request = TranslationRequest(
    ...     text="Hello, world!",
    ...     source_lang="en",
    ...     target_lang="ko",
    ...     model="gpt-4o-mini"
    ... )
    """

    text: str = Field(..., description="번역할 텍스트", min_length=1)
    source_lang: str = Field(..., description="원본 언어 (예: 'en', 'ko')")
    target_lang: str = Field(..., description="목표 언어 (예: 'en', 'ko')")
    model: str = Field(..., description="사용할 모델 ID")
