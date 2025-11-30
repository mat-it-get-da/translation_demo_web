<script lang="ts">
    import { onDestroy } from "svelte";

    // Props
    export let isRunning: boolean = false;
    export let isCompleted: boolean = false;
    export let elapsedTime: number = 0;  // 외부에서 접근 가능하도록 export

    // 상태
    let intervalId: number | null = null;
    let displayTime: string = "0.00";

    // isRunning이 변경될 때마다 실행
    $: {
        if (isRunning && !intervalId) {
            startTimer();
        } else if (!isRunning && intervalId) {
            stopTimer();
        }
    }

    // 타이머 시작
    function startTimer() {
        elapsedTime = 0;
        displayTime = "0.00";
        intervalId = window.setInterval(() => {
            elapsedTime += 0.1;
            displayTime = elapsedTime.toFixed(2);
        }, 100);
    }

    // 타이머 정지
    function stopTimer() {
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
        }
    }

    // 컴포넌트 파괴 시 타이머 정리
    onDestroy(() => {
        stopTimer();
    });
</script>

{#if isRunning || isCompleted}
    <div class="timer-container" class:running={isRunning} class:completed={isCompleted}>
        <span class="timer-icon">⏱️</span>
        <span class="timer-label">
            {#if isRunning}
                번역 중...
            {:else if isCompleted}
                완료!
            {/if}
        </span>
        <span class="timer-value">{displayTime}초</span>
    </div>
{/if}

<style>
    .timer-container {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.3s ease;
    }

    .timer-container.running {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        animation: pulse 2s ease-in-out infinite;
    }

    .timer-container.completed {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        color: white;
        animation: bounceIn 0.5s ease;
    }

    .timer-icon {
        font-size: 1.5rem;
        animation: rotate 2s linear infinite;
    }

    .timer-container.completed .timer-icon {
        animation: none;
    }

    .timer-label {
        font-weight: 600;
    }

    .timer-value {
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        font-weight: 700;
        min-width: 4rem;
        text-align: right;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
    }

    @keyframes bounceIn {
        0% {
            transform: scale(0.8);
            opacity: 0;
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }

    @keyframes rotate {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }

    @media (max-width: 768px) {
        .timer-container {
            font-size: 0.9rem;
            padding: 0.5rem 0.75rem;
        }

        .timer-icon {
            font-size: 1.2rem;
        }

        .timer-value {
            font-size: 1rem;
            min-width: 3.5rem;
        }
    }
</style>

