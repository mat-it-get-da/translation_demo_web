import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: 'index.html',
			precompress: false,
			strict: true
		}),
		paths: {
			// 모든 환경에서 base를 빈 문자열로 설정 (루트 경로 `/`로 서빙)
			// 환경 변수 SVELTE_BASE_PATH가 명시적으로 설정되어 있으면 사용, 없으면 빈 문자열
			base: process.env.SVELTE_BASE_PATH !== undefined 
				? process.env.SVELTE_BASE_PATH 
				: '/'
		}
	}
};

export default config;
