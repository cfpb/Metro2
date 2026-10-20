import '@testing-library/cypress/add-commands'
import 'cypress-real-events/support'

Cypress.on('uncaught:exception', error => {
  // we expect the api to return 401 for unauthorized errors
  // and don't want to fail the test so we return false
  if (
    error.message.includes('401') ||
    error.message.includes('500') ||
    error.message.includes('handle.createWritable is not a function') ||
    error.message.includes(
      'ResizeObserver loop completed with undelivered notifications'
    ) ||
    error.message.includes('ResizeObserver loop limit exceeded')
  ) {
    return false
  }
  // we still want to ensure there are no other unexpected
  // errors, so we let them fail the test
})
