/* eslint-disable cypress/require-data-selectors */
import { AccountRecord } from 'utils/constants'
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

  verifyHeaders(expectedHeaderValues: string[]) {
    // Verify that text of header cells in table matches array of expected values
    this.getHeaderCells().each((cell, cellIndex) => {
      cy.wrap(cell).should('have.text', expectedHeaderValues[cellIndex])
    })
  }

  // given a group of table rows -- accessed via getPinnedRows or getBodyRows methods --
  // a list of fields that should appear in the rows,
  // and an array of account records that map to the rows,
  // verify that each row displays the expected fields' values for its record
  verifyAccountTableBodyContent(
    rows: Cypress.Chainable<JQuery>,
    fields: string[],
    expectedData: AccountRecord[]
  ) {
    rows.each((row, rowIndex) => {
      // get the record for this row
      const rowData = expectedData[rowIndex]
      row.find('.ag-cell-value').each((cellIndex, cell) => {
        // get the field that corresponds with this cell
        const field = fields[cellIndex]
        // get the value that should be displayed in this cell.
        // depending on the field type,
        // this could be a formatted date, a USD formatted number,
        // a string with parenthetical annotation,
        // or the raw value from the record.
        const expectedValue = getDisplayValue(field, rowData[field])
        cy.wrap(cell).should('have.text', expectedValue ?? '')
      })
    })
  }
}
