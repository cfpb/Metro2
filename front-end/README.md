# Metro2 Tool Front-End

## Features

- [Vite](https://vitejs.dev) with [React](https://reactjs.org), [TypeScript](https://www.typescriptlang.org) and [absolute imports](https://github.com/aleclarson/vite-tsconfig-paths).
- Uses [ESLint](https://eslint.org), [stylelint](https://stylelint.io) and [Prettier](https://prettier.io) on VSCode and before you commit with [Husky](https://github.com/typicode/husky) and [lint-staged](https://github.com/okonet/lint-staged).
- Unit and integration tests with [Vitest](https://vitest.dev/) and [Testing Library](https://testing-library.com/).
- e2e tests with [Cypress](https://www.cypress.io).

## Getting started

In the `front-end` directory, install the dependencies:

```
yarn install
```

## Scripts

- `yarn dev` - start a development server with hot reload.
- `yarn build` - build for production. The generated files will be on the `dist` folder.
- `yarn preview` - locally preview the production build.
- `yarn test` - run unit and integration tests related to changed files based on git.
- `yarn test:ci` - run all unit and integration tests in CI mode.
- `yarn test:e2e` - run all e2e tests with the Cypress Test Runner.
- `yarn test:e2e:headless` - run all e2e tests headlessly.
- `yarn format` - format all files with Prettier.
- `yarn lint` - runs TypeScript, ESLint and Stylelint.
- `yarn validate` - runs `lint`, `test:ci` and `test:e2e:ci`.
