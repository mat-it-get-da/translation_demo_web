"""
Post-Editor 번역기: DeepL NMT + GPT-4o 후수정

DeepL NMT로 초기 번역을 수행한 후, GPT-4o로 번역을 세밀하게 후수정하여
최고 품질의 번역을 제공합니다.
"""

from fastapi import HTTPException
from .deepl_translator import translate_with_deepl
from .openai_translator import openai_client


async def translate_with_post_editor(
    text: str,
    source_lang: str,
    target_lang: str,
    source_name: str,
    target_name: str,
) -> str:
    """
    DeepL NMT로 초기 번역 후 GPT-4o로 후수정합니다.

    Parameters
    ----------
    text : str
        번역할 텍스트
    source_lang : str
        원본 언어 코드 (예: "en")
    target_lang : str
        목표 언어 코드 (예: "ko")
    source_name : str
        원본 언어 이름 (예: "English")
    target_name : str
        목표 언어 이름 (예: "Korean")

    Returns
    -------
    str
        후수정된 번역 텍스트

    Raises
    ------
    HTTPException
        번역 또는 후수정 실패 시

    Notes
    -----
    이 번역기는 2단계 프로세스를 사용합니다:
    1. DeepL NMT로 자연스러운 초기 번역 생성
    2. GPT-4o로 번역을 검토하고 세밀하게 개선
    """
    # Step 1: DeepL NMT로 초기 번역
    try:
        initial_translation = translate_with_deepl(text, source_lang, target_lang)
        print(f"[Post-Editor] Step 1/2: DeepL 초기 번역 완료")
        print(f"[Post-Editor] DeepL 결과: {initial_translation[:80]}...")
    except HTTPException as e:
        # translate_with_deepl 내부에서 이미 적절한 에러를 발생시킴
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DeepL 초기 번역 실패: {str(e)}")

    # Step 2: GPT-4o로 후수정
    if not openai_client:
        raise HTTPException(
            status_code=500,
            detail="OpenAI 클라이언트가 초기화되지 않았습니다.",
        )

    try:
        # Post-editing 프롬프트
        system_prompt = """You are an expert post-editor specializing in refining machine translations.

<Goals>
1) Review and improve machine-translated text while preserving the original meaning
2) Ensure natural flow, cultural appropriateness, and linguistic accuracy
3) Maintain consistency with the source text
4) Produce polished, publication-ready translations
</Goals>

<Output Format>
Provide only the improved translation text without any explanations, notes, or additional commentary.
- Output must be in the target language only
- Do not include source text or comparison comments
- Focus on delivering the final, polished version
</Output Format>

<Format Explanations>
Natural Flow: Ensure the translation reads smoothly and naturally in the target language
Cultural Appropriateness: Adapt expressions, idioms, and references to be culturally relevant
Linguistic Accuracy: Maintain grammatical correctness and proper terminology usage
Consistency: Preserve the tone and style of the original text
</Format Explanations>"""

        user_prompt = f"""Review and improve this machine translation.

Source Language: {source_name}
Target Language: {target_name}

Original Text:
{text}

Machine Translation (DeepL NMT):
{initial_translation}

Task: Carefully review the machine translation and improve it to make it more natural, accurate, and culturally appropriate. Fix any awkward phrasing, grammatical errors, or unnatural expressions. Output only the improved translation in {target_name}."""

        print(f"[Post-Editor] Step 2/2: GPT-4o 후수정 시작...")

        response = openai_client.chat.completions.create(
            model="gpt-4o",  # GPT-4o 사용
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=1024,
        )

        post_edited_text = response.choices[0].message.content.strip()
        print(f"[Post-Editor] GPT-4o 후수정 완료!")
        print(f"[Post-Editor] 최종 결과: {post_edited_text[:80]}...")

        return post_edited_text

    except Exception as e:
        # 후수정 실패 시 DeepL 번역이라도 반환
        print(f"[Post-Editor] WARNING: GPT-4o 후수정 실패, DeepL 번역 반환")
        print(f"[Post-Editor] 에러: {str(e)}")
        return initial_translation
