import { FilterHelpers } from '@cypress/helpers/filterHelpers'
import { Metro2Page } from '@cypress/helpers/pageHelper'
import { PII_COOKIE_NAME } from '@src/constants/settings'
// Instantiate helpers
const page = new Metro2Page()
const filters = new FilterHelpers()

describe('Filter counts', () => {
  it('Should not show counts when there are more than 1M results', () => {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')

    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')
    cy.intercept(
      'GET',
      `/api/events/1/evaluator/Test-Eval-1/?page=1&page_size=20&sort=activity_date&view=all`,
      {
        fixture: 'evaluatorHits_1000000'
      }
    ).as('getEvaluatorHits')

    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/facets/`, {
      fixture: 'facets'
    }).as('counts')

    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-1/facets/?acct_stat=11`, {
      fixture: 'facets_filtered'
    }).as('filteredCounts')

    cy.visit(`/events/1/evaluators/Test-Eval-1/?view=all`)

    cy.wait(['@getEvent', '@getUser', '@getEvaluatorHits'])
    // API requests for counts should not have been made
    cy.get('@counts.all').should('have.length', 0)
    cy.get('@filteredCounts.all').should('have.length', 0)

    // No counts content should be visible
    cy.get('.label-with-count').should('not.exist')

    // A message should be displayed
    cy.findByTestId('counts-message')
      .should('be.visible')
      .and(
        'have.text',
        'Filter counts are not available for evaluators with over a million results.'
      )
  })

  it('Should not show counts if API request for counts fails', () => {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')

    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept(
      'GET',
      `/api/events/1/evaluator/Test-Eval-2/?page=1&page_size=20&sort=activity_date&view=all`,
      {
        fixture: 'evaluatorHits_page1'
      }
    ).as('getEvaluatorHits')

    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-2/facets/`, {
      delay: 500,
      statusCode: 504
    }).as('counts')

    cy.visit(`/events/1/evaluators/Test-Eval-2/?view=all`)

    cy.wait(['@getEvent', '@getEvaluatorHits'])

    // Loader should be visible
    cy.findByTestId('filter-loader').should('be.visible')

    // wait for request to fail
    cy.wait(1000)

    // Loader should not be visible
    cy.findByTestId('filter-loader').should('not.exist')

    // No counts content should be visible
    cy.get('.label-with-count').should('not.exist')

    // A message should be displayed
    cy.findByTestId('counts-message')
      .should('be.visible')
      .and('include.text', 'Filter counts are not currently available.')
  })

  it('Should allow user to cancel requests for counts and see basic filters', () => {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')

    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept(
      'GET',
      `/api/events/1/evaluator/Test-Eval-2/?page=1&page_size=20&sort=activity_date&view=all`,
      {
        fixture: 'evaluatorHits_page1'
      }
    ).as('getEvaluatorHits')

    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-2/facets/`, {
      delay: 2000
    }).as('counts')

    cy.visit(`/events/1/evaluators/Test-Eval-2/?view=all`)

    cy.wait(['@getEvent', '@getEvaluatorHits'])

    // Filters should not be in page
    cy.findByTestId('evaluator-filter-container').should('not.exist')

    // Loader should be visible
    cy.findByTestId('filter-loader').should('be.visible')

    // Click button to cancel requests for counts
    cy.findByTestId('cancel-counts').should('be.visible').click()

    // Loader should not be visible
    cy.findByTestId('filter-loader').should('not.exist')

    // Filter section should be visible
    cy.findByTestId('evaluator-filter-container').should('be.visible')

    // No counts content should be visible
    cy.get('.label-with-count').should('not.exist')
  })

  it('Should show counts', () => {
    cy.viewport(1920, 1800)
    cy.setCookie(PII_COOKIE_NAME, 'true')

    cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
    cy.intercept(
      'GET',
      `/api/events/1/evaluator/Test-Eval-2/?page=1&page_size=20&sort=activity_date&view=all`,
      {
        fixture: 'evaluatorHits_page1'
      }
    ).as('getEvaluatorHits')

    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-2/facets/`, {
      fixture: 'facets',
      delay: 1000
    }).as('counts')

    cy.intercept('GET', `/api/events/1/evaluator/Test-Eval-2/facets/?acct_stat=11`, {
      fixture: 'facets_filtered',
      delay: 1000
    }).as('filteredCounts')

    cy.visit(`/events/1/evaluators/Test-Eval-2/?view=all`)

    cy.wait(['@getEvent', '@getEvaluatorHits'])

    // Loader should be displayed
    cy.findByTestId('filter-loader').should('be.visible')

    // API request for initial counts should be made
    cy.wait(['@counts'])
    // but not the request for filtered counts
    cy.get('@filteredCounts.all').should('have.length', 0)

    // Loader should not be visible any more
    cy.findByTestId('filter-loader').should('not.exist')

    // Counts should exist
    cy.get('.label-with-count').should('exist')

    // Fields without children with counts should be disabled
    const fieldsWithoutCounts = [
      'compl_cond_cd',
      'pmt_rating',
      'terms_freq',
      'cons_info_ind',
      'l1__change_ind'
    ]
    filters.expectAccordionsAreDisabled(fieldsWithoutCounts)

    const fieldsWithCounts = ['acct_stat', 'spc_com_cd', 'php1']
    filters.expectAccordionsAreActive(fieldsWithCounts)

    // Check that the expected groups are active / inactive in Account status
    const statusGroupsWithoutCounts = [
      'acct_stat_Paid_or_settled_in_full',
      'acct_stat_Paid_or_settled_in_full',
      'acct_stat_Foreclosure_or_default',
      'acct_stat_Repossession_or_surrender',
      'acct_stat_Deleted'
    ]
    filters.expectAccordionsAreDisabled(statusGroupsWithoutCounts)
    const statusGroupsWithCounts = ['acct_stat_Current', 'acct_stat_Delinquent']
    filters.expectAccordionsAreActive(statusGroupsWithCounts)

    // Check that Current / Delinquent have correct counts
    cy.get('#acct_stat_Current-label').find('.count').should('have.text', '2,500')
    cy.get('#acct_stat_Delinquent-label').find('.count').should('have.text', '500')

    // Check that the expected checkboxes are active / inactive in Delinquent
    filters.expectCheckboxesAreDisabled([
      'acct_stat_80',
      'acct_stat_82',
      'acct_stat_83',
      'acct_stat_84',
      'acct_stat_93',
      'acct_stat_97'
    ])
    filters.expectCheckboxesAreActive(['acct_stat_71', 'acct_stat_78'])
    cy.get('#acct_stat_71-label').find('.count').should('have.text', '250')
    cy.get('#acct_stat_78-label').find('.count').should('have.text', '250')

    filters.getAccordionTarget('acct_stat').click()
    page.getExpandableByText('Account status').within(() => {
      cy.get('#acct_stat_Current-label').click()
    })

    // Active / inactive state should be the same,
    // but counts should be updated
    filters.expectAccordionsAreDisabled(fieldsWithoutCounts)
    filters.expectAccordionsAreActive(fieldsWithCounts)
    filters.expectAccordionsAreDisabled(statusGroupsWithoutCounts)
    filters.expectAccordionsAreActive(statusGroupsWithCounts)

    // Check that Current has correct counts
    cy.get('#acct_stat_Current-label').find('.count').should('have.text', '2,500')

    // And Delinquent has no count
    cy.get('#acct_stat_Delinquent-label').find('.count').should('have.text', '')

    // Check that the expected checkboxes are active / inactive in Delinquent
    filters.expectCheckboxesAreDisabled([
      'acct_stat_80',
      'acct_stat_82',
      'acct_stat_83',
      'acct_stat_84',
      'acct_stat_93',
      'acct_stat_97'
    ])
    filters.expectCheckboxesAreActive(['acct_stat_71', 'acct_stat_78'])

    // Active delinquent checkboxes should not show counts
    cy.get('#acct_stat_71-label').find('.count').should('not.exist')
    cy.get('#acct_stat_78-label').find('.count').should('not.exist')
  })
})
