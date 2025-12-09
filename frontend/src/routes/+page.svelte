<script lang="ts">
    import { onMount } from "svelte";
    import Models from "../components/models.svelte";
    import LangModal from "../components/LangModal.svelte";
    import TranslationTimer from "../components/TranslationTimer.svelte";
    import TranslationHistory from "../components/TranslationHistory.svelte";

    // API 기본 URL
    const API_BASE_URL =
        import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

    // 모델 정보 타입
    interface ModelInfo {
        id: string;
        name: string;
        description: string;
    }

    // 번역 기록 타입
    interface TranslationHistory {
        id: number;
        inputText: string;
        outputText: string;
        elapsedTime: number;
        model: string;
        sourceLang: string;
        targetLang: string;
        timestamp: Date;
    }

    // AI 모델 리스트
    let aiModels: string[] = [];
    let modelMap: Map<string, string> = new Map(); // 표시명 -> ID 매핑
    let selectedAIModel: string = "";

    // 자연어 리스트
    let languages: string[] = [
        "한국어",
        "English",
        "日本語",
        "中文",
        "Español",
        "Français",
        "Deutsch",
    ];

    // 언어 코드 매핑
    const languageCodeMap: { [key: string]: string } = {
        한국어: "ko",
        English: "en",
        日本語: "ja",
        中文: "zh",
        Español: "es",
        Français: "fr",
        Deutsch: "de",
    };

    // 선택된 입력 언어
    let selectedInputLanguage: string = "";
    // 선택된 출력 언어
    let selectedOutputLanguage: string = "";

    // 입력/출력 텍스트
    let userInput: string = "";
    let aiOutput: string = "";

    // 상태 관리
    let isLoading: boolean = false;
    let error: string = "";
    let isTranslating: boolean = false;

    // 타이머 상태
    let timerRunning: boolean = false;
    let timerCompleted: boolean = false;
    let timerElapsedTime: number = 0;
    let translationStartTime: number = 0;

    // 번역 기록
    let translationHistory: TranslationHistory[] = [];
    let historyIdCounter: number = 1;

    // 컴포넌트 마운트 시 모델 목록 가져오기
    onMount(async () => {
        await fetchModels();
    });

    // 모델 목록 가져오기
    async function fetchModels() {
        isLoading = true;
        error = "";

        try {
            const response = await fetch(`${API_BASE_URL}/api/models`);

            if (!response.ok) {
                throw new Error(
                    `모델 목록을 가져오는데 실패했습니다: ${response.status}`,
                );
            }

            const data: { models: ModelInfo[] } = await response.json();

            // 모델 표시명 배열 생성
            aiModels = data.models.map((model) => model.name);

            // 표시명 -> ID 매핑 생성
            data.models.forEach((model) => {
                modelMap.set(model.name, model.id);
            });

            // 첫 번째 모델을 기본값으로 선택
            if (aiModels.length > 0) {
                selectedAIModel = aiModels[0];
            }
        } catch (err) {
            error =
                err instanceof Error
                    ? err.message
                    : "모델 목록을 가져오는데 실패했습니다.";
            console.error("Error fetching models:", err);

            // 폴백: 기본 모델 사용 (백엔드 연결 실패 시)
            aiModels = [
                "GPT-3.5 Turbo",
                "GPT-4o Mini",
                "GPT-4o",
                "Google Translate",
                "DeepL NMT",
            ];
            modelMap.set("GPT-3.5 Turbo", "gpt-3.5-turbo");
            modelMap.set("GPT-4o Mini", "gpt-4o-mini");
            modelMap.set("GPT-4o", "gpt-4o");
            modelMap.set("Google Translate", "google-translate");
            modelMap.set("DeepL NMT", "deepl-nmt");
        } finally {
            isLoading = false;
        }
    }

    // 번역 함수
    async function handleTranslate() {
        // 입력 검증
        if (!userInput.trim()) {
            error = "번역할 텍스트를 입력하세요.";
            return;
        }

        if (!selectedAIModel) {
            error = "AI 모델을 선택하세요.";
            return;
        }

        if (!selectedInputLanguage) {
            error = "입력 언어를 선택하세요.";
            return;
        }

        if (!selectedOutputLanguage) {
            error = "출력 언어를 선택하세요.";
            return;
        }

        // 같은 언어로 번역 시도 방지
        if (selectedInputLanguage === selectedOutputLanguage) {
            error = "입력 언어와 출력 언어가 같습니다.";
            return;
        }

        // 상태 초기화
        isTranslating = true;
        error = "";
        aiOutput = "";
        timerRunning = true;
        timerCompleted = false;
        translationStartTime = Date.now();

        try {
            // 모델 ID 가져오기
            const modelId = modelMap.get(selectedAIModel);
            if (!modelId) {
                throw new Error("유효하지 않은 모델입니다.");
            }

            // 언어 코드 변환
            const sourceLang = languageCodeMap[selectedInputLanguage];
            const targetLang = languageCodeMap[selectedOutputLanguage];

            // API 요청
            const response = await fetch(`${API_BASE_URL}/api/translate`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    text: userInput,
                    source_lang: sourceLang,
                    target_lang: targetLang,
                    model: modelId,
                }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(
                    errorData.detail || `번역 실패: ${response.status}`,
                );
            }

            const data = await response.json();
            aiOutput = data.translated_text;

            // 번역 성공 시 기록 저장
            const elapsedSeconds = (Date.now() - translationStartTime) / 1000;
            timerElapsedTime = elapsedSeconds;

            const newHistory: TranslationHistory = {
                id: historyIdCounter++,
                inputText: userInput,
                outputText: aiOutput,
                elapsedTime: elapsedSeconds,
                model: selectedAIModel,
                sourceLang: selectedInputLanguage,
                targetLang: selectedOutputLanguage,
                timestamp: new Date(),
            };

            // 최신 기록이 맨 위로 오도록 배열 앞에 추가
            translationHistory = [newHistory, ...translationHistory];
        } catch (err) {
            error =
                err instanceof Error
                    ? err.message
                    : "번역 중 오류가 발생했습니다.";
            console.error("Translation error:", err);
        } finally {
            isTranslating = false;
            timerRunning = false;
            if (!error && aiOutput) {
                timerCompleted = true;
                // 3초 후 완료 상태 초기화
                setTimeout(() => {
                    timerCompleted = false;
                }, 3000);
            }
        }
    }

    // 번역 버튼 활성화 여부
    $: canTranslate =
        userInput.trim() &&
        selectedAIModel &&
        selectedInputLanguage &&
        selectedOutputLanguage &&
        !isTranslating;

    // 개별 기록 삭제
    function deleteHistory(id: number) {
        translationHistory = translationHistory.filter((h) => h.id !== id);
    }

    // 전체 기록 삭제
    function clearAllHistory() {
        translationHistory = [];
    }
