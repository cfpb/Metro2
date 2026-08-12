import type { AccountSearchSchema } from '@src/pages/Account/AccountSearchPage/utils/accountSearchSchema'
import type AccountSummary from '@src/types/AccountSummary'
import { stringifySearchParams } from '@src/utils/customStringify'

export class AccountSearchPage {
  searchInput() {
    return 'account-search-input'
  }

  getQueryString(params?: AccountSearchSchema) {
    return params ? stringifySearchParams(params) : ''
  }

  getSearchApiEndpoint(accountIds: string) {
    return `api/events/1/account/${accountIds ? this.getQueryString({ cons_acct_num: accountIds }) : ''}`
  }

  interceptSearch(accountIds: string, data: AccountSummary[], alias: string): void {
    cy.intercept('GET', `/api/events/1/account/?cons_acct_num=${accountIds}`, {
      body: data
    }).as(alias)
  }

  getSearchInput() {
    return cy.findByTestId(this.searchInput())
  }

  getSearchResults() {
    return cy.findByTestId('account-search-results')
  }

  getSearchResultsMessage() {
    return cy.findByTestId('account-search-results-message')
  }

  getNotFoundMessage() {
    return cy.findByTestId('account-not-found-message')
  }

  getResetButton() {
    return cy.findByTestId('account-search-reset-button')
  }

  clickResetButton() {
    this.getResetButton().click()
  }

  getSearchButton() {
    return cy.findByTestId('account-search-submit-button')
  }

  clickSearchButton() {
    this.getSearchButton().click()
  }

  hasAccountSearchQuerystring(accountIds?: string) {
    const querystring =
      accountIds && accountIds.length > 0 ? `?cons_acct_num=${accountIds}` : ''
    cy.location('search').should('eq', querystring)
  }

  hasResultsMessage(msg: string) {
    this.getSearchResultsMessage().should('be.visible').and('include.text', msg)
  }

  hasNotFoundMessage(msg: string) {
    this.getNotFoundMessage().should('be.visible').and('contain.text', msg)
  }
}
