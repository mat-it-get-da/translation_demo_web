<script lang="ts">
    // 부모에서 전달받는 AI 모델 리스트
    export let modelList: string[] = [];
    // 현재 선택된 모델 (양방향 바인딩)
    export let selectedModel: string = "";
</script>

<!-- AI 모델 선택 드롭다운 -->
<div>
    <label for="model-select">AI 모델 선택:</label>
    <select id="model-select" bind:value={selectedModel}>
        <option value="" disabled>모델을 선택하세요</option>
        {#each modelList as model}
            <option value={model}>{model}</option>
        {/each}
    </select>
</div>
