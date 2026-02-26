/// <reference types="vitest" />
import react from '@vitejs/plugin-react'
import { resolve } from 'node:path'
import { defineConfig } from 'vite'
import eslint from 'vite-plugin-eslint'
import tsconfigPaths from 'vite-tsconfig-paths'
import pluginProcessIcons from './postcss/processIcons'

export default defineConfig(({ mode }) => ({
  css: {
    postcss: {
      plugins: [pluginProcessIcons()]
    }
  },
  resolve: {
    alias: {
      // Catch-all for internal library paths to bypass restrictive "exports" in package.json
      '@cfpb/cfpb-design-system/src': resolve(
        __dirname,
        'node_modules/@cfpb/cfpb-design-system/src'
      ),
      // Helper for specifically accessing the new abstracts location
      '@cfpb/cfpb-design-system/src/elements/abstracts': resolve(
        __dirname,
        'node_modules/@cfpb/cfpb-design-system/src/elements/abstracts/index.scss'
      )
    }
  },
  test: {
    css: false,
    // include: ['src/**/__tests__/*'],
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
  plugins: [tsconfigPaths(), react(), ...(mode === 'test' ? [] : [eslint()])],
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
