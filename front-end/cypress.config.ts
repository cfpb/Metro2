import { defineConfig } from 'cypress'

export default defineConfig({
  // Set to false to disable deprecated Cypress.env()
  allowCypressEnv: false, 
  fileServerFolder: 'dist',
  projectId: 'etow1b',

  e2e: {
    baseUrl: 'http://localhost:3000/',
    specPattern: 'cypress/e2e/**/*.ts'
  },

  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite'
    }
  }
})
