import { EvaluatorPage } from '@cypress/helpers/evaluatorPageHelpers'
import { Metro2Table } from '@cypress/helpers/tableHelpers'
// Instantiate helpers
const page = new EvaluatorPage()
const table = new Metro2Table()

describe('Sorting evaluator results table', () => {
  it('Should show default sorting when there are no sort params in URL', () => {
    // Navigate to the evaluator page all results tab
    page.loadEvaluatorPage({ view: 'all' })

    // sort=activity_date is added to URL
    cy.location('search').should('include', 'sort=activity_date')

    // Activity date column shows ascending sort icon
    table.shouldShowSortIcon('activity_date', 'ascending')

    // Other columns show 'no sort' icon
    table.otherColumnsShouldBeUnsorted('activity_date')
  })

  it('Should update sort direction and fetch new data when sort button clicked', () => {
    // Navigate to the evaluator page all results tab
    page.loadEvaluatorPage({ view: 'all' })

    // sort=activity_date is added to URL
    cy.location('search').should('include', 'sort=activity_date')

    // Activity date column shows ascending sort icon
    table.shouldShowSortIcon('activity_date', 'ascending')

    // Intercept requests
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

    // Clicking the spc_com_cd sort button applies ascending sort
    // to the spc_com_cd column and removes sort from activity_date
    table.clickSortButton('spc_com_cd')

    cy.wait(['@sccAscending'])

    cy.location('search').should('include', 'sort=spc_com_cd')

    table.shouldShowSortIcon('spc_com_cd', 'ascending')
    table.shouldShowUnsortedIcon('activity_date')

    // Clicking the spc_com_cd button again applies descending sort
    // to that column
    table.clickSortButton('spc_com_cd')

    cy.wait(['@sccDescending'])

    cy.location('search').should('include', 'sort=-spc_com_cd')

    table.shouldShowSortIcon('spc_com_cd', 'descending')

    // Clicking the button a third time removes sort from spc_com_cd
    // and reapplies default sort to activity_date column
    table.clickSortButton('spc_com_cd')

    // Data is fetched from cache, so no request
    cy.location('search').should('include', 'sort=activity_date')

    table.shouldShowSortIcon('activity_date', 'ascending')

    table.shouldShowUnsortedIcon('spc_com_cd')
  })

  it('Should allow multisort', () => {
    // Navigate to the evaluator page all results tab
    page.loadEvaluatorPage({ view: 'all' })

    // sort=activity_date is added to URL
    cy.location('search').should('include', 'sort=activity_date')

    // Activity date column shows ascending sort icon
    table.shouldShowSortIcon('activity_date', 'ascending')

    // Intercept requests for results with multisort params
    page.interceptFilteredResults(
      'multisort',
      { view: 'all', sort: ['activity_date', 'current_bal'] },
      'evaluatorHits_page1'
    )

    // Clicking another column while holding the shift key
    // should multisort
    table.clickSortButtonWithShift('current_bal')

    cy.wait(['@multisort'])

    cy.location('search').should('include', 'sort=activity_date,current_bal')

    table.shouldShowSortIcon('activity_date', 'ascending')
    table.shouldShowSortOrder('activity_date', 1)

    table.shouldShowSortIcon('current_bal', 'ascending')
    table.shouldShowSortOrder('current_bal', 2)
  })

  it('Should reset sort when sample results tab clicked', () => {
    // Navigate to the evaluator page all results tab
    page.loadEvaluatorPage({ view: 'all' })

    // sort=activity_date is added to URL
    cy.location('search').should('include', 'sort=activity_date')

    // Only activity date column is sorted
    table.shouldShowSortIcon('activity_date', 'ascending')
    table.shouldNotShowSortOrder('activity_date')

    // Intercept requests
    page.interceptFilteredResults(
      'multisort',
      { view: 'all', sort: ['activity_date', 'current_bal'] },
      'evaluatorHits_page1'
    )
    page.interceptFilteredResults(
      'sampleView',
      { view: 'sample' },
      'evaluatorHits_16'
    )

    // Clicking the current_bal column sort button should multisort
    table.clickSortButtonWithShift('current_bal')

    cy.wait(['@multisort'])

    cy.location('search').should('include', 'sort=activity_date,current_bal')

    table.shouldShowSortIcon('current_bal', 'ascending')
    table.shouldShowSortOrder('current_bal', 2)

    table.shouldShowSortIcon('activity_date', 'ascending')
    table.shouldShowSortOrder('activity_date', 1)

    // Clicking sample results tab button should reset to default sort
    cy.findByTestId('sample-results-tab').click({ force: true })

    cy.wait(['@sampleView'])

    // URL should reflect sample view and default sort
    cy.location('search')
      .should('include', 'sort=activity_date')
      .and('include', 'view=sample')

    // Ascending sort icon should show in activity_date column
    table.shouldShowSortIcon('activity_date', 'ascending')

    // but all other columns should show the unsorted icon
    table.otherColumnsShouldBeUnsorted('activity_date')

    // and neither activity_date nor current_bal should show sort order
    table.shouldNotShowSortOrder('activity_date')
    table.shouldNotShowSortOrder('current_bal')
  })
})
