<script lang="ts">
    import { createEventDispatcher } from "svelte";

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

    // Props
    export let history: TranslationHistory[] = [];

    // 이벤트 디스패처
    const dispatch = createEventDispatcher();

    // 개별 기록 삭제
    function handleDeleteHistory(id: number) {
        dispatch("deleteHistory", { id });
    }

    // 전체 기록 삭제
    function handleClearAll() {
        if (confirm("모든 번역 기록을 삭제하시겠습니까?")) {
            dispatch("clearAll");
        }
    }

    // 텍스트 축약 함수
    function truncateText(text: string, maxLength: number = 150): string {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + "...";
    }

    // 시간 포맷팅 함수
    function formatTime(seconds: number): string {
        return seconds.toFixed(2) + "초";
    }
</script>

{#if history.length > 0}
    <div class="history-section">
        <div class="history-header">
            <h3>📚 기록</h3>
            <button on:click={handleClearAll} class="clear-all-btn">
                🗑️ 전체 삭제
            </button>
        </div>

        <div class="history-list">
            {#each history as item (item.id)}
                <div class="history-card">
                    <div class="history-card-header">
                        <div class="history-info">
                            <span class="history-model">🤖 {item.model}</span>
                            <span class="history-lang">
                                {item.sourceLang} → {item.targetLang}
                            </span>
                            <span class="history-time-badge">
                                ⏱️ {formatTime(item.elapsedTime)}
                            </span>
                        </div>
                        <button
                            on:click={() => handleDeleteHistory(item.id)}
                            class="delete-btn"
                            title="이 기록 삭제"
                        >
                            ✕
                        </button>
                    </div>

                    <div class="history-content">
                        <div class="history-text">
                            <strong>입력:</strong>
                            <p>{truncateText(item.inputText, 150)}</p>
                        </div>
                        <div class="history-text">
                            <strong>결과:</strong>
                            <p>{truncateText(item.outputText, 150)}</p>
                        </div>
                    </div>

                    <div class="history-footer">
                        <span class="history-timestamp">
                            {item.timestamp.toLocaleString("ko-KR")}
                        </span>
                    </div>
                </div>
            {/each}
        </div>
    </div>
{:else}
    <div class="no-history">
        <p>아직 번역 기록이 없습니다.</p>
        <p class="hint">번역을 완료하면 여기에 기록이 표시됩니다.</p>
    </div>
{/if}

<style>
    /* 기록 섹션 스타일 */
    .history-section {
        margin-top: 2rem;
        padding: 1.5rem;
        background: #f9f9f9;
        border-radius: 8px;
    }

    .history-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    .history-header h3 {
        margin: 0;
        color: #333;
        font-size: 1.5rem;
    }

    .clear-all-btn {
        background: #f44336;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: background 0.3s;
    }

    .clear-all-btn:hover {
        background: #d32f2f;
    }

    .history-list {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }

    .history-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        transition: box-shadow 0.3s;
    }

    .history-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .history-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }

    .history-info {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        align-items: center;
    }

    .history-model {
        font-weight: 600;
        color: #1976d2;
    }

    .history-lang {
        color: #666;
        font-size: 0.9rem;
    }

    .history-time-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .delete-btn {
        background: #ff5252;
        color: white;
        border: none;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.3s;
    }

    .delete-btn:hover {
        background: #f44336;
    }

    .history-content {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }

    .history-text {
        padding: 0.5rem;
        background: #f5f5f5;
        border-radius: 4px;
    }

    .history-text strong {
        display: block;
        margin-bottom: 0.25rem;
        color: #555;
        font-size: 0.9rem;
    }

    .history-text p {
        margin: 0;
        color: #333;
        line-height: 1.5;
    }

    .history-footer {
        margin-top: 0.75rem;
        padding-top: 0.75rem;
        border-top: 1px solid #e0e0e0;
    }

    .history-timestamp {
        font-size: 0.8rem;
        color: #999;
    }

    .no-history {
        text-align: center;
        padding: 3rem 1rem;
        color: #999;
        margin-top: 2rem;
        background: #f9f9f9;
        border-radius: 8px;
    }

    .no-history .hint {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    @media (max-width: 768px) {
        .history-section {
            padding: 1rem;
        }

        .history-header {
            flex-direction: column;
            gap: 1rem;
            align-items: stretch;
        }

        .history-info {
            flex-direction: column;
            align-items: flex-start;
        }

        .history-card {
            padding: 0.75rem;
        }
    }
</style>

