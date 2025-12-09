"""
API 스키마 모델 패키지

번역 API의 Request/Response 모델을 정의합니다.

이 패키지는 다음과 같은 스키마 모델들을 제공합니다:

- TranslationRequest: 번역 요청 모델
- TranslationResponse: 번역 응답 모델
- ModelProfile: 모델 프로필 모델
- ModelProfiles: 모델 프로필 목록 응답 모델

Examples
--------
>>> from backend.schemas import TranslationRequest, TranslationResponse
>>>
>>> request = TranslationRequest(
...     text="Hello",
...     source_lang="en",
...     target_lang="ko",
...     model="gpt-4o-mini"
... )
"""

from .model_profile import ModelProfile
from .model_profiles import ModelProfiles
from .translation_request import TranslationRequest
from .translation_response import TranslationResponse

__all__ = [
    "TranslationRequest",
    "TranslationResponse",
    "ModelProfile",
    "ModelProfiles",
]
