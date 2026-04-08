import { PII_COOKIE_NAME } from '@src/constants/settings'
import EvaluatorMetadata from '@src/types/EvaluatorMetadata'
import type Event from '@src/types/Event'
import data from '../fixtures/event_1.json'
import { Metro2Page } from '../helpers/pageHelper'
import { Metro2Table } from '../helpers/tableHelpers'
const eventData = data as Event

// Instantiate helpers
const table = new Metro2Table()
const eventPage = new Metro2Page()

import { Metro2Modal } from '../helpers/modalHelpers'
const modal = new Metro2Modal()

describe('Event page loader', () => {
  it('Should show a loading view while event data fetched', () => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1', {
      delay: 2000,
      fixture: 'event_1'
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
    cy.intercept('GET', 'api/events/1', { fixture: 'event_1' }).as('getEvent')
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
    const expectedHeaders = [
      'Evaluator',
      'Description',
      'Category',
      'Total instances',
      'Total accounts'
    ]
    table.verifyHeaders(expectedHeaders)
  })
  it('Should show correct number of evaluators', () => {
    table.getBodyRows().should('have.length', eventData.evaluators.length)
  })
  it('Should show correct evaluator value per row', () => {
    const fields = ['id', 'description', 'category', 'hits', 'accounts_affected']
    table.verifyTableBodyContent<EvaluatorMetadata>(
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
        .then(rowCells => {
          //verifying the URL for each evaluator
          cy.wrap(rowCells)
            .should('have.length', 5)
            .first()
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
    cy.intercept('GET', 'api/events/1', { fixture: 'event_1' }).as('getEvent')
    cy.visit('/events/1')
  })

  it('Should open download modal with active download button', () => {
    modal.openModal('Save summary')
    modal.getModal().within(() => {
      cy.findByTestId('download-acknowledgment').should('not.exist')
      modal.getPIICheckboxLabel().should('not.exist')
      modal.getSaveButton().should('not.have.attr', 'disabled')
    })
  })

  it('Should download event data', () => {
    const eventDownloadData =
      'ID,DESCRIPTION,CATEGORY,HITS,ACCOUNTS AFFECTED\nTest-Eval-1,This is a test evaluator.,Delinquency,1000,450\nTest-Eval-2,Test evaluator.,Bankruptcy,85,17'

    modal.openModal('Save summary')

    modal.getModal().within(() => {
      modal.getSaveButton().click()
      cy.readFile('cypress/downloads/Browser-testing-event.csv')
        .should('exist')
        .and('contain', eventDownloadData)
    })

    modal.getModal().should('not.be.visible')
  })
})
