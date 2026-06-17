const DOWNLOAD_ACKNOWLEDGMENT_TEXT =
  'I understand that by downloading data from this system, I will be accessing Personally Identifiable Information (PII) and Confidential Information (CI).'

const DOWNLOAD_ACKNOWLEDGMENT_LABEL =
  'I confirm that I am knowingly downloading PII or CI and understand that I am responsible for safeguarding this data.'

export const getInputByLabel = (label: string) => {
  return cy
    .contains('label', label)
    .invoke('attr', 'for')
    .then(id => {
      cy.get(`#${String(id)}`)
    })
}

export class Metro2Modal {
  getModal(testid: string | null = null) {
    return testid ? cy.get(`[data-testid="${testid}"].modal`) : cy.get('.modal')
  }

  openModal(buttonText: string): Cypress.Chainable<JQuery> {
    cy.get('button').contains(buttonText).click()
    return this.getModal()
  }

  closeModal() {
    this.getModal().within(() => {
      this.getCloseButton().click()
    })
  }

  getDownloadAcknowledgment() {
    return cy.findByTestId('download-acknowledgment')
  }

  verifyPrivacyMessage() {
    cy.contains(DOWNLOAD_ACKNOWLEDGMENT_TEXT).should('be.visible')
  }

  getPIICheckboxLabel() {
    return cy.contains(DOWNLOAD_ACKNOWLEDGMENT_LABEL)
  }

  getPIICheckbox() {
    return getInputByLabel(DOWNLOAD_ACKNOWLEDGMENT_LABEL)
  }

  checkPIICheckbox() {
    this.getPIICheckboxLabel().click()
  }

  getCloseButton() {
    return cy.contains('button', 'Cancel')
  }

  getSaveButton() {
    return cy.contains('button', 'Download')
  }

  verifyPrivacyCheckboxRequired() {
    this.getModal().within(() => {
      // privacy checkbox should be unchecked
      this.getPIICheckbox().should('exist').and('not.be.checked')
      // save button should be disabled
      this.getSaveButton().should('have.attr', 'disabled')
      // clicking the privacy checkbox should enable the save button
      this.checkPIICheckbox()
      this.getSaveButton().should('not.have.attr', 'disabled')
    })
  }
}
