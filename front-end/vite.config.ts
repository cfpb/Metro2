/// <reference types="vitest" />
import eslintPlugin from '@nabla/vite-plugin-eslint'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig(({ mode }) => ({
	base: 'static/',
  build: {
    // generate manifest.json in outDir
    manifest: true,
    rollupOptions: {
      input: {
        main: './src/main.tsx',
      },
      output: {
        chunkFileNames: undefined,
      },

    },
    // outDir: 'dist',
    commonjsOptions: {
      include: /node_modules/,
    },
  },
	test: {
		css: false,
		include: ['src/**/__tests__/*'],
		globals: true,
		environment: 'jsdom',
		setupFiles: 'src/setupTests.ts',
		clearMocks: true,
		coverage: {
			provider: 'istanbul',
			enabled: true,
			'100': true,
			reporter: ['text', 'lcov'],
			reportsDirectory: 'coverage'
		}
	},
	plugins: [
		tsconfigPaths(),
		react(),
		...(mode === 'test' ? [] : [eslintPlugin()])
	],
	server: {
		port: 3000,
		host: true
	}
}))