</script>

<div class="container">
    <h1>🌐 AI 번역기</h1>

    {#if error}
        <div class="error-banner">
            ⚠️ {error}
            <button on:click={() => (error = "")} class="close-btn">✕</button>
        </div>
    {/if}

    <!-- AI 모델 선택 -->
    {#if isLoading}
        <p>모델 목록을 불러오는 중...</p>
    {:else}
        <Models modelList={aiModels} bind:selectedModel={selectedAIModel} />
        {#if selectedAIModel}
            <p class="selected-info">
                선택된 모델: <strong>{selectedAIModel}</strong>
            </p>
        {/if}
    {/if}

    <hr />

    <!-- 언어 선택 -->
    <div class="language-selection">
        <div class="lang-item">
            <p>입력 언어:</p>
            <LangModal
                langList={languages}
                bind:selectedLang={selectedInputLanguage}
                placeholder="입력 언어 선택"
            />
        </div>

        <div class="lang-item">
            <p>출력 언어:</p>
            <LangModal
                langList={languages}
                bind:selectedLang={selectedOutputLanguage}
                placeholder="출력 언어 선택"
            />
        </div>
    </div>

    <!-- 텍스트 입력/출력 영역 -->
    <div class="text-areas">
        <div class="text-area-container">
            <label for="input-text">입력 텍스트:</label>
            <textarea
                id="input-text"
                bind:value={userInput}
                placeholder="여기에 번역할 텍스트를 입력하세요..."
                rows="8"
                disabled={isTranslating}
            ></textarea>
            <p class="char-count">{userInput.length}자</p>
        </div>

        <div class="text-area-container">
            <label for="output-text">번역 결과:</label>
            <textarea
                id="output-text"
                bind:value={aiOutput}
                placeholder="번역 결과가 여기에 표시됩니다..."
                rows="8"
                readonly
            ></textarea>
            {#if aiOutput}
                <p class="char-count">{aiOutput.length}자</p>
            {/if}
        </div>
    </div>

    <!-- 번역 버튼 -->
    <div class="button-container">
        <button
            on:click={handleTranslate}
            disabled={!canTranslate}
            class="translate-btn"
        >
            {#if isTranslating}
                <span class="spinner"></span>
                번역 중...
            {:else}
                🚀 번역하기
            {/if}
        </button>
    </div>

    <!-- 번역 타이머 -->
    <div class="timer-wrapper">
        <TranslationTimer
            isRunning={timerRunning}
            isCompleted={timerCompleted}
            bind:elapsedTime={timerElapsedTime}
        />
    </div>

    <!-- 번역 기록 표시 -->
    {#if aiOutput}
        <TranslationHistory
            history={translationHistory}
            on:deleteHistory={(e) => deleteHistory(e.detail.id)}
            on:clearAll={clearAllHistory}
        />
    {/if}
</div>

<style>
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }

    h1 {
        text-align: center;
        color: #333;
        margin-bottom: 1.5rem;
    }

    .error-banner {
        background: #fee;
        border: 1px solid #fcc;
        color: #c00;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .close-btn {
        background: none;
        border: none;
        color: #c00;
        font-size: 1.2rem;
        cursor: pointer;
        padding: 0 0.5rem;
    }

    .selected-info {
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #ddd;
    }

    .language-selection {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .lang-item p {
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    .text-areas {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .text-area-container {
        display: flex;
        flex-direction: column;
    }

    .text-area-container label {
        margin-bottom: 0.5rem;
        font-weight: 500;
    }

    textarea {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-family: inherit;
        font-size: 0.95rem;
        resize: vertical;
    }

    textarea:focus {
        outline: none;
        border-color: #4caf50;
    }

    textarea:disabled {
        background: #f5f5f5;
        cursor: not-allowed;
    }

    textarea[readonly] {
        background: #f9f9f9;
    }

    .char-count {
        font-size: 0.85rem;
        color: #666;
        text-align: right;
        margin-top: 0.25rem;
    }

    .button-container {
        text-align: center;
        margin: 1.5rem 0;
    }

    .timer-wrapper {
        text-align: center;
        margin: 1rem 0;
        min-height: 3rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .translate-btn {
        background: #4caf50;
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        border-radius: 4px;
        cursor: pointer;
        transition: background 0.3s;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }

    .translate-btn:hover:not(:disabled) {
        background: #45a049;
    }

    .translate-btn:disabled {
        background: #ccc;
        cursor: not-allowed;
    }

    .spinner {
        width: 16px;
        height: 16px;
        border: 2px solid #fff;
        border-top-color: transparent;
        border-radius: 50%;
        animation: spin 0.6s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    @media (max-width: 768px) {
        .language-selection,
        .text-areas {
            grid-template-columns: 1fr;
        }
    }
</style>
