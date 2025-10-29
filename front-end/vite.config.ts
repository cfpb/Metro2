/// <reference types="vitest" />
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import eslint from 'vite-plugin-eslint'
import tsconfigPaths from 'vite-tsconfig-paths'
import { resolve } from 'node:path'

export default defineConfig(({ mode }) => ({
  resolve: {
    alias: {
      '~': resolve(__dirname),
      '@cfpb/cfpb-design-system/src/index': resolve(
        __dirname,
        'node_modules/@cfpb/cfpb-design-system/src/index.scss'
      ),
      '@cfpb/cfpb-design-system/src/abstracts': resolve(
        __dirname,
        'node_modules/@cfpb/cfpb-design-system/src/abstracts/index.scss'
      ),
      '@cfpb/cfpb-design-system/src/utilities': resolve(
        __dirname,
        'node_modules/@cfpb/cfpb-design-system/src/utilities/index.scss'
      ),
      '@cfpb/cfpb-design-system/src/components/cfpb-typography/mixins': resolve(
        __dirname,
        'node_modules/@cfpb/cfpb-design-system/src/components/cfpb-typography/mixins.scss'
      ),
      '@cfpb/cfpb-design-system/src/components/cfpb-notifications/vars': resolve(
        __dirname,
        'node_modules/@cfpb/cfpb-design-system/src/components/cfpb-notifications/vars.scss'
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
