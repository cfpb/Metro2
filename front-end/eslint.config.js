import { defineConfig } from 'eslint/config'

import js from '@eslint/js'
import prettierConfig from 'eslint-config-prettier'
import pluginCypress from 'eslint-plugin-cypress'
import importPlugin from 'eslint-plugin-import'
import jsxA11y from 'eslint-plugin-jsx-a11y'
import reactPlugin from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'
import testingLibrary from 'eslint-plugin-testing-library'
import unicorn from 'eslint-plugin-unicorn'
import globals from 'globals'
import tseslint from 'typescript-eslint'

export default defineConfig([
  {
    ignores: [
      'dist',
      'coverage',
      'node_modules',
      '.yarn',
      '*.config.js',
      '*.config.ts',
      'cypress',
      'postcss',
      'src/components/Table/suppressKeyboardEvents.tsx'
    ]
  },

  // Base JS & TS Recommended
  js.configs.recommended,
  importPlugin.flatConfigs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,

  // A11y
  jsxA11y.flatConfigs.recommended,

  // React
  reactPlugin.configs.flat.recommended,
  // Add this if using React 17+ JSX transform
  reactPlugin.configs.flat['jsx-runtime'],

  // Testing Library
  testingLibrary.configs['flat/react'],

  // Unicorn & Storybook
  unicorn.configs.recommended,

  // Prettier always last
  prettierConfig,

  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.jest
      },
      parserOptions: {
        project: './tsconfig.eslint.json',
        tsconfigRootDir: import.meta.dirname
      }
    },

    plugins: {
      'react-hooks': reactHooks,
      'testing-library': testingLibrary
    },
    settings: {
      react: { version: '19' },

      // Tell eslint-plugin-import how to resolve TS/JS files.
      'import/resolver': {
        typescript: {
          project: './tsconfig.json'
        }
      }
    },
    rules: {
      // Add your custom overrides here
      'no-console': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'unicorn/prevent-abbreviations': 'off', // Airbnb was less strict than Unicorn
      'unicorn/null-data-property': 'off',
      'unicorn/no-null': 'off',
      'react/prop-types': 'off', // Using TypeScript, so don't use PropTypes.
      // Resolver cannot resolve @cfpb/cfpb-design-system src subpaths (Vite alias + node_modules do at build/runtime).
      'import/no-unresolved': ['error', { ignore: ['^@cfpb/cfpb-design-system/'] }],
      'unicorn/filename-case': 'off'
    }
  },
  //Overrides for Tests
  {
    files: ['**/*.spec.tsx'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off'
    }
  },

  {
    files: ['cypress/**/*.{cy.ts,ts,tsx}'],
    plugins: {
      cypress: pluginCypress
    },
    extends: [
      pluginCypress.configs.recommended // Enables recommended Cypress rules and globals
    ],

    rules: {
      // Optional: adjust specific Cypress rules
      'cypress/no-unnecessary-waiting': 'off',
      '@typescript-eslint/require-await': 'off', // Disable the rule
      'cypress/no-async-tests': 'error' // Ensure you use the cypress rule instead
    }
  }
])
