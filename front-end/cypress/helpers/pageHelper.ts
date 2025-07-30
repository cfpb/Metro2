/* eslint-disable cypress/require-data-selectors */
import { stringifySearchParams } from 'utils/customStringify'

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
    return cy
      .get('.o-expandable_header')
      .contains(text)
      .parents('.o-expandable')
      .first()
      .find('.o-expandable_content')
      .first()
  }

  getExpandableTargetByText(text: string) {
    // We need to find the element that opens the expandable.
    // It could be the entire header or a button within the header,
    // so we get the first expandable parent of the header
    // containing the text (since expandables can be nested)
    // and then find the target within it
    return cy
      .get('.o-expandable_header')
      .contains(text)
      .parents('.o-expandable')
      .first()
      .find('.o-expandable_target')
      .first()
  }

  openExpandable(headerText: string) {
    this.getExpandableTargetByText(headerText).click()
  }

  queryString(params: object) {
    const defaults = { page: 1, page_size: 20, view: 'sample' }
    return stringifySearchParams({ ...defaults, ...params })
  }

  hasQueryString(params: object) {
    cy.url().should('include', this.queryString(params))
  }

  hasURL(path: string, params: object) {
    cy.url().should('eq', `http://localhost:3000/${path}${this.queryString(params)}`)
  }

  checkboxHasState(label: string, state: 'checked' | 'unchecked' | 'indeterminate') {
    if (state === 'checked') {
      this.getInputByLabel(label).should('be.checked')
      cy.contains('label', label).parent().should('not.have.class', 'indeterminate')
    } else if (state === 'unchecked') {
      this.getInputByLabel(label).should('not.be.checked')
      cy.contains('label', label).parent().should('not.have.class', 'indeterminate')
    } else if (state === 'indeterminate') {
      this.getInputByLabel(label).should('not.be.checked')
      cy.contains('label', label).parent().should('have.class', 'indeterminate')
    }
  }

  getInputByLabel(label: string) {
    return cy.contains('label', label).then($label => {
      const inputId = $label.attr('for')
      cy.get(`#${inputId}`)
    })
  }
}
