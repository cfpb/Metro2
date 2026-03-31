import { EvaluatorPage } from '../helpers/evaluatorPageHelpers'

// Instantiate helpers
const page = new EvaluatorPage()

// TODO: standardize icon checks to handle content clipping

describe('Sorting evaluator results table', () => {
  it('Should show default sorting when there are no sort params in URL', () => {
    // Navigate to the evaluator page all results tab
    page.loadEvaluatorPage({ view: 'all' })

    // sort=activity_date is added to URL
    cy.location('search').should('include', 'sort=activity_date')

    // Activity date column shows ascending sort icon
    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-ascending-icon')
      .should('be.visible')
      .and('not.have.class', 'ag-hidden')
    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-descending-icon')
      .should('not.be.visible')
      .and('have.class', 'ag-hidden')
    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-indicator-icon.ag-sort-none-icon')
      .should('not.be.visible')
      .and('have.class', 'ag-hidden')

    // Other columns show 'no sort' icon
    cy.get('.ag-header-cell:not([col-id="activity_date"])').each(cell => {
      cy.wrap(cell)
        .find('.ag-sort-ascending-icon')
        .should('not.be.visible')
        .and('have.class', 'ag-hidden')
      cy.wrap(cell)
        .find('.ag-sort-descending-icon')
        .should('not.be.visible')
        .and('have.class', 'ag-hidden')
      cy.wrap(cell)
        .find('.ag-sort-indicator-icon.ag-sort-none-icon')
        .should('not.have.class', 'ag-hidden')
    })
  })

  it('Should update sort direction and fetch new data when sort button clicked', () => {
    // Navigate to the evaluator page all results tab
    page.loadEvaluatorPage({ view: 'all' })

    // sort=activity_date is added to URL
    cy.location('search').should('include', 'sort=activity_date')

    // Activity date column shows ascending sort icon
    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-ascending-icon')
      .should('be.visible')
      .and('not.have.class', 'ag-hidden')

    // Clicking another column should change the sort to that column
    // and request new data

    // Intercept requests for results with sort params
    page.interceptFilteredResults(
      'sccAscending',
      { view: 'all', sort: ['spc_com_cd'] },
      'evaluatorHits_page1'
    )
    page.interceptFilteredResults(
      'sccDescending',
      { view: 'all', sort: ['-spc_com_cd'] },
      'evaluatorHits_page2'
    )

    // Click the spc_com_cd sort button and verify
    // that new page data is loaded and scc header shows sort
    cy.get('.ag-header-cell[col-id="spc_com_cd"]')
      .find('.ag-sort-indicator-container')
      .click()

    cy.wait(['@sccAscending'])

    cy.location('search').should('include', 'sort=spc_com_cd')

    cy.get('.ag-header-cell[col-id="spc_com_cd"]')
      .find('.ag-sort-ascending-icon')
      .should('be.visible')

    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-ascending-icon')
      .should('not.be.visible')

    // Click the button again and descending sort should be applied
    cy.get('.ag-header-cell[col-id="spc_com_cd"]')
      .find('.ag-sort-indicator-container')
      .click()

    cy.wait(['@sccDescending'])

    cy.location('search').should('include', 'sort=-spc_com_cd')

    cy.get('.ag-header-cell[col-id="spc_com_cd"]')
      .find('.ag-sort-descending-icon')
      .should('be.visible')

    // Click the button a third time and default sort should be back
    cy.get('.ag-header-cell[col-id="spc_com_cd"]')
      .find('.ag-sort-indicator-container')
      .click()

    // Data is fetched from cache, so no request
    cy.location('search').should('include', 'sort=activity_date')

    cy.get('.ag-header-cell[col-id="spc_com_cd"]')
      .find('.ag-sort-descending-icon')
      .should('have.class', 'ag-hidden')

    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-ascending-icon')
      .should('not.have.class', 'ag-hidden')
  })

  it('Should reset sort when sample results tab clicked', () => {
    // Navigate to the evaluator page all results tab
    page.loadEvaluatorPage({ view: 'all' })

    // sort=activity_date is added to URL
    cy.location('search').should('include', 'sort=activity_date')

    // Activity date column shows ascending sort icon
    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-ascending-icon')
      .should('be.visible')
      .and('not.have.class', 'ag-hidden')

    // Clicking that column should update sort direction
    // and request new data

    // Intercept requests for results with sort params
    page.interceptFilteredResults(
      'activityDateDescending',
      { view: 'all', sort: ['-activity_date'] },
      'evaluatorHits_page1'
    )
    page.interceptFilteredResults(
      'sampleView',
      { view: 'sample' },
      'evaluatorHits_page2'
    )

    // Click to sort activity date descending
    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-indicator-container')
      .click()

    cy.wait(['@activityDateDescending'])

    cy.location('search').should('include', 'sort=-activity_date')

    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-descending-icon')
      .should('be.visible')
      .and('not.have.class', 'ag-hidden')

    //Click sample results tab button
    cy.findByTestId('sample-results-tab').click({ force: true })

    cy.wait(['@sampleView'])

    cy.location('search')
      .should('include', 'sort=activity_date')
      .and('include', 'view=sample')

    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-ascending-icon')
      .should('be.visible')
      .and('not.have.class', 'ag-hidden')
  })

  it('Should allow multisort', () => {
    // Navigate to the evaluator page all results tab
    page.loadEvaluatorPage({ view: 'all' })

    // sort=activity_date is added to URL
    cy.location('search').should('include', 'sort=activity_date')

    // Activity date column shows ascending sort icon
    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-ascending-icon')
      .should('be.visible')
      .and('not.have.class', 'ag-hidden')

    // Clicking another column while holding the shift key
    // should multisort

    // Intercept requests for results with multisort params
    page.interceptFilteredResults(
      'multisort',
      { view: 'all', sort: ['activity_date', 'current_bal'] },
      'evaluatorHits_page1'
    )

    cy.get('.ag-header-cell[col-id="current_bal"]')
      .find('.ag-sort-indicator-container')
      .click({ shiftKey: true })

    cy.wait(['@multisort'])

    cy.location('search').should('include', 'sort=activity_date,current_bal')

    cy.get('.ag-header-cell[col-id="current_bal"]')
      .find('.ag-sort-ascending-icon')
      .should('be.visible')
    cy.get('.ag-header-cell[col-id="current_bal"]')
      .find('.ag-sort-order')
      .should('be.visible')
      .and('have.text', '2')

    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-ascending-icon')
      .should('be.visible')

    cy.get('.ag-header-cell[col-id="activity_date"]')
      .find('.ag-sort-order')
      .should('be.visible')
      .and('have.text', '1')
  })
})
