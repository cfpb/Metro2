/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable unicorn/prefer-set-has */
import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { expect } from 'chai'

xdescribe('API', () => {
  it('Should return only the expected fields for an account record', () => {
    cy.request('GET', '/api/events/1/account/11111/').then(response => {
      expect(response.status).to.eq(200)
      // Get a list of all the Metro2 account record fields we expect in the front end code
      const expectedFields = [...M2_FIELD_NAMES.keys()]
      // Get a list of all the fields returned on this account's records
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      const sampleRecord = response.body.account_activity[0]
      // filter out fields we expect but aren't part of a Metro 2 account record
      // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
      const fields = Object.keys(sampleRecord).filter(
        field => !['id', 'inconsistencies'].includes(field)
      )
      // Verify that there aren't any unexpected fields in the records returned for this account
      // eslint-disable-next-line @typescript-eslint/no-unused-expressions
      expect(fields.every(field => expectedFields.includes(field))).to.be.true
    })
  })
})

// Test errors using actual API instead of mocks
// Requires running API and database with event 1
xdescribe('Not found errors', () => {
  it('Should render a not found message for a non-existent route', () => {
    cy.visit('/not-a-real-route')

    cy.get('[data-testid="error-title"]').should(
      'have.text',
      'The page doesn’t exist.'
    )
  })

  it('Should render a not found message for a non-existent event', () => {
    cy.visit('/events/123456789')

    cy.get('[data-testid="error-title"]').should(
      'have.text',
      'The page doesn’t exist.'
    )
  })

  it('Should render a not found message for a non-existent evaluator', () => {
    // expect an unhandled promise exception
    cy.once('uncaught:exception', () => false)

    cy.intercept('/api/events/1/evaluator/not-an-evaluator/').as(
      'nonexistentEvaluator'
    )

    cy.visit('/events/1/evaluators/not-an-evaluator')

    cy.wait('@nonexistentEvaluator').its('response.statusCode').should('eq', 404)

    cy.get('[data-testid="error-title"]').should(
      'have.text',
      `The results for this evaluator don’t exist.`
    )
  })

  it('Should render a not found message for a non-existent account', () => {
    cy.intercept('/api/events/1/account/not-an-account/').as('nonexistentAccount')

    cy.visit('/events/1/accounts/not-an-account')

    cy.wait('@nonexistentAccount').its('response.statusCode').should('eq', 404)

    cy.get('[data-testid="error-title"]').should(
      'have.text',
      `The account doesn’t exist.`
    )
  })
})
