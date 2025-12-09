"""
번역 응답 스키마 모델
"""

from pydantic import BaseModel, Field


class TranslationResponse(BaseModel):
    """
    번역 응답 모델

    번역 API가 클라이언트에게 반환하는 번역 결과를 정의합니다.

    Parameters
    ----------
    translated_text : str
        번역된 텍스트. 원본 텍스트가 목표 언어로 번역된 결과입니다.
    model : str
        번역에 사용된 모델 ID. 요청 시 지정한 모델과 동일합니다.
    source_lang : str
        원본 언어 코드. 요청 시 지정한 언어 코드로 정규화된 값입니다.
    target_lang : str
        목표 언어 코드. 요청 시 지정한 언어 코드로 정규화된 값입니다.

    Examples
    --------
    >>> response = TranslationResponse(
    ...     translated_text="안녕하세요, 세상!",
    ...     model="gpt-4o-mini",
    ...     source_lang="en",
    ...     target_lang="ko"
    ... )
    """

    translated_text: str = Field(..., description="번역된 텍스트")
    model: str = Field(..., description="사용된 모델 ID")
    source_lang: str = Field(..., description="원본 언어")
    target_lang: str = Field(..., description="목표 언어")
