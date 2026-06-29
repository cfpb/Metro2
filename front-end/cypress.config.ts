import { defineConfig } from 'cypress'
import dotenv from 'dotenv'
import path from 'path'
import { fileURLToPath } from 'url'
import { loadEnv } from 'vite'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

// Get any env variable overrides from parent of parent directory
dotenv.config({ path: path.resolve(__dirname, '../../.env') })

export default defineConfig({
  // Set to false to disable deprecated Cypress.env()
  allowCypressEnv: false,
  fileServerFolder: 'dist',
  projectId: 'etow1b',

  e2e: {
    baseUrl: 'http://localhost:3000/',
    specPattern: 'cypress/e2e/**/*.ts',
    setupNodeEvents(on, config) {
      // Capture the current mode (defaults to 'development' if not set)
      const mode = (config.env.mode as string) || 'development'

      // Load env variables from the project root based on the mode
      const viteEnv = loadEnv(mode, process.cwd())

      // Assign the variables to config.env so Cypress can access them
      // Check for override values first
      config.env.VITE_ADMIN_EMAIL =
        process.env.VITE_ADMIN_EMAIL ?? viteEnv.VITE_ADMIN_EMAIL
      config.env.VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT =
        process.env.VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT ??
        viteEnv.VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT
      config.env.VITE_PII_WARNING_TEXT =
        process.env.VITE_PII_WARNING_TEXT ?? viteEnv.VITE_PII_WARNING_TEXT
      config.env.VITE_SHOW_CFPB_HEADER =
        process.env.VITE_SHOW_CFPB_HEADER ?? viteEnv.VITE_SHOW_CFPB_HEADER

      return config
    }
  },
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite'
    }
  }
})
