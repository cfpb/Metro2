import '@testing-library/jest-dom'

const noop = (): void => void 0
Object.defineProperty(globalThis, 'scrollTo', { value: noop, writable: true })
