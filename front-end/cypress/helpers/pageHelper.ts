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
    return this.getExpandableTargetByText(text)
      .parents('.o-expandable')
      .get('.o-expandable_content')
  }

  getExpandableTargetByText(text: string) {
    return cy
      .get('.o-expandable_header')
      .contains(text)
      .parents('.o-expandable')
      .find('.o-expandable_target')
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
}
