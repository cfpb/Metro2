/* eslint-disable @typescript-eslint/no-non-null-assertion */
/* eslint-disable import/extensions */
/* eslint-disable cypress/require-data-selectors */
import type Event from 'types/Event'
import hitsFixture from '../fixtures/evaluatorHits.json'
import eventFixture from '../fixtures/event.json'

import AccountRecord from 'types/AccountRecord'
import EvaluatorMetadata from 'types/EvaluatorMetadata'
import { EvaluatorPage } from '../helpers/evaluatorPageHelpers'
import { Metro2Modal } from '../helpers/modalHelpers'
import { Metro2Page } from '../helpers/pageHelper'

// Get data from event fixture
const event: Event = eventFixture

const evaluatorName = 'Test-Eval-1'

// Get evaluator data from event
const evaluator: EvaluatorMetadata = event.evaluators.find(
  item => item.id == evaluatorName
)!

// Get data from hits fixture
const hits: AccountRecord[] = hitsFixture.hits

// Instantiate helpers
const page = new Metro2Page()
const modal = new Metro2Modal()
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
      // Clicking the expandable target should open the expandable
      page.getExpandableTargetByText('Criteria evaluated').click()
      page.getExpandableByText('Criteria evaluated').should('be.visible')

      // All the segments of the long description should be displayed
      for (const segment of evaluator.long_description.split('\n')) {
        page
          .getExpandableByText('Criteria evaluated')
          .should('include.text', segment)
      }
    })

    it('Should display how to evaluate content in an expandable', () => {
      const howToSections = [
        'Rationale',
        'Potential harm',
        'CRRG reference',
        'Alternate explanation'
      ]

      // Clicking the expandable target should open the expandable
      page.getExpandableTargetByText('How to evaluate these results').click()
      page
        .getExpandableByText('How to evaluate these results')
        .should('be.visible')
        .and(
          'include.text',
          'Help make this tool more useful: Your experience and knowledge about specific evaluators can help others. Consider adding'
        )
        .find('li')
        .each((item, itemIndex) => {
          cy.wrap(item).should('have.text', howToSections[itemIndex])
        })
    })
  })
})
