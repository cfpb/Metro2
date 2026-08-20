import { getInputByLabel, Metro2Modal } from '@cypress/helpers/modalHelpers'
import { stripHtmlTags } from '@cypress/helpers/utils'
import { PII_COOKIE_NAME } from '@src/constants/settings'
import { accountTableFields } from '@src/pages/Account/AccountPage/utils/accountTableFields'

import accountData from '@cypress/fixtures/account_1.json'
import { Metro2Page } from '@cypress/helpers/pageHelper'
import { Metro2Table } from '@cypress/helpers/tableHelpers'

// Instantiate helpers
const table = new Metro2Table()
const accountPage = new Metro2Page()
const modal = new Metro2Modal()

// ******** Page loader ******//
describe('Account page loader', () => {
  it('Should show a loading view while account data is fetched', () => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', 'api/events/1/account/111111/', {
      fixture: 'account_1',
      delay: 2000
    }).as('getAccount')
    cy.visit('/events/1/accounts/111111')
    cy.get('.loader').should('be.visible')
    cy.wait(['@getEvent', '@getAccount'])
    cy.get('.loader').should('not.exist')
  })
})

describe('Account page', () => {
  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', 'api/events/1/account/111111/', {
      fixture: 'account_1'
    }).as('getAccount')
    cy.visit('/events/1/accounts/111111')
    cy.wait(['@getEvent', '@getAccount'])
  })

  it('Should show breadcrumbs back to the parent event page', () => {
    accountPage.verifyBreadcrumbs([
      { text: 'Back to event results', href: '/events/1' }
    ])
  })

  it('Should show information about the account in the locator bar', () => {
    accountPage.verifyLocatorBarContent('Account', '111111')
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
      .each((link, index) => {
        cy.wrap(link)
          .should('have.attr', 'href')
          .and(
            'include',
            `/events/1/evaluators/${accountData.inconsistencies[index]}`
          )
      })
  })
  // it('Should show correct headers for account table', () => {
  //   const expectedHeaders = accountData.header_title
  //   table.verifyHeaders(expectedHeaders)
  // })
})

// ******** Account data download ******//
describe('Account data download', () => {
  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', 'api/events/1/account/11111/', {
      fixture: 'account_1'
    }).as('getAccount')
    cy.visit('/events/1/accounts/11111')
    cy.wait(['@getEvent', '@getAccount'])
  })

  it('Should show download modal when button is clicked', () => {
    modal.getModal().should('not.be.visible')
    cy.get('.downloader > button')
      .contains('Save account data')
      .should('be.visible')
      .click()
    modal
      .getModal()
      .should('be.visible')
      .within(() => {
        cy.get('h1').should('have.text', 'Save account data')
        modal.verifyPrivacyMessage()
      })
  })
  it('Should close the modal when the cancel button is clicked', () => {
    modal.getModal().should('not.be.visible')
    modal.openModal('Save account data')
    modal.getModal().should('be.visible')
    modal.closeModal()
    modal.getModal().should('not.be.visible')
  })

  it('Should show a download acknowledgment message from env variable', () => {
    modal.openModal('Save account data')
    cy.env(['VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT']).then(
      ({ VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT }) => {
        modal
          .getModal()
          .should('be.visible')
          .within(() => {
            cy.findByTestId('download-acknowledgment-text').should(
              'include.text',
              stripHtmlTags(VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT as string)
            )
          })
      }
    )
  })

  it('Should not allow downloading unless privacy notice is accepted', () => {
    modal.openModal('Save account data')
    modal.verifyPrivacyCheckboxRequired()
  })
  it('Should reset options when closed', () => {
    /**
     * When the account download modal is closed, its form elements
     * should be reset to initial state:
     *   - PII acknowledgment checkbox should be unchecked
     *   - 'Exclude' option should be selected in contact info radio buttons
     */

    const includeContactInfoLabel =
      'Include latest contact information for account holder'
    const excludeContactInfoLabel =
      'Do not include account holder contact information'

    // PII acknowledgment checkbox and include contact info radio
    // should be unchecked by default when the Account modal is opened
    modal.openModal('Save account data').within(() => {
      getInputByLabel(excludeContactInfoLabel).should('be.checked')
      getInputByLabel(includeContactInfoLabel).should('not.be.checked')
      modal.getPIICheckbox().should('not.be.checked')

      // Clicking PII acknowledgment checkbox and include contact info radio
      // should update their checked state
      cy.get('label').contains(includeContactInfoLabel).click()
      modal.checkPIICheckbox()
      getInputByLabel(excludeContactInfoLabel).should('not.be.checked')
      getInputByLabel(includeContactInfoLabel).should('be.checked')
      modal.getPIICheckbox().should('be.checked')
    })

    // Closing the modal should reset the PII acknowledgment checkbox
    // and 'include contact info' radio to their default unchecked state
    modal.closeModal()
    modal.openModal('Save account data').within(() => {
      getInputByLabel(includeContactInfoLabel).should('not.be.checked')
      getInputByLabel(excludeContactInfoLabel).should('be.checked')
      modal.getPIICheckbox().should('not.be.checked')
    })
  })
})

