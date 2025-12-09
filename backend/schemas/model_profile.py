"""
모델 프로필 스키마 모델
"""

from pydantic import BaseModel


class ModelProfile(BaseModel):
    """
    모델 프로필 모델

    사용 가능한 번역 모델의 메타데이터를 정의합니다.

    Parameters
    ----------
    id : str
        모델의 고유 식별자. API 요청 시 사용되는 모델 ID입니다.
        예: "gpt-4o-mini", "google-translate", "deepl-nmt" 등.
    name : str
        모델의 표시 이름. 사용자에게 보여지는 이름입니다.
        예: "GPT-4o Mini", "Google Translate", "DeepL NMT" 등.
    description : str
        모델에 대한 설명. 모델의 특징, 장점, 사용 사례 등을 설명합니다.

    Examples
    --------
    >>> profile = ModelProfile(
    ...     id="gpt-4o-mini",
    ...     name="GPT-4o Mini",
    ...     description="OpenAI의 빠르고 저렴한 최신 모델 - 번역에 최적화"
    ... )
    """

    id: str
    name: str
    description: str
