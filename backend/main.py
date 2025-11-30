#!/usr/bin/env python
"""
Lemonade Server 기반 번역기

이 스크립트는 Lemonade Server를 사용하여 다국어 간 번역을 수행합니다.
Hydra를 통해 설정을 관리하며, 명령줄에서 모델을 변경할 수 있습니다.

실행 방법:
-----------
기본 설정으로 실행 (Qwen3 모델):
    rye run python -m backend.main

다른 모델로 실행:
    rye run python -m backend.main model=gemma3
    rye run python -m backend.main model=gpt-oss

주의사항:
---------
- Lemonade Server가 http://localhost:8000에서 실행 중이어야 합니다
- 사용할 모델을 미리 다운로드해야 합니다:
  lemonade-server pull Qwen3-4B-Instruct-2507-GGUF
  lemonade-server pull Gemma-3-4b-it-GGUF
  lemonade-server pull gpt-oss-20b-mxfp4-GGUF
"""

import os
import sys
from pathlib import Path
from typing import List, Dict

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import hydra  # noqa: E402
from omegaconf import DictConfig  # noqa: E402
from openai import OpenAI  # noqa: E402


def translate_text(
    client: OpenAI,
    text: str,
    source_lang: str,
    target_lang: str,
    model_name: str,
    temperature: float,
    max_tokens: int,
) -> str:
    """
    Lemonade Server를 사용하여 텍스트를 번역합니다.

    Parameters
    ----------
    client : OpenAI
        OpenAI 호환 클라이언트 (Lemonade Server)
    text : str
        번역할 텍스트
    source_lang : str
        원본 언어 (예: "en", "ko")
    target_lang : str
        목표 언어 (예: "en", "ko")
    model_name : str
        사용할 모델 이름
    temperature : float
        생성 온도
    max_tokens : int
        최대 토큰 수

    Returns
    -------
    str
        번역된 텍스트
    """
    # 언어 코드를 전체 이름으로 변환
    lang_names = {
        "en": "English",
        "ko": "Korean",
        "ja": "Japanese",
        "zh": "Chinese",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
    }

    source_name = lang_names.get(source_lang, source_lang)
    target_name = lang_names.get(target_lang, target_lang)

    # 시스템 프롬프트
    system_prompt = f"""You are a professional translator. Translate the given text from {source_name} to {target_name}.
Provide ONLY the translated text without any explanations or additional comments."""

    # 사용자 메시지
    user_message = f"Translate this text to {target_name}:\n\n{text}"

    # API 호출
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,  # 스트리밍 비활성화로 속도 개선
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ 번역 중 오류 발생: {e}")
        raise


@hydra.main(version_base=None, config_path="../configs", config_name="config")
def main(cfg: DictConfig):
    """
    메인 함수.

    Hydra를 통해 설정을 로드하고 Lemonade Server로 번역 예제를 실행합니다.

    Parameters
    ----------
    cfg : DictConfig
        Hydra 설정 객체
    """
    print("=" * 80)
    print("Lemonade Server 번역기")
    print("=" * 80)
    print()

    # 설정 출력
    print("📋 현재 설정:")
    print("-" * 80)
    print(f"모델: {cfg.model.name}")
    print(f"프로바이더: {cfg.model.provider}")
    print(f"온도: {cfg.model.temperature}")
    print(f"최대 토큰: {cfg.model.max_tokens}")
    print(f"Top-P: {cfg.model.top_p}")
    print(f"Lemonade Server: {cfg.api.base_url}")
    print("-" * 80)
    print()

    # Lemonade Server 클라이언트 초기화
    try:
        client = OpenAI(
            base_url=cfg.api.base_url,
            api_key="lemonade",  # required but unused
        )
        print("✅ Lemonade Server 클라이언트 초기화 완료")
        print(f"   연결: {cfg.api.base_url}")
        print()
    except Exception as e:
        print(f"❌ 클라이언트 초기화 실패: {e}")
        print()
        print("해결 방법:")
        print("1. Lemonade Server가 실행 중인지 확인하세요")
        print("2. 서버 주소가 올바른지 확인하세요: http://localhost:8000")
        return

    # 번역 예제 실행
    test_cases: List[Dict[str, str]] = [
        {
            "text": "Hello, world! This is a simple translation test using Lemonade Server.",
            "source": "en",
            "target": "ko",
            "description": "영어 → 한국어",
        },
        {
            "text": "안녕하세요! Lemonade Server를 사용한 간단한 번역 테스트입니다.",
            "source": "ko",
            "target": "en",
            "description": "한국어 → 영어",
        },
        {
            "text": "Machine learning is revolutionizing the way we approach complex problems in various fields.",
            "source": "en",
            "target": "ko",
            "description": "영어 → 한국어 (긴 문장)",
        },
    ]

    print("🔄 번역 예제 실행")
    print("=" * 80)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[테스트 {i}] {test_case['description']}")
        print("-" * 80)
        print(f"원문: {test_case['text']}")
        print()

        try:
            result = translate_text(
                client=client,
                text=test_case["text"],
                source_lang=test_case["source"],
                target_lang=test_case["target"],
                model_name=cfg.model.name,
                temperature=cfg.model.temperature,
                max_tokens=cfg.model.max_tokens,
            )

            print(f"번역: {result}")
            print()
            print("✅ 성공")

        except Exception as e:
            print(f"❌ 실패: {e}")
            import traceback

            traceback.print_exc()

    print()
    print("=" * 80)
    print("🎉 번역 예제 완료!")
    print()


if __name__ == "__main__":
    main()
