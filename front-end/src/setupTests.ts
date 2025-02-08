import '@testing-library/jest-dom'

const noop = (): void => {}
Object.defineProperty(window, 'scrollTo', { value: noop, writable: true })
