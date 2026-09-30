import { EvaluatorPage } from '@cypress/helpers/evaluatorPageHelpers'
import { Metro2Modal } from '@cypress/helpers/modalHelpers'
import { stripHtmlTags } from '@cypress/helpers/utils'
import { PII_COOKIE_NAME } from '@src/constants/settings'
import { expect } from 'chai'

import type Event from '@src/types/Event'

// Instantiate helpers
const modal = new Metro2Modal()
const evaluatorPage = new EvaluatorPage()

describe('Evaluator download modal', () => {
  beforeEach(() => {
    evaluatorPage.loadEvaluatorPage()
  })

  it('Should show download modal when button is clicked', () => {
    modal.getModal('download-modal').should('not.be.visible')
    cy.findByTestId('evaluator-save-button').should('be.visible').click()
    modal
      .getModal('download-modal')
      .should('be.visible')
      .within(() => {
        // This is a partial check of some of the modal content
        // Might want to consider what content we check as a smoke test
        cy.get('h1').should('have.text', 'Save results')
        cy.get('legend').should('include.text', 'Download')
        modal.verifyPrivacyMessage()
      })
  })

  it('Should close the modal when the cancel button is clicked', () => {
    modal.getModal('download-modal').should('not.be.visible')
    modal.openModal('Save results', 'download-modal')
    modal.getModal('download-modal').should('be.visible')
    modal.closeModal('download-modal')
    modal.getModal('download-modal').should('not.be.visible')
  })

  it('Should show a download acknowledgment message from env variable', () => {
    modal.openModal('Save results', 'download-modal')
    cy.env(['VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT']).then(
      ({ VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT }) => {
        modal
          .getModal('download-modal')
          .should('be.visible')
          .within(() => {
            cy.findByTestId('download-acknowledgment-text').should(
              'include.text',
              stripHtmlTags(VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT as string)
            )
          })
      }
    )
  })

  it('Should not allow downloading if privacy notice is not accepted', () => {
    modal.openModal('Save results', 'download-modal')
    modal.verifyPrivacyCheckboxRequired('download-modal')
  })
})

