import { AccountSearchPage } from '@cypress/helpers/accountSearchHelpers'
import { Metro2Table } from '@cypress/helpers/tableHelpers'
import { PII_COOKIE_NAME } from '@src/constants/settings'
import AccountSummary from '@src/types/AccountSummary'
import { expect } from 'chai'
import 'cypress-real-events/support'

const page = new AccountSearchPage()
const table = new Metro2Table()

const EXPECTED_TABLE_HEADERS = [
  'Account number',
  'Portfolio type',
  'Account type',
  'Number of records',
  'Total number of hits'
]
const EXPECTED_TABLE_FIELDS = [
  'cons_acct_num',
  'port_type',
  'acct_type',
  'total_records',
  'total_hits'
]

const ACCOUNT_ONE = {
  cons_acct_num: '1234',
  total_hits: 2,
  total_records: 3,
  port_type: 'I',
  acct_type: '00'
}

const ACCOUNT_TWO = {
  cons_acct_num: '5678',
  total_hits: 1,
  total_records: 3,
  port_type: 'I',
  acct_type: '00'
}

// ******** Search form ******//
describe('Account search', () => {
  // check the API response for an invalid account
  describe('API check', () => {
    const fakeAccountId = 'not-an-account-number'

    it('Should return an empty array for not found accounts', () => {
      const apiEndpoint = page.getSearchApiEndpoint(fakeAccountId)
      cy.request(apiEndpoint).then(response => {
        const body = response.body as AccountSummary[]
        expect(body).to.deep.equal([])
      })
    })

    it('Should show error message when no accounts found', () => {
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.viewport(1920, 1080)
      cy.visit('/events/1/accounts/')

      // enter fake account id in the search field
      page.getSearchInput().type(fakeAccountId)

      // click the search button
      page.clickSearchButton()

      // url should reflect account search param
      page.hasAccountSearchQuerystring(fakeAccountId)

      // not found message should be visible
      page.hasNotFoundMessage(`We can't find account: ${fakeAccountId}`)

      // results should not be displayed
      page.getSearchResults().should('not.exist')
    })
  })

  describe('Search results', () => {
    beforeEach(() => {
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.viewport(1920, 1080)
      cy.visit('/events/1/accounts/')
    })

    it('Should show data for one valid account', () => {
      // intercept api request for account with id of '1234'
      cy.intercept('GET', '/api/events/1/account/?cons_acct_num=1234', {
        body: [ACCOUNT_ONE],
        delay: 2000
      }).as('accountSearch')

      // search form should be visible on page load
      page.getSearchInput().should('be.visible')

      // but results section should not
      page.getSearchResults().should('not.exist')
      page.getNotFoundMessage().should('not.exist')

      // enter '1234' in the search field
      page.getSearchInput().type('1234')

      // click the search button
      page.clickSearchButton()

      // url should show account search param
      page.hasAccountSearchQuerystring('1234')

      // loading view should show while api request is in progress
      cy.get('.loader').should('be.visible')

      // wait until account search results load
      cy.wait(['@accountSearch'])

      // loading view should now be removed
      cy.get('.loader').should('not.exist')

      // results should now be displayed
      page.getSearchResults().should('be.visible')
      page.hasResultsMessage('Showing 1 result')
      table.getTable().should('be.visible')
      table.verifyHeaders(EXPECTED_TABLE_HEADERS)
      table.hasRowCount(1)
      table.verifyTableBodyContent(table.getBodyRows(), EXPECTED_TABLE_FIELDS, [
        ACCOUNT_ONE
      ])

      // but 'not found' message should not be visible
      page.getNotFoundMessage().should('not.exist')
    })

    it('Should show data for more than one valid account', () => {
      // intercept api request
      page.interceptSearch('1234,5678', [ACCOUNT_ONE, ACCOUNT_TWO], 'getAccounts')

      // Search
      page.getSearchInput().type('1234,5678')
      page.getSearchButton().click()

      // URL should include search params
      page.hasAccountSearchQuerystring('1234,5678')

      cy.wait(['@getAccounts'])

      // results for both accounts should be displayed
      page.hasResultsMessage('Showing 1 - 2 of 2 results')
      table.hasRowCount(2)
      table.verifyTableBodyContent(table.getBodyRows(), EXPECTED_TABLE_FIELDS, [
        ACCOUNT_ONE,
        ACCOUNT_TWO
      ])
    })

    it('Should show error message and results when some accounts found', () => {
      // intercept api request for account with id of '1234,5678'
      page.interceptSearch('1234,5678', [ACCOUNT_ONE], 'accountSearch')

      // enter '1234,5678' in the search field
      page.getSearchInput().type('1234,5678')

      // click the search button
      page.clickSearchButton()

      // url should reflect account search param
      page.hasAccountSearchQuerystring('1234,5678')

      // wait until account search results load
      cy.wait(['@accountSearch'])

      // not found message should be visible
      page.hasNotFoundMessage(`We can't find account: 5678`)

      // results should not be displayed
      page.hasResultsMessage('Showing 1 result')
      table.getTable().should('be.visible')
      table.verifyHeaders(EXPECTED_TABLE_HEADERS)
      table.hasRowCount(1)
      table.verifyTableBodyContent(table.getBodyRows(), EXPECTED_TABLE_FIELDS, [
        ACCOUNT_ONE
      ])
    })
  })

  describe('Search via query param', () => {
    it('Should load search results based on query params', () => {
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.viewport(1920, 1080)

      // intercept api request
      page.interceptSearch('1234,5678', [ACCOUNT_ONE, ACCOUNT_TWO], 'accountSearch')

      // navigate to search page with account ids in query params
      cy.visit('/events/1/accounts?cons_acct_num=1234,5678')

      page.getSearchInput().should('have.value', '1234,5678')

      // wait for data to load
      cy.wait(['@accountSearch'])

      // Search results should be visible
      page.hasResultsMessage('Showing 1 - 2 of 2 results')
      table.hasRowCount(2)
      table.verifyTableBodyContent(table.getBodyRows(), EXPECTED_TABLE_FIELDS, [
        ACCOUNT_ONE,
        ACCOUNT_TWO
      ])
    })
  })

  describe('Search form interactions', () => {
    beforeEach(() => {
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.viewport(1920, 1080)
      cy.visit('/events/1/accounts/')
      // intercept api request for account with id of '1234'
      page.interceptSearch('1234', [ACCOUNT_ONE], 'accountSearch')
    })

    it('Should clear search input when reset button clicked', () => {
      // enter '1234' in the search field
      page.getSearchInput().type('1234')

      // click the search button
      page.clickSearchButton()

      // url should reflect account search param
      page.hasAccountSearchQuerystring('1234')

      // wait until account search results load
      cy.wait(['@accountSearch'])

      // results should now be displayed
      page.getSearchResults().should('be.visible')
      page.hasResultsMessage('Showing 1 result')
      table.getTable().should('be.visible')
      table.verifyHeaders(EXPECTED_TABLE_HEADERS)
      table.hasRowCount(1)
      table.verifyTableBodyContent(table.getBodyRows(), EXPECTED_TABLE_FIELDS, [
        ACCOUNT_ONE
      ])

      // but not found message should not be shown
      page.getNotFoundMessage().should('not.exist')

      // clear form
      page.clickResetButton()

      // input should have no content
      page.getSearchInput().should('contain.value', '')

      // but results should still be displayed
      page.hasAccountSearchQuerystring('1234')
      page.getSearchResults().should('be.visible')
      table.hasRowCount(1)
    })

    it('Should submit search when enter key pressed in input', () => {
      // enter '1234' in the search field
      page.getSearchInput().type('1234{enter}')

      // url should reflect account search param
      page.hasAccountSearchQuerystring('1234')

      // wait until account search results load
      cy.wait(['@accountSearch'])

      // results should now be displayed
      page.getSearchResults().should('be.visible')
    })

    it('Should accommodate tabbing through form', () => {
      // Account search bar is starting point for keyboard interactions
      cy.get('body').realClick()
      cy.findByTestId('account-search-bar').click()

      // Tab order should include search input, reset button, and submit button
      cy.realPress('Tab')
      cy.focused().should('have.attr', 'data-testid', 'account-search-input')
      cy.realPress('Tab')
      cy.focused().should('have.attr', 'data-testid', 'account-search-reset-button')
      cy.realPress('Tab')
      cy.focused().should('have.attr', 'data-testid', 'account-search-submit-button')
    })

    it('Should submit and reset form via keyboard', () => {
      // results should not be visible on page load
      page.getSearchResults().should('not.exist')

      // enter '1234' in the search field
      page.getSearchInput().type('1234')
      page.getSearchInput().realClick()

      // KEYBOARD SUBMIT
      // tab twice to get to submit button
      cy.realPress('Tab')
      cy.realPress('Tab')
      cy.focused().should('have.attr', 'data-testid', 'account-search-submit-button')

      // press enter on submit button to submit form
      cy.realPress('Enter')

      // wait until account search results load
      cy.wait(['@accountSearch'])

      // url should contain search params and results should be displayed
      page.hasAccountSearchQuerystring('1234')

      page.getSearchResults().should('be.visible')
      page.hasResultsMessage('Showing 1 result')
      table.verifyTableBodyContent(table.getBodyRows(), EXPECTED_TABLE_FIELDS, [
        ACCOUNT_ONE
      ])

      // KEYBOARD RESET
      // from search input, tab to reset button and press enter to clear form
      page.getSearchInput().realClick()
      cy.realPress('Tab')
      cy.focused().should('have.attr', 'data-testid', 'account-search-reset-button')
      cy.realPress('Enter')

      // input should have no content
      page.getSearchInput().should('contain.value', '')

      // but results should still be displayed
      page.hasAccountSearchQuerystring('1234')

      page.getSearchResults().should('be.visible')
      table.hasRowCount(1)
    })
  })

  describe('Account search validation', () => {
    describe('Form validation', () => {
      beforeEach(() => {
        cy.setCookie(PII_COOKIE_NAME, 'true')
        cy.viewport(1920, 1080)
        cy.visit('/events/1/accounts/')
        page.interceptSearch('1234', [ACCOUNT_ONE], 'accountSearch')
      })

      it('Should sanitize html tags but keep any content in search input', () => {
        page.getSearchInput().type('<p>1234</p>')
        page.clickSearchButton()

        page.hasAccountSearchQuerystring('1234')
        page.getSearchInput().should('have.value', '1234')
        page.getSearchResults().should('be.visible')
        table.hasRowCount(1)
      })

      it('Should remove extraneous spaces in form input', () => {
        page.getSearchInput().type('  1234   ')
        page.clickSearchButton()

        cy.wait(['@accountSearch'])
        page.hasAccountSearchQuerystring('1234')
        page.getSearchInput().should('have.value', '1234')

        page.getSearchResults().should('be.visible')
        table.hasRowCount(1)
      })

      it('Should remove extraneous commas in form input', () => {
        page.getSearchInput().type('1234, , ,')
        page.clickSearchButton()

        cy.wait(['@accountSearch'])
        page.hasAccountSearchQuerystring('1234')
        page.getSearchInput().should('have.value', '1234')

        page.getSearchResults().should('be.visible')
        table.hasRowCount(1)
      })
    })

    describe('Querystring validation', () => {
      beforeEach(() => {
        cy.setCookie(PII_COOKIE_NAME, 'true')
        cy.viewport(1920, 1080)
      })

      it('Should sanitize html tags but keep any content in search querystring', () => {
        page.interceptSearch('1234', [ACCOUNT_ONE], 'accountSearch')

        cy.visit('/events/1/accounts?cons_acct_num=<p>1234</p>')
        page.getSearchInput().should('have.value', '1234')
        cy.wait(['@accountSearch'])

        page.getSearchResults().should('be.visible')
        table.hasRowCount(1)
      })

      it('Should remove extraneous spaces in search querystring', () => {
        page.interceptSearch('1234', [ACCOUNT_ONE], 'accountSearch')

        cy.visit('/events/1/accounts?cons_acct_num=  1234   ')
        page.getSearchInput().should('have.value', '1234')
        cy.wait(['@accountSearch'])

        page.getSearchResults().should('be.visible')
        table.hasRowCount(1)
      })

      it('Should remove extraneous commas in search querystring', () => {
        page.interceptSearch('1234', [ACCOUNT_ONE], 'accountSearch')

        cy.visit('/events/1/accounts?cons_acct_num=1234, , , ')
        page.getSearchInput().should('have.value', '1234')
        cy.wait(['@accountSearch'])

        page.getSearchResults().should('be.visible')
        table.hasRowCount(1)
      })
    })
  })
})