/**
 * Table sorting
 *
 * 1. When account page is loaded without a sort param in the URL,
 *      URL & table sort should be updated to reflect default sort (activity_date ascending)
 * 2. Clicking another column's sort indicator three times should update sort state,
 *      cycling through ascending sort, descending sort, and then sort removal / return to default sort
 * 3. Clicking one column's sort indicator and then shift-clicking the sort indicator in an
 *      additional column should update row order and URL to include the additional sort param
 * 4. Navigating to page with sort state in URL should apply that state
 * 
 *
 * Excerpt of fields for the four records in the account data fixture
 * 
 *  [
      {
        activity_date: '2018-07-30',
        actual_pmt_amt: 50,
        current_bal: 300
      },
      {
        activity_date: '2018-08-30',
        actual_pmt_amt: 100,
        current_bal: 1000
      },
      {
        activity_date: '2018-09-30',
        actual_pmt_amt: 50,
        current_bal: 500
      },
      {
        activity_date: '2018-10-30',
        actual_pmt_amt: 50,
        current_bal: 1000
      }
    ]
 */

describe('Account page sorting', () => {
  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', 'api/events/1/account/111111/', {
      fixture: 'account_1'
    }).as('getAccount')
    cy.visit('/events/1/accounts/111111')
    cy.wait(['@getEvent', '@getAccount'])
  })

  it('Should default to sorting by activity_date when there is no sort param in URL', () => {
    // A sort param of activity_date is added to the URL
    cy.location('search').should('include', 'sort=activity_date')

    // The activity date column should show the sort ascending icon,
    // and all other columns should show the unsorted icon
    table.shouldShowSortIcon('activity_date', 'ascending')
    table.otherColumnsShouldBeUnsorted('activity_date')

    // The data in the table should be sorted by activity_date ascending
    table.verifyColumnContent('activity_date', [
      '2018-07-30',
      '2018-08-30',
      '2018-09-30',
      '2018-10-30'
    ])
    table.verifyColumnContent('current_bal', [300, 1000, 500, 1000])
  })

  it('Should update sort state when a column sort button is clicked repeatedly', () => {
    // URL and table show sorting by default column activity_date
    // when page is loaded without sort param
    cy.location('search').should('include', 'sort=activity_date')
    table.shouldShowSortIcon('activity_date', 'ascending')
    table.otherColumnsShouldBeUnsorted('activity_date')
    table.verifyColumnContent('activity_date', [
      '2018-07-30',
      '2018-08-30',
      '2018-09-30',
      '2018-010-30'
    ])
    table.verifyColumnContent('current_bal', [300, 1000, 500, 1000])

    // Click the sort icon in the current balance column
    table.clickSortButton('current_bal')

    // Table and URL should be updated to show sorting by current balance
    cy.location('search').should('include', 'sort=current_bal')
    table.shouldShowSortIcon('current_bal', 'ascending')
    table.shouldShowUnsortedIcon('activity_date')
    table.verifyColumnContent('current_bal', [300, 500, 1000, 1000])
    table.verifyColumnContent('activity_date', [
      '2018-07-30',
      '2018-09-30',
      '2018-08-30',
      '2018-10-30'
    ])

    // Click the current balance sort button again to sort descending
    table.clickSortButton('current_bal')

    // Table and URL should be updated to show sorting by current balance
    cy.location('search').should('include', 'sort=-current_bal')
    table.shouldShowSortIcon('current_bal', 'descending')
    table.shouldShowUnsortedIcon('activity_date')
    table.verifyColumnContent('current_bal', [1000, 1000, 500, 300])
    table.verifyColumnContent('activity_date', [
      '2018-08-30',
      '2018-10-30',
      '2018-09-30',
      '2018-07-30'
    ])

    // Clicking the current balance sort button a third time removes
    // the current balance sorting and restores default sort
    table.clickSortButton('current_bal')

    cy.location('search').should('include', 'sort=activity_date')
    table.shouldShowSortIcon('activity_date', 'ascending')
    table.shouldShowUnsortedIcon('current_bal')
    table.verifyColumnContent('activity_date', [
      '2018-07-30',
      '2018-08-30',
      '2018-09-30',
      '2018-010-30'
    ])
    table.verifyColumnContent('current_bal', [300, 1000, 500, 1000])
  })

  it('Should multisort', () => {
    // URL and table show sorting by default column activity_date
    cy.location('search').should('include', 'sort=activity_date')
    table.shouldShowSortIcon('activity_date', 'ascending')
    table.otherColumnsShouldBeUnsorted('activity_date')
    table.verifyColumnContent('activity_date', [
      '2018-07-30',
      '2018-08-30',
      '2018-09-30',
      '2018-010-30'
    ])
    table.verifyColumnContent('current_bal', [300, 1000, 500, 1000])

    // Click the sort icon in the current balance column
    table.clickSortButton('current_bal')

    // Table and URL should be updated to show sorting by current balance
    cy.location('search').should('include', 'sort=current_bal')
    table.shouldShowSortIcon('current_bal', 'ascending')
    table.shouldShowUnsortedIcon('activity_date')
    table.verifyColumnContent('current_bal', [300, 500, 1000, 1000])
    table.verifyColumnContent('activity_date', [
      '2018-07-30',
      '2018-09-30',
      '2018-08-30',
      '2018-10-30'
    ])

    // Shift-click the actual payment amount sort button with
    table.clickSortButtonWithShift('actual_pmt_amt')

    // Table and URL should be updated to show sorting by both
    // current balance and actual payment amount
    cy.location('search').should('include', 'sort=current_bal,actual_pmt_amt')

    table.shouldShowUnsortedIcon('activity_date')
    table.shouldShowSortIcon('current_bal', 'ascending')
    table.shouldShowSortOrder('current_bal', 1)
    table.shouldShowSortIcon('actual_pmt_amt', 'ascending')
    table.shouldShowSortOrder('actual_pmt_amt', 2)

    table.verifyColumnContent('current_bal', [300, 500, 1000, 1000])
    table.verifyColumnContent('actual_pmt_amt', [50, 50, 50, 100])
    table.verifyColumnContent('activity_date', [
      '2018-07-30',
      '2018-09-30',
      '2018-10-30',
      '2018-08-30'
    ])
  })
})

