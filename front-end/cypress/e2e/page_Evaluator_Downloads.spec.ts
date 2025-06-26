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

  describe('Download modal', () => {
    it('Should show download modal when button is clicked', () => {
      modal.getModal().should('not.exist')
      cy.get('button').contains('Save results').should('be.visible').click()
      modal
        .getModal()
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
      modal.getModal().should('not.exist')
      modal.openModal('Save results')
      modal.getModal().should('be.visible')
      modal.closeModal()
      modal.getModal().should('not.be.visible')
    })

    it('Should not allow downloading unless privacy notice is accepted', () => {
      modal.openModal('Save results')
      modal.verifyPrivacyCheckboxRequired()
    })
  })
})
