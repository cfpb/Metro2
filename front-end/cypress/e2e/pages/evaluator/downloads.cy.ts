import { EvaluatorPage } from '@cypress/helpers/evaluatorPageHelpers'
import { Metro2Modal } from '@cypress/helpers/modalHelpers'

// Instantiate helpers
const modal = new Metro2Modal()
const evaluatorPage = new EvaluatorPage()

describe('Evaluator page', () => {
  beforeEach(() => {
    evaluatorPage.loadEvaluatorPage()
  })

  describe('Download modal', () => {
    it('Should show download modal when button is clicked', () => {
      modal.getModal().should('not.be.visible')
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
      modal.getModal().should('not.be.visible')
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
