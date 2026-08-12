import { getDisplayValue } from './displayValueHelper'

export class Metro2Table {
  getTable() {
    return cy.findByTestId('data-grid-container')
  }

  getHeaderCells() {
    return cy.get('.ag-header-cell-text')
  }

  getPinnedRows() {
    return cy.get(`.ag-pinned-left-cols-container div[role="row"]`)
  }

  getBodyRows() {
    return cy.get(`.ag-center-cols-container div[role="row"]`)
  }

  hasRowCount(count: number) {
    this.getBodyRows().should('have.length', count)
  }

  verifyHeaders(expectedHeaderValues: string[]) {
    // Verify that text of header cells in table matches array of expected values
    this.getHeaderCells().each((cell, cellIndex) => {
      cy.wrap(cell).should('have.text', expectedHeaderValues[cellIndex])
    })
  }

  verifyTableBodyContent<Type>(
    rows: Cypress.Chainable<JQuery>,
    fields: string[],
    expectedData: Type[]
  ) {
    rows.each((row, rowIndex) => {
      // Get the object that corresponds with this row
      // from the expected data array
      const expectedRowData = expectedData[rowIndex]

      // Check the content of each cell in the row against the
      // value at the corresponding index in the row's expected data object.
      // Because the fixture data matches what would be returned from the API
      // and the values for many fields are formatted before they're displayed in tables,
      // we check to see if we need to apply formatting before comparing the
      // table value against the fixture value.
      row.find('.ag-cell-value').each((cellIndex, cell) => {
        const field = fields[cellIndex]
        const expectedValue = expectedRowData[field as keyof Type]
        const formattedValue = getDisplayValue(field, expectedValue)
        cy.wrap(cell).should('have.text', formattedValue)
      })
    })
  }

  verifyColumnContent(field: string, values: (string | number)[]) {
    cy.get(`.ag-cell[col-id="${field}"]`).each((cell, cellIndex) => {
      const expectedValue = values[cellIndex]
      const formattedValue = getDisplayValue(field, expectedValue)
      cy.wrap(cell).should('have.text', formattedValue)
    })
  }

  shouldShowSortIcon(field: string, direction: 'ascending' | 'descending') {
    return cy
      .get(`.ag-header-cell[col-id="${field}"]`)
      .find(`.ag-sort-${direction}-icon`)
      .should('not.have.class', 'ag-hidden')
  }

  shouldShowUnsortedIcon(field: string) {
    return cy
      .get(`.ag-header-cell[col-id="${field}"]`)
      .find('.ag-sort-indicator-icon.ag-sort-none-icon')
      .should('not.have.class', 'ag-hidden')
  }

  shouldNotShowSortOrder(field: string) {
    cy.get(`.ag-header-cell[col-id="${field}"]`)
      .find('.ag-sort-order')
      .should('have.class', 'ag-hidden')
  }

  shouldShowSortOrder(field: string, order: number) {
    cy.get(`.ag-header-cell[col-id="${field}"]`)
      .find('.ag-sort-order')
      .should('not.have.class', 'ag-hidden')
      .and('have.text', order)
  }

  otherColumnsShouldBeUnsorted(field: string) {
    cy.get(`.ag-header-cell:not([col-id="${field}"])`).each(cell => {
      cy.wrap(cell).find('.ag-sort-ascending-icon').and('have.class', 'ag-hidden')
      cy.wrap(cell).find('.ag-sort-descending-icon').and('have.class', 'ag-hidden')
      cy.wrap(cell).find('.ag-sort-order').should('have.class', 'ag-hidden')
      cy.wrap(cell)
        .find('.ag-sort-indicator-icon.ag-sort-none-icon')
        .should('not.have.class', 'ag-hidden')
    })
  }

  clickSortButton(field: string) {
    cy.get(`.ag-header-cell[col-id="${field}"]`)
      .find('.ag-sort-indicator-container')
      .click({ shiftKey: false })
  }

  clickSortButtonWithShift(field: string) {
    cy.get(`.ag-header-cell[col-id="${field}"]`)
      .find('.ag-sort-indicator-container')
      .click({ shiftKey: true })
  }
}
