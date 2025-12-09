<script lang="ts">
    // 부모에서 전달받는 자연어 리스트
    export let langList: string[] = [];
    // 선택된 언어 (양방향 바인딩)
    export let selectedLang: string = "";
    // 버튼에 표시할 기본 텍스트 (선택 안했을 때)
    export let placeholder: string = "언어 선택";

    // 모달 열림/닫힘 상태
    let isModalOpen: boolean = false;

    // 모달 토글
    const toggleModal = () => {
        isModalOpen = !isModalOpen;
    };

    // 모달 닫기
    const closeModal = () => {
        isModalOpen = false;
    };

    // 언어 선택
    const selectLang = (lang: string) => {
        selectedLang = lang;
        isModalOpen = false;
    };
</script>

<!-- 언어 선택 모달 컴포넌트 -->
<div class="lang-selector">
    <button type="button" class="trigger-btn" onclick={toggleModal}>
        {selectedLang || placeholder}
        <span class="arrow">▼</span>
    </button>

    {#if isModalOpen}
        <!-- 오버레이 배경 (화면 전체 덮음) -->
        <div
            class="modal-overlay"
            role="button"
            tabindex="0"
            onclick={closeModal}
            onkeydown={(e) => e.key === "Escape" && closeModal()}
        ></div>

        <!-- 모달 창 (화면 중앙에 고정) -->
        <div
            class="modal"
            role="dialog"
            tabindex="-1"
            aria-label="언어 선택"
            onclick={(e) => e.stopPropagation()}
            onkeydown={(e) => e.stopPropagation()}
        >
            <div class="modal-header">
                <h3>언어 선택</h3>
                <button type="button" class="close-btn" onclick={closeModal}
                    >✕</button
                >
            </div>
            <div class="modal-content">
                {#each langList as lang}
                    <div
                        class="lang-option"
                        class:selected={selectedLang === lang}
                        role="button"
                        tabindex="0"
                        onclick={() => selectLang(lang)}
                        onkeydown={(e) => e.key === "Enter" && selectLang(lang)}
                    >
                        {#if selectedLang === lang}
                            <span class="check">✓</span>
                        {/if}
                        {lang}
                    </div>
                {/each}
            </div>
        </div>
    {/if}
</div>

<style>
    .lang-selector {
        position: relative;
        display: inline-block;
    }

    .trigger-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 16px;
        border: 1px solid #ccc;
        border-radius: 6px;
        background: #fff;
        cursor: pointer;
        font-size: 14px;
        transition: border-color 0.2s;
    }

    .trigger-btn:hover {
        border-color: #888;
    }

    .arrow {
        font-size: 10px;
        color: #666;
    }

    /* 오버레이 - 화면 전체 덮음 (fixed) */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1000;
    }

    /* 모달 - 화면 중앙 고정 */
    .modal {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        z-index: 1001;
        min-width: 280px;
        max-width: 90vw;
        max-height: 70vh;
        overflow: hidden;
        animation: modalFadeIn 0.2s ease-out;
    }

    @keyframes modalFadeIn {
        from {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translate(-50%, -50%) scale(1);
        }
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px;
        border-bottom: 1px solid #eee;
    }

    .modal-header h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
    }

    .close-btn {
        background: none;
        border: none;
        font-size: 18px;
        cursor: pointer;
        color: #666;
        padding: 4px 8px;
        border-radius: 4px;
        transition: background 0.2s;
    }

    .close-btn:hover {
        background: #f0f0f0;
    }

    .modal-content {
        padding: 8px 0;
        max-height: 50vh;
        overflow-y: auto;
    }

    .lang-option {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 20px;
        cursor: pointer;
        transition: background 0.15s;
    }

    .lang-option:hover {
        background: #f5f5f5;
    }

    .lang-option.selected {
        background: #e8f4fd;
        color: #1976d2;
    }

    .check {
        color: #1976d2;
        font-weight: bold;
    }
</style>
