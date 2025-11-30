<script lang="ts">
    // 부모에서 전달받는 자연어 리스트
    export let langList: string[] = [];
    // 선택된 언어 (양방향 바인딩)
    export let selectedLang: string = "";
    // 버튼에 표시할 기본 텍스트 (선택 안했을 때)
    export let placeholder: string = "언어 선택";

    // 팝오버 열림/닫힘 상태
    let isPopoverOpen: boolean = false;

    // 팝오버 토글
    const togglePopover = () => {
        isPopoverOpen = !isPopoverOpen;
    };

    // 팝오버 닫기 (오버레이 클릭 시)
    const closePopover = () => {
        isPopoverOpen = false;
    };

    // 언어 선택
    const selectLang = (lang: string) => {
        selectedLang = lang;
        isPopoverOpen = false;
    };
</script>

<!-- 언어 선택 팝오버 컴포넌트 -->
<div>
    <button type="button" onclick={togglePopover}>
        {selectedLang || placeholder}
    </button>
    {#if isPopoverOpen}
        <!-- 오버레이 배경 -->
        <div
            class="overlay"
            role="button"
            tabindex="0"
            onclick={closePopover}
            onkeydown={(e) => e.key === "Escape" && closePopover()}
        ></div>

        <!-- 팝오버 창 -->
        <div
            class="popover"
            role="dialog"
            tabindex="-1"
            aria-label="언어 선택"
            onclick={(e) => e.stopPropagation()}
            onkeydown={(e) => e.stopPropagation()}
        >
            <div class="popover-content">
                {#each langList as lang}
                    <div
                        role="button"
                        tabindex="0"
                        onclick={() => selectLang(lang)}
                        onkeydown={(e) => e.key === "Enter" && selectLang(lang)}
                    >
                        {#if selectedLang === lang}
                            <span>✓</span>
                        {/if}
                        {lang}
                    </div>
                {/each}
            </div>
        </div>
    {/if}
</div>
