export class FilterHelpers {
  getAccordionTarget(id: string) {
    return cy
      .get(`input#${id}`)
      .parents('.o-expandable')
      .first()
      .find('.o-expandable__target')
      .first()
  }

  expectAccordionIsDisabled(id: string) {
    cy.get(`input#${id}`)
      .should('be.disabled')
      .parents('.o-expandable__header')
      .should('have.class', 'disabled')
  }

  expectAccordionsAreDisabled(ids: string[]) {
    for (const id of ids) {
      this.expectAccordionIsDisabled(id)
    }
  }

  expectAccordionIsActive(id: string) {
    cy.get(`input#${id}`)
      .should('not.be.disabled')
      .parents('.o-expandable__header')
      .should('not.have.class', 'disabled')
  }

  expectAccordionsAreActive(ids: string[]) {
    for (const id of ids) {
      this.expectAccordionIsActive(id)
    }
  }

  expectCheckboxIsDisabled(id: string) {
    cy.get(`input#${id}`).should('be.disabled')
  }

  expectCheckboxesAreDisabled(ids: string[]) {
    for (const id of ids) {
      this.expectCheckboxIsDisabled(id)
    }
  }

  expectCheckboxIsActive(id: string) {
    cy.get(`input#${id}`).should('not.be.disabled')
  }

  expectCheckboxesAreActive(ids: string[]) {
    for (const id of ids) {
      this.expectCheckboxIsActive(id)
    }
  }
}
