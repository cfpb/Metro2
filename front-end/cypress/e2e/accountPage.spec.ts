/* eslint-disable cypress/require-data-selectors */

import '../../src/pages/Account/Account.tsx'
import { PII_COOKIE_NAME } from '../../src/utils/constants'
import accountData from '../fixtures/account.json'
import { getInputByLabel, Metro2Modal } from '../helpers/modalHelpers'
import { Metro2Page } from '../helpers/pageHelper'
import { Metro2Table } from '../helpers/tableHelpers'

// Instantiate helpers
const table = new Metro2Table()
const accountPage = new Metro2Page()
const modal = new Metro2Modal()

// ******** Page loader ******//
describe('Account page loader', () => {
  it('Should show a loading view while account data is fetched', () => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/account/20140800499328/', {
      fixture: 'account'
    }).as('getAccount')
    cy.visit('/events/1/accounts/20140800499328')
    cy.get('.loader').should('be.visible')
    cy.wait('@getAccount')
    cy.get('.loader').should('not.exist')
  })
})

describe('Account page', () => {
  beforeEach(() => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/account/20140800499328/', {
      delay: 2000,
      fixture: 'account'
    }).as('getAccount')
    cy.visit('/events/1/accounts/20140800499328')
    cy.wait('@getAccount')
  })
  it('Should show breadcrumbs back to the parent event page', () => {
    accountPage.verifyBreadcrumbs([
      { text: 'Back to event results', href: '/events/1' }
    ])
  })

  it('Should show information about the evaluator in the locator bar', () => {
    accountPage.verifyLocatorBarContent('Account', '20140800499328')
  })

  //Account details area
  it('Should show account details', () => {
    cy.findAllByTestId('details').find('h2').should('have.text', 'Account Details')
    const detailItems = [
      { key: 'Contact Information', value: '' },
      { key: 'Portfolio type', value: accountData.account_activity[0].port_type },
      { key: 'Account type', value: accountData.account_activity[0].acct_type },
      { key: 'Terms duration', value: accountData.account_activity[0].terms_dur },
      { key: 'Terms frequency', value: accountData.account_activity[0].terms_freq },
      {
        key: 'Date opened',
        value: '08/15/14' /*value: accountData.account_activity[0].date_open*/
      }
    ]
    accountPage.verifySummary(detailItems)
  })
  it('Should show all inconsistencies found', () => {
    cy.findAllByTestId('inconsistencies')
      .find('h2')
      .should('have.text', 'Inconsistencies found')
    cy.get('[data-testid="inconsistencies"] > ol').each((row, rowIndex) => {
      cy.wrap(row)
        .find('li')
        .should('contain', accountData.inconsistencies[rowIndex])
    })
  })
  it('Should have links for each evaluator', () => {
    cy.get('[data-testid="inconsistencies"] > ol')
      .find('li > a')
      .each(($li, index) => {
        cy.get('li > a').eq(index).click()
        cy.location('pathname', { timeout: 1000 }).should(
          'include',
          '/events/1/evaluators/' + accountData.inconsistencies[index]
        )
        cy.go('back')
      })
  })
  it('Should show correct headers for account table', () => {
    const expectedHeaders = accountData.header_title
    table.verifyHeaders(expectedHeaders)
  })

  it('Should show correct account data per column/cell', () => {
    table.verifyAccountTableBodyContent(
      table.getPinnedRows(),
      ['activity_date'],
      accountData.account_activity
    )
    // FIGURE OUT HOW TO TEST REST OF TABLE
    // table.verifyAccountTableBodyContent(
    //   table.getBodyRows(),
    //   [],
    //   accountData.account_activity
    // )
  })
})

// ******** Account data download ******//
describe(
  'Account data download',
  { viewportHeight: 1080, viewportWidth: 1920 },
  () => {
    beforeEach(() => {
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.intercept('GET', 'api/events/1/account/20140800499328/', {
        delay: 2000,
        fixture: 'account'
      }).as('getAccount')
      cy.visit('/events/1/accounts/20140800499328')
      cy.wait('@getAccount')
    })

    it('Should show download modal when button is clicked', () => {
      modal.getModal().should('not.exist')
      cy.get('.downloader > button')
        .contains('Download account data')
        .should('be.visible')
        .click()
      modal
        .getModal()
        .should('be.visible')
        .within(() => {
          // This is a partial check of some of the modal content
          // Might want to consider what content we check as a smoke test
          cy.get('h1').should('have.text', 'Download account data')
          cy.get('h2').should(
            'have.text',
            'Confirmation of ability to d/l PII or CI Statement:'
          )
          modal.verifyPrivacyMessage()
        })
    })
    it('Should close the modal when the cancel button is clicked', () => {
      modal.getModal().should('not.exist')
      modal.openModal('Download account data')
      modal.getModal().should('be.visible')
      modal.closeModal()
      modal.getModal().should('not.exist')
    })
    it('Should not allow downloading unless privacy notice is accepted', () => {
      modal.openModal('Download account data')
      modal.verifyPrivacyCheckboxRequired()
    })
    it('Should reset options when closed', () => {
      const uncheckedOptionLabel =
        'Include latest contact information for account holder'
      modal.openModal('Download account data').within(() => {
        getInputByLabel(uncheckedOptionLabel).should('not.have.attr', 'checked')
        modal.getPIICheckbox().should('not.have.attr', 'checked')
        cy.get('label').contains(uncheckedOptionLabel).click()
        modal.checkPIICheckbox()
      })
      modal.closeModal()
      modal.openModal('Download account data').within(() => {
        getInputByLabel(uncheckedOptionLabel).should('not.have.attr', 'checked')
        modal.getPIICheckbox().should('not.have.attr', 'checked')
      })
    })
    it('Should launch FileSystemAPI save file dialog when save button clicked', () => {
      modal.openModal('Download account data')
      modal.verifyShowSaveFilePicker('Sample-Dataset-007_20140800499328.xlsx', [
        {
          description: 'Excel',
          accept: {
            'text/xlsx': ['.xlsx']
          }
        }
      ])
    })
  }
)
