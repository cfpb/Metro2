/// <reference types="vitest" />
import eslintPlugin from '@nabla/vite-plugin-eslint'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig(({ mode }) => ({
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
    },
    onConsoleLog(log: string, type: 'stderr' | 'stdout'): false | void {
      console.log('log in test:', log)
      if (log === 'message from third party library' && type === 'stdout') {
        return false
      }
    }
  },
  plugins: [tsconfigPaths(), react(), ...(mode === 'test' ? [] : [eslintPlugin()])],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://django:8000',
        changeOrigin: true,
        secure: false,
        ws: true
      }
    }
  }
}))
