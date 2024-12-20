/* eslint-disable unicorn/prevent-abbreviations */
import '@testing-library/cypress/add-commands'

Cypress.on('uncaught:exception', err => {
  // we expect the api to return 401 for unauthorized errors
  // and don't want to fail the test so we return false
  if (
    err.message.includes('401') ||
    err.message.includes('500') ||
    err.message.includes('handle.createWritable is not a function')
  ) {
    return false
  }
  // we still want to ensure there are no other unexpected
  // errors, so we let them fail the test
})
