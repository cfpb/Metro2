import { defineConfig } from "cypress";

export default defineConfig({
  fileServerFolder: "dist",
  projectId: "etow1b",

  e2e: {
    baseUrl: "http://localhost:3000/",
    specPattern: "cypress/e2e/**/*.ts",
  },

  component: {
    devServer: {
      framework: "react",
      bundler: "vite",
    },
  },
});
