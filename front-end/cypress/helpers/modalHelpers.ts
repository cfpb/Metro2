import {
  DOWNLOAD_ACKNOWLEDGMENT_LABEL,
  DOWNLOAD_ACKNOWLEDGMENT_TEXT
} from '@src/config'

export const getInputByLabel = (label: string) => {
  return cy
    .contains('label', label)
    .invoke('attr', 'for')
    .then(id => {
      cy.get(`#${String(id)}`)
    })
}

export class Metro2Modal {
  getModal() {
    return cy.get('.modal')
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
