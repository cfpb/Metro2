/* eslint-disable cypress/require-data-selectors */
export const getInputByLabel = (label: string) => {
  return cy
    .contains('label', label)
    .invoke('attr', 'for')
    .then(id => {
      cy.get(`#${String(id)}`)
    })
}

const piiCheckboxLabel =
  'I confirm that I am knowingly downloading PII or CI and understand that I am responsible for safeguarding this data'

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

  verifyPrivacyMessage() {
    // This is just an excerpt; could test the whole thing
    cy.contains(
      'I understand that by downloading data from this system, I will be accessing Personally Identifiable Information (PII) and Confidential Information (CI)'
    ).should('be.visible')
  }

  getPIICheckboxLabel() {
    return cy.get('label').contains(piiCheckboxLabel)
  }

  getPIICheckbox() {
    return getInputByLabel(piiCheckboxLabel)
  }

  checkPIICheckbox() {
    this.getPIICheckboxLabel().click()
  }

  getCloseButton() {
    return cy.get('button').contains('Cancel')
  }

  getSaveButton() {
    return cy.get('button').contains('Save file')
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

  // Ensure that the FileSystemAPI save dialog is launched when the save
  // button is clicked, with expected parameters of a suggested file name,
  // a starting directory, and a file type
  verifyShowSaveFilePicker(
    suggestedFileName: string,
    types: { description: string; accept: { [key: string]: string[] } }[]
  ) {
    cy.window().then(win =>
      cy.stub(win, 'showSaveFilePicker').as('showSaveFilePicker').returns(true)
    )
    this.checkPIICheckbox()
    this.getSaveButton().click()

    cy.get('@showSaveFilePicker')
      .should('have.been.calledOnceWith', {
        startIn: 'downloads',
        suggestedName: suggestedFileName,
        types: types
      })
      .invoke('restore')
  }
}
