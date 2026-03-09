import { getDisplayValue } from './displayValueHelper'

export class Metro2Table {
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
}
