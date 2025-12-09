"""
모델 프로필 목록 응답 스키마 모델
"""

from pydantic import BaseModel

from .model_profile import ModelProfile


class ModelProfiles(BaseModel):
    """
    모델 프로필 목록 응답 모델

    사용 가능한 모든 번역 모델의 목록을 반환하는 응답을 정의합니다.

    Parameters
    ----------
    models : list[ModelProfile]
        사용 가능한 번역 모델들의 정보 리스트.
        각 항목은 ModelProfile 객체로, 모델의 ID, 이름, 설명을 포함합니다.

    Examples
    --------
    >>> response = ModelProfiles(
    ...     models=[
    ...         ModelProfile(
    ...             id="gpt-4o-mini",
    ...             name="GPT-4o Mini",
    ...             description="OpenAI의 빠르고 저렴한 최신 모델"
    ...         ),
    ...         ModelProfile(
    ...             id="google-translate",
    ...             name="Google Translate",
    ...             description="구글 번역 - 빠르고 정확한 무료 번역"
    ...         )
    ...     ]
    ... )
    """

    models: list[ModelProfile]
