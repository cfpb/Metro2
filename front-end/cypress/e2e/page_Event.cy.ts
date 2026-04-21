import data from '@cypress/fixtures/event_1.json'
import { Metro2Modal } from '@cypress/helpers/modalHelpers'
import { Metro2Page } from '@cypress/helpers/pageHelper'
import { Metro2Table } from '@cypress/helpers/tableHelpers'

import { PII_COOKIE_NAME } from '@src/constants/settings'
import { EVENT_COLUMN_MAP } from '@src/pages/Event/utils/eventColumns'
import EvaluatorMetadata from '@src/types/EvaluatorMetadata'
import type Event from '@src/types/Event'
const eventData = data as Event

// Instantiate helpers
const table = new Metro2Table()
const eventPage = new Metro2Page()
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

/**
 * Table sorting
 *
 * 1. When event page is loaded without a sort param in the URL,
 *      URL & table sort should be updated to reflect default sort (id ascending)
 * 2. Clicking another column's sort indicator three times should update sort state,
 *      cycling through ascending sort, descending sort, and then sort removal 
 *      and a return to default sort
 * 4. Navigating to page with non-default sort state in URL should apply that state
 * 5. Sort values in URL should be validated and replaced with id if invalid
 *
 * Excerpt of fields for the two records in the event data fixture
 * 
 *  [
      {
      "hits": 1000,
      "id": "Test-Eval-1",
      "category": "Delinquency"
    },
    {
      "hits": 85,
      "id": "Test-Eval-2",
      "category": "Bankruptcy"
    }
    ]
 */

describe('Sorting is configured for event page', () => {
  beforeEach(() => {
    // Load event page with no sort param
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1', { fixture: 'event_1' }).as('getEvent')
    cy.visit('/events/1')
    cy.wait(['@getEvent'])
  })

  it('Should default to sorting by id when there is no sort param in URL', () => {
    // A sort param of id is added to the URL
    cy.location('search').should('include', 'sort=id')

    // The id column show the sort ascending icon,
    // and all other columns show the unsorted icon
    table.shouldShowSortIcon('id', 'ascending')
    table.otherColumnsShouldBeUnsorted('id')

    // The data in the table is sorted by id ascending
    table.verifyColumnContent('id', ['Test-Eval-1', 'Test-Eval-2'])
    table.verifyColumnContent('category', ['Delinquency', 'Bankruptcy'])
  })

  it('Should update sort state when a column sort button is clicked repeatedly', () => {
    // URL and table show sorting by default column id
    cy.location('search').should('include', 'sort=id')
    table.shouldShowSortIcon('id', 'ascending')
    table.otherColumnsShouldBeUnsorted('id')

    table.verifyColumnContent('id', ['Test-Eval-1', 'Test-Eval-2'])
    table.verifyColumnContent('category', ['Delinquency', 'Bankruptcy'])

    // Click the sort button in the category column
    table.clickSortButton('category')

    // Table and URL should be updated to show sorting by category
    cy.location('search').should('include', 'sort=category')
    table.shouldShowSortIcon('category', 'ascending')
    table.shouldShowUnsortedIcon('id')
    table.verifyColumnContent('id', ['Test-Eval-2', 'Test-Eval-1'])
    table.verifyColumnContent('category', ['Bankruptcy', 'Delinquency'])

    // Click the category sort button again to sort descending
    table.clickSortButton('category')

    // Table and URL should be updated to show sorting by category
    cy.location('search').should('include', 'sort=-category')
    table.shouldShowSortIcon('category', 'descending')
    table.shouldShowUnsortedIcon('id')
    table.verifyColumnContent('id', ['Test-Eval-1', 'Test-Eval-2'])
    table.verifyColumnContent('category', ['Delinquency', 'Bankruptcy'])

    // Clicking the category sort button a third time removes
    // the category sorting and restores default sort
    table.clickSortButton('category')
    cy.location('search').should('include', 'sort=id')
    table.shouldShowSortIcon('id', 'ascending')
    table.shouldShowUnsortedIcon('category')
  })
})

describe('Sorting is applied based on query params', () => {
  it('Should get sort state from url', () => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1', { fixture: 'event_1' }).as('getEvent')
    cy.visit(`/events/1/?sort=category`)
    cy.wait(['@getEvent'])

    cy.location('search').should('include', 'sort=category')
    table.shouldShowSortIcon('category', 'ascending')
    table.otherColumnsShouldBeUnsorted('category')
    table.verifyColumnContent('id', ['Test-Eval-2', 'Test-Eval-1'])
    table.verifyColumnContent('category', ['Bankruptcy', 'Delinquency'])
  })
})

describe('Sort params are validated and used', () => {
  describe('Valid sort param handling', () => {
    // Get event table columns
    const validFields = [...EVENT_COLUMN_MAP.keys()]
    for (const field of validFields) {
      it(`Should accept "${field}" as sort param`, () => {
        eventPage.loadEventPage(field)
        cy.location('search').should('include', `sort=${field}`)
        table.shouldShowSortIcon(field, 'ascending')

        eventPage.loadEventPage(`-${field}`)
        cy.location('search').should('include', `sort=-${field}`)
        table.shouldShowSortIcon(field, 'descending')
      })
    }
  })

  describe('Invalid sort param handling', () => {
    const invalidValues = ['', 'activity_date', 'random']
    for (const val of invalidValues) {
      it(`Should replace invalid sort param "${val}" with default`, () => {
        eventPage.loadEventPage(val)
        cy.location('search').should('include', 'sort=id')
      })
    }
  })
})