describe('Sorting is applied from query params', () => {
  it('Should apply sort state from url', () => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', 'api/events/1/account/11111/', {
      fixture: 'account_1'
    }).as('getAccount')
    cy.visit(`/events/1/accounts/11111/?sort=current_bal`)
    cy.wait(['@getEvent', '@getAccount'])

    // only current_bal column shows sorted icon
    table.shouldShowSortIcon('current_bal', 'ascending')
    table.otherColumnsShouldBeUnsorted('current_bal')

    // current_bal column data is sorted ascending, and other columns are unsorted
    table.verifyColumnContent('current_bal', [300, 500, 1000, 1000])
    table.verifyColumnContent('activity_date', [
      '2018-07-30',
      '2018-09-30',
      '2018-08-30',
      '2018-10-30'
    ])
  })
})

describe('Querystring validation', () => {
  beforeEach(() => {
    cy.viewport(1920, 1080)
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', 'api/events/1/account/111111/', {
      fixture: 'account_1'
    }).as('getAccount')
  })

  describe('Should accept valid sort params', () => {
    // It takes a while to check all the fields, so
    // get a few random values to check from account table fields.
    const validFields = accountTableFields
      .toSorted(() => 0.5 - Math.random())
      .slice(0, 5)
    for (const field of validFields) {
      it(`Should accept "${field}" as sort param`, () => {
        cy.visit(`/events/1/accounts/111111/?sort=${field}`)
        cy.wait(['@getEvent', '@getAccount'])
        cy.location('search').should('include', `sort=${field}`)
        table.shouldShowSortIcon(field, 'ascending')

        cy.visit(`/events/1/accounts/111111/?sort=-${field}`)
        cy.wait(['@getEvent', '@getAccount'])
        cy.location('search').should('include', `sort=-${field}`)
        table.shouldShowSortIcon(field, 'descending')
      })
    }
  })

  describe('Should replace invalid sort params', () => {
    const invalidValues = ['', 'random_value']
    for (const val of invalidValues) {
      it(`Should replace invalid sort param "${val}" with default`, () => {
        cy.visit(`/events/1/accounts/111111/?sort=${val}`)
        cy.wait(['@getEvent', '@getAccount'])
        cy.location('search').should('include', 'sort=activity_date')
      })
    }
  })
})
