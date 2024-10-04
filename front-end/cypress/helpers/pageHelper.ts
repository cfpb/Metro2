/* eslint-disable cypress/require-data-selectors */

export class Metro2Page {
  verifyLocatorBarContent(eyebrow: string, heading: string) {
    cy.get('.header-with-icon').should('be.visible')
    cy.findByTestId('locator-bar-eyebrow').should('have.text', eyebrow)
    cy.findByTestId('locator-bar-heading').should('have.text', heading)
  }

  verifyEventLocatorBarContent(heading: string, subhead: string) {
    cy.get('.header-with-icon').should('be.visible')    
    cy.findByTestId('locator-bar-heading').should('have.text', heading)
    cy.findByTestId('locator-bar-subhead').should('have.text', subhead)
  }

  verifyBreadcrumbs(breadcrumbs: [{ text: string; href: string }]) {
    cy.get('.m-breadcrumbs')
      .should('be.visible')
      .find('.m-breadcrumbs_crumb')
      .should('have.length', breadcrumbs.length)
      .each((breadcrumb, index) => {
        const expectedValue = breadcrumbs[index]
        cy.wrap(breadcrumb)
          .should('be.visible')
          .and('include.text', expectedValue.text)
          .and('have.attr', 'href', expectedValue.href)
      })
  }

  // verify that summary section displays expected key/value pairs
  verifySummary(summaryItems: { key: string; value: string }[]) {
    for (const item of summaryItems) {
      cy.contains(item.key).should('exist').next().should('include.text', item.value)
    }
  }

  getExpandableByText(text: string) {
    return this.getExpandableTargetByText(text)
      .parents('.o-expandable')
      .find('.o-expandable_content')
  }

  getExpandableTargetByText(text: string) {
    return cy.get('button').contains(text)
  }
  verifyDirectSummaryDownload(
    suggestedFileName: string,
    types: { description: string; accept: { [key: string]: string[] } }[]
  ) {
    cy.window().then((win) =>
      cy.stub(win, 'showSaveFilePicker').as('showSaveFilePicker').returns(true),
    )  
    cy.contains("button", 'Download summary')
    .click();
  
    cy.get('@showSaveFilePicker')
      .should('have.been.calledOnceWith', {
        startIn: 'downloads',
        suggestedName: suggestedFileName,
        types: types
      })
      .invoke('restore')
  }
}
