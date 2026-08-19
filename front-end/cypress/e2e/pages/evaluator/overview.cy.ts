import eventFixture from '@cypress/fixtures/event_1.json'
import { PII_COOKIE_NAME } from '@src/constants/settings'
import type Event from '@src/types/Event'

import { EvaluatorPage } from '@cypress/helpers/evaluatorPageHelpers'
import { Metro2Page } from '@cypress/helpers/pageHelper'
import EvaluatorMetadata from '@src/types/EvaluatorMetadata'

// Get data from event fixture
const event: Event = eventFixture

const evaluatorName = 'Test-Eval-1'

// Get evaluator data from event
const evaluator: EvaluatorMetadata = event.evaluators.find(
  item => item.id == evaluatorName
)!

// Instantiate helpers
const page = new Metro2Page()
const evaluatorPage = new EvaluatorPage()

describe('Evaluator page', () => {
  beforeEach(() => {
    evaluatorPage.loadEvaluatorPage()
  })

  describe('Page overview', () => {
    it('Should show information about the evaluator in the locator bar', () => {
      page.verifyLocatorBarContent('Evaluator', evaluatorName)
    })

    it('Should show breadcrumbs back to the parent event page', () => {
      page.verifyBreadcrumbs([{ text: 'Back to event results', href: '/events/1' }])
    })

    it('Should show summary information in the Details section', () => {
      cy.contains('Details').should('be.visible')
      const summaryItems = [
        { key: 'Data from', value: '01/30/20 - 11/30/20' },
        { key: 'Duration', value: '01/30/20 - 11/30/20' },
        { key: 'Total instances', value: '1,000' },
        { key: 'Total accounts affected', value: '450' },
        {
          key: 'Category',
          value: 'Delinquency'
        }
      ]
      page.verifySummary(summaryItems)
    })

    it('Should display the short description of the evaluator', () => {
      cy.contains('Description').should('be.visible')
      cy.contains(evaluator.description).should('be.visible')
    })

    it('Should display the long description of the evaluator in an expandable', () => {
      // Clicking the long description expandable target should open the expandable
      page.getExpandableTargetByText('Criteria evaluated').click()

      // The expandable should contain the long description html
      page
        .getExpandableByText('Criteria evaluated')
        .should('be.visible')
        .and('include.html', evaluator.long_description)
    })
  })
})

describe('Evaluator metadata', () => {
  it('Should display metadata fields when populated', () => {
    // Load evaluator that has some metadata content
    // Populated fields: rationale and crrg_reference
    // Empty fields: potential_harm and alternate_explanation
    evaluatorPage.loadEvaluatorPage()

    // Clicking the expandable target should open the metadata expandable
    page.getExpandableTargetByText('How to evaluate these results').click()
    page.getExpandableByText('How to evaluate these results').should('be.visible')

    cy.findByTestId('metadata')
      .should('be.visible')
      .within(() => {
        // Metadata fields with content should be output
        cy.contains('h4', 'Rationale').should('exist')
        cy.findByTestId('rationale')
          .should('exist')
          .and('contain.html', evaluator.rationale)
        cy.contains('h4', 'CRRG reference').should('exist')
        cy.findByTestId('crrg_reference').should(
          'contain.html',
          evaluator.crrg_reference
        )

        // Metadata fields without content should be skipped
        cy.contains('h4', 'Potential harm').should('not.exist')
        cy.findByTestId('potential_harm').should('not.exist')
        cy.contains('h4', 'Alternate explanation').should('not.exist')
        cy.findByTestId('alternate_explanation').should('not.exist')
      })
  })

  it('Should display a no-metadata message when no metadata populated', () => {
    // Load evaluator without metadata content
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.visit('/events/1/evaluators/Test-Eval-2/')
    cy.wait(['@getEvent', '@getUser'])

    // Clicking the expandable target should open the metadata expandable
    page.getExpandableTargetByText('How to evaluate these results').click()
    page.getExpandableByText('How to evaluate these results').should('be.visible')

    cy.findByTestId('metadata').should('not.exist')
    cy.findByTestId('no-metadata-message').should('be.visible')
  })

  it('Should display a has metadata cta for a non-admin user', () => {
    // Load evaluator with some metadata content
    // with a non-admin user
    evaluatorPage.loadEvaluatorPage()

    // Clicking the expandable target should open the metadata expandable
    page.getExpandableTargetByText('How to evaluate these results').click()
    page.getExpandableByText('How to evaluate these results').should('be.visible')

    // The has metadata contribute message should be visible
    cy.findByTestId('metadata-contribute').should('be.visible')

    // The other contribute messages should not exist
    cy.findByTestId('metadata-contribute-admin').should('not.exist')
    cy.findByTestId('no-metadata-contribute').should('not.exist')
  })

  it('Should display a no metadata cta for a non-admin user', () => {
    // Load evaluator without metadata content
    // with a non-admin user
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.visit('/events/1/evaluators/Test-Eval-2/')
    cy.wait(['@getEvent', '@getUser'])

    // Clicking the expandable target should open the metadata expandable
    page.getExpandableTargetByText('How to evaluate these results').click()
    page.getExpandableByText('How to evaluate these results').should('be.visible')

    // The no metadata contribute message should be visible
    cy.findByTestId('no-metadata-contribute').should('be.visible')

    // The other contribute messages should not exist
    cy.findByTestId('metadata-contribute-admin').should('not.exist')
    cy.findByTestId('metadata-contribute').should('not.exist')
  })

  it('Should display an admin cta for an admin user', () => {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'userAdmin' }).as('getUser')
    cy.visit('/events/1/evaluators/Test-Eval-1/')
    cy.wait(['@getEvent', '@getUser'])

    // Clicking the expandable target should open the metadata expandable
    page.getExpandableTargetByText('How to evaluate these results').click()
    page.getExpandableByText('How to evaluate these results').should('be.visible')

    // The contribute message for admins should be visible
    cy.findByTestId('metadata-contribute-admin').should('be.visible')

    // The other contribute messages should not exist
    cy.findByTestId('metadata-contribute').should('not.exist')
    cy.findByTestId('no-metadata-contribute').should('not.exist')
  })
})
