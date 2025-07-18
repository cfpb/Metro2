import { PII_COOKIE_NAME } from '@src/constants/settings'
import eventData from '../fixtures/event.json'
import { Metro2Page } from '../helpers/pageHelper'
import { Metro2Table } from '../helpers/tableHelpers'

// Instantiate helpers
const table = new Metro2Table()
const eventPage = new Metro2Page()

describe('Event page loader', () => {
  it('Should show a loading view while event data fetched', () => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1', {
      delay: 2000,
      fixture: 'event'
    }).as('getEvent')
    cy.visit('/events/1')
    cy.get('.loader').should('be.visible')
    cy.wait('@getEvent')
    cy.get('.loader').should('not.exist')
  })
})

describe('Event page', () => {
  beforeEach(() => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1', { fixture: 'event' }).as('getEvent')
    cy.visit('/events/1')
  })
  it('Should show locator', () => {
    cy.get('.locator-bar').should('be.visible')
  })
  it('Should show event title and date range for ID 1 in locator bar', () => {
    eventPage.verifyEventLocatorBarContent(
      eventData.name,
      'Data from Jan 2020 - Nov 2020'
    )
  })
  it('Should show correct headers for evaluator table', () => {
    const expectedHeaders = eventData.headers
    table.verifyHeaders(expectedHeaders)
  })
  it('Should show correct number of evaluators', () => {
    table.getBodyRows().should('have.length', eventData.evaluators.length)
  })
  it('Should show correct evaluator value per row', () => {
    const fields = ['id', 'description', 'category', 'hits', 'accounts_affected']
    table.verifyAccountTableBodyContent(
      table.getBodyRows(),
      fields,
      eventData.evaluators
    )
  })
  it('Should contain the correct URL per evaluator', () => {
    table.getBodyRows().each((row, rowIndex) => {
      const rowEvaluator = eventData.evaluators[rowIndex]
      cy.wrap(row)
        .find('.ag-cell-value')
        .then(cells => {
          //verifying the URL for each evaluator
          cy.get(cells[0])
            .find('a')
            .should('have.attr', 'href')
            .and('include', '/evaluators/' + rowEvaluator.id)
        })
    })
  })
})

describe('Event file download', () => {
  beforeEach(() => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1', { fixture: 'event' }).as('getEvent')
    cy.visit('/events/1')
  })
  it('Should have "Save summary" button', () => {
    cy.get('.downloader')
      .find('button')
      .should('contain', 'Save summary')
  })
})