describe('Evaluator download scenarios', () => {
  let event: Event

  beforeEach(() => {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')

    // Create default event with an evaluator that has 100 hits
    event = {
      id: 1,
      name: 'Browser testing event',
      portfolio: '',
      eid_or_matter_num: '',
      other_descriptor: '',
      date_range_start: '2020-01-30',
      date_range_end: '2020-11-30',
      evaluators: [
        {
          inconsistency_start: '2020-01-30',
          inconsistency_end: '2020-11-30',
          id: 'Test-Eval-1',
          description: 'This is a test evaluator.',
          long_description: '<h4>Heading</h4><p>Condition</p>',
          fields_used: ['dofd', 'current_bal'],
          category: 'Test category',
          hits: 100,
          accounts_affected: 100
        }
      ]
    }
  })

  it('Should download a representative sample', () => {
    // intercept event request with default evaluator that has 100 hits
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // intercept hits url with a fixture showing a count of 20
    // (equal to representative sample size)
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'sample' })}`,
      {
        body: {
          count: 20,
          hits: [{ cons_acct_num: '123456' }]
        }
      }
    ).as('getHits')

    // load page and wait for all the data
    cy.visit('/events/1/evaluators/Test-Eval-1/?view=sample')
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // Open modal
    cy.findByTestId('evaluator-save-button').click()

    // Download modal should include representative sample messaging
    modal.getModal('download-modal').within(() => {
      cy.get('legend').should(
        'include.text',
        'Download representative sample of results'
      )
      modal.getSaveButton().should('include.text', 'Download 20 sample results')

      // Accept the privacy warning and click download
      modal.checkPIICheckbox()
      modal.getSaveButton().click()

      // A generated CSV should download and contain the account number from the fixture
      // in the first row
      const expectedCSV =
        'cypress/downloads/Browser-testing-event_Test-Eval-1_sample.csv'
      cy.readFile(expectedCSV).should('exist')
      evaluatorPage.verifyFirstCSVCell(expectedCSV, '123456')
    })
  })

  it('Should download all results', () => {
    // Set total hits on test evaluator to 1000
    event.evaluators[0].hits = 1000

    // intercept event
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // intercept hits with a fixture that has a hits count of 20
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'all' })}`,
      { body: { count: 20, hits: [{ cons_acct_num: '123456' }] } }
    ).as('getHits')

    // spy on the CSV url for this evaluator
    const csvUrl = evaluatorPage.downloadURL(1, 'Test-Eval-1')
    cy.intercept('GET', csvUrl, cy.spy().as('csvUrl'))

    // wait for page to load
    cy.visit('/events/1/evaluators/Test-Eval-1/?view=all')
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // CSV url hasn't been hit yet
    cy.get('@csvUrl').should('not.been.called')

    // open the download modal
    cy.findByTestId('evaluator-save-button').click()

    modal.getModal('download-modal').within(() => {
      // Download modal should contain all results messaging
      cy.get('legend').should('include.text', 'Download all results')
      modal.getSaveButton().should('include.text', 'Download 1,000 results')

      // Download modal should not include a warning about too many results
      cy.findByTestId('download-size-warning').should('not.exist')

      // clicking the save button should call the csv url
      modal.checkPIICheckbox()
      modal.getSaveButton().click()
      cy.get('@csvUrl').should('have.been.called')
    })
  })

  it('Should download all results on sample tab when there are fewer than 20', () => {
    // Set total hits for evaluator to less than representative sample count
    event.evaluators[0].hits = 15

    // intercept event
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // intercept hits with a fixture that has 15 results
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'all' })}`,
      { body: { count: 15, hits: [{ cons_acct_num: 'abcde' }] } }
    ).as('getHits')

    // spy on the CSV url for this evaluator
    const csvUrl = evaluatorPage.downloadURL(1, 'Test-Eval-1')
    cy.intercept('GET', csvUrl, cy.spy().as('csvUrl'))

    // wait for page to load
    cy.visit('/events/1/evaluators/Test-Eval-1/?view=all')
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // CSV url hasn't been hit yet
    cy.get('@csvUrl').should('not.been.called')

    // open the download modal
    cy.findByTestId('evaluator-save-button').click()
    modal.getModal('download-modal').within(() => {
      // Download modal should include all results messaging
      cy.get('legend').should('include.text', 'Download all results')
      modal.getSaveButton().should('include.text', 'Download 15 results')

      // Download modal should not include a warning about too many results
      cy.findByTestId('download-size-warning').should('not.exist')

      // clicking the save button should call the csv url
      modal.checkPIICheckbox()
      modal.getSaveButton().click()
      cy.get('@csvUrl').should('have.been.called')
    })
  })

  it('Should download all results when filters do not narrow', () => {
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // intercept filtered hits with the full hits count of 100
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'all', acct_stat: ['11'] })}`,
      { body: { count: 100, hits: [{ cons_acct_num: 'abcde' }] } }
    ).as('getHits')

    // spy on the CSV url for this evaluator
    const csvUrl = evaluatorPage.downloadURL(1, 'Test-Eval-1')
    cy.intercept('GET', csvUrl, cy.spy().as('csvUrl'))

    // wait for page to load
    cy.visit(
      `/events/1/evaluators/Test-Eval-1/${evaluatorPage.queryString({ view: 'all', acct_stat: ['11'] })}`
    )
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // open the download modal
    cy.findByTestId('evaluator-save-button').click()
    modal.getModal('download-modal').within(() => {
      // Download modal should include all results messaging
      cy.get('legend').should('include.text', 'Download all results')
      modal.getSaveButton().should('include.text', 'Download 100 results')

      // Download modal should not include a warning about too many results
      cy.findByTestId('download-size-warning').should('not.exist')

      // clicking the save button should call the csv url
      modal.checkPIICheckbox()
      modal.getSaveButton().click()
      cy.get('@csvUrl').should('have.been.called')
    })
  })

  it('Should not allow download if there are no filtered results', () => {
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // intercept filtered hits with no results
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'all', acct_stat: ['11'] })}`,
      { body: { count: 0, hits: [] } }
    ).as('getHits')

    // wait for page to load
    cy.visit(
      `/events/1/evaluators/Test-Eval-1/${evaluatorPage.queryString({ view: 'all', acct_stat: ['11'] })}`
    )
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // download button should be disabled
    cy.findByTestId('evaluator-save-button').should('be.disabled')
  })

  it('Should download filtered results when already in table', () => {
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // set a count of 10 for the filtered hits and generate 10 rows of data
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'all', acct_stat: ['11'] })}`,
      { body: { count: 10, hits: evaluatorPage.generateRecords(10, 'acct-num') } }
    ).as('getHits')

    // wait for page to load
    cy.visit(
      `/events/1/evaluators/Test-Eval-1/${evaluatorPage.queryString({ view: 'all', acct_stat: ['11'] })}`
    )
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // open the download modal
    cy.findByTestId('evaluator-save-button').click()
    modal.getModal('download-modal').within(() => {
      // Download modal should include filtered results messaging
      cy.get('legend').should('include.text', 'Download filtered results')
      modal.getSaveButton().should('include.text', 'Download 10 results')

      // Download modal should not include a warning about too many results
      cy.findByTestId('download-size-warning').should('not.exist')

      // clicking the save button should download a filtered csv
      modal.checkPIICheckbox()
      modal.getSaveButton().click()
      const expectedCSV =
        'cypress/downloads/Browser-testing-event_Test-Eval-1_filtered.csv'
      cy.readFile(expectedCSV).should('exist')
      evaluatorPage.verifyFirstCSVCell(expectedCSV, 'acct-num-0')
    })
  })

  it('Should fetch and download additional filtered results', () => {
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // set a count of 30 for the filtered hits and generate 30 rows of data
    const hits = evaluatorPage.generateRecords(30, 'filtered-acct')
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'all', acct_stat: ['11'] })}`,
      { body: { count: 30, hits: hits.slice(0, 20) } }
    ).as('getHits')

    // wait for page to load
    cy.visit(
      `/events/1/evaluators/Test-Eval-1/${evaluatorPage.queryString({ view: 'all', acct_stat: ['11'] })}`
    )
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // open the download modal
    cy.findByTestId('evaluator-save-button').click()
    modal.getModal('download-modal').within(() => {
      // Download modal should include filtered results messaging
      cy.get('legend').should('include.text', 'Download filtered results')
      modal.getSaveButton().should('include.text', 'Download 30 results')

      // Download modal should not include a warning about too many results
      cy.findByTestId('download-size-warning').should('not.exist')

      // intercept the call for the rest of the data
      const apiExt = evaluatorPage.apiExt({
        view: 'all',
        acct_stat: ['11'],
        page_size: 30
      })
      cy.intercept('GET', `api/events/1/evaluator/Test-Eval-1/${apiExt}`, {
        body: { count: 30, hits: hits }
      }).as('getMoreHits')

      // clicking the save button should download a filtered csv
      modal.checkPIICheckbox()
      modal.getSaveButton().click()
      cy.wait('@getMoreHits')

      const expectedCSV =
        'cypress/downloads/Browser-testing-event_Test-Eval-1_filtered.csv'
      cy.readFile(expectedCSV)
        .should('exist')
        .then((txt: string) => {
          const rows = txt.split('\n')
          expect(rows.length).to.eq(31)
          const firstRowFields = rows[1].split(',')
          expect(firstRowFields[0]).to.eq('filtered-acct-0')
        })
    })
  })

  it('Should download subset when there are too many filtered results', () => {
    event.evaluators[0].hits = 1_000_000
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // set a count of 200_000 for the filtered hits and generate first page of data
    const hits = evaluatorPage.generateRecords(30, 'cons-acct')
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'all', acct_stat: ['11'] })}`,
      { body: { count: 200_000, hits: hits.slice(0, 20) } }
    ).as('getHits')

    // wait for page to load
    cy.visit(
      `/events/1/evaluators/Test-Eval-1/${evaluatorPage.queryString({ view: 'all', acct_stat: ['11'] })}`
    )
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // open the download modal
    cy.findByTestId('evaluator-save-button').click()
    modal.getModal('download-modal').within(() => {
      // Download modal should include filtered results messaging
      cy.get('legend').should('include.text', 'Download filtered results')
      modal.getSaveButton().should('include.text', 'Download first 100,000 results')

      // Download modal should also include a warning about too many results
      cy.findByTestId('download-size-warning').should('be.visible')

      // intercept the call for the rest of the data
      const apiExt = evaluatorPage.apiExt({
        view: 'all',
        acct_stat: ['11'],
        page_size: 100_000
      })
      cy.intercept('GET', `api/events/1/evaluator/Test-Eval-1/${apiExt}`, {
        body: { count: 100_000, hits: hits }
      }).as('getMoreHits')

      // clicking the save button should download a filtered csv
      modal.checkPIICheckbox()
      modal.getSaveButton().click()
      cy.wait('@getMoreHits')

      const expectedCSV =
        'cypress/downloads/Browser-testing-event_Test-Eval-1_filtered.csv'
      cy.readFile(expectedCSV).should('exist')
      evaluatorPage.verifyFirstCSVCell(expectedCSV, 'cons-acct-0')
    })
  })

  it('Should show an error modal if problem downloading additional filtered results', () => {
    cy.intercept('GET', 'api/events/1/', { body: event }).as('getEvent')

    // set a count of 30 for the filtered hits and generate initial 20 rows of data
    cy.intercept(
      'GET',
      `api/events/1/evaluator/Test-Eval-1/${evaluatorPage.apiExt({ view: 'all', acct_stat: ['11'] })}`,
      { body: { count: 30, hits: evaluatorPage.generateRecords(20, 'acct-num') } }
    ).as('getHits')

    // wait for page to load
    cy.visit(
      `/events/1/evaluators/Test-Eval-1/${evaluatorPage.queryString({ view: 'all', acct_stat: ['11'] })}`
    )
    cy.wait(['@getEvent', '@getUser', '@getHits'])

    // intercept the call for the rest of the data with an error
    const apiExt = evaluatorPage.apiExt({
      view: 'all',
      acct_stat: ['11'],
      page_size: 30
    })
    cy.intercept('GET', `api/events/1/evaluator/Test-Eval-1/${apiExt}`, {
      statusCode: 504
    })

    // open the download modal
    cy.findByTestId('evaluator-save-button').click()
    modal.getModal('download-modal').within(() => {
      // clicking the save button should trigger the error
      modal.checkPIICheckbox()
      modal.getSaveButton().click()
    })

    // the download modal should no longer be visible
    modal.getModal('download-modal').should('not.be.visible')

    // the error modal should be visible
    modal
      .getModal('download-error-modal')
      .should('be.visible')
      .within(() => {
        // click to close the error modal
        cy.findByTestId('close-error-modal').click()
      })

    // the error modal should not be visible
    modal.getModal('download-error-modal').should('not.be.visible')
  })
})
