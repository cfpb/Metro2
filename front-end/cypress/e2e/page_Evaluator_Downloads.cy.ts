import { EvaluatorPage } from '@cypress/helpers/evaluatorPageHelpers'
import { Metro2Modal } from '@cypress/helpers/modalHelpers'
import { stripHtmlTags } from '@cypress/helpers/utils'

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

    it('Should show a download acknowledgment message from env variable', () => {
      modal.openModal('Save results')
      cy.env(['VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT']).then(
        ({ VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT }) => {
          modal
            .getModal()
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

    it('Should not allow downloading unless privacy notice is accepted', () => {
      modal.openModal('Save results')
      modal.verifyPrivacyCheckboxRequired()
    })

    it('Should download sample evaluator results when download button clicked', () => {
      modal.openModal('Save results')
      modal.checkPIICheckbox()
      modal.getSaveButton().click()
      cy.readFile(
        'cypress/downloads/Browser-testing-event_Test-Eval-1_sample.csv'
      ).should('exist')
    })
  })
})
