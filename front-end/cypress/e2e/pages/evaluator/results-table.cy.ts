import { Metro2Table } from '@cypress/helpers/tableHelpers'
import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { PII_COOKIE_NAME } from '@src/constants/settings'
import getTableFields from '@src/pages/Evaluator/results/utils/getTableFields'
import AccountRecord from '@src/types/AccountRecord'
import EvaluatorMetadata from '@src/types/EvaluatorMetadata'

const table = new Metro2Table()

describe('Results table', () => {
  it('Should show correct content in the results table', () => {
    // Request the data for the first event from the API
    cy.request('api/events/1/').then(response => {
      // Get the first evaluator from the event's results
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      const evaluator = response.body?.evaluators[0] as EvaluatorMetadata

      // Load the results view for the selected evaluator
      cy.viewport(1920, 1800)
      cy.setCookie(PII_COOKIE_NAME, 'true')
      cy.visit(`/events/1/evaluators/${evaluator.id}`)

      // Wait for the evaluator results table to load
      cy.get('.ag-row-first').should('be.visible')

      // Verify that the expected field names are displayed in the table column headers
      const expectedHeaders = [
        ...new Set([
          'Account number',
          'Activity date',
          ...evaluator.fields_used.map(field => M2_FIELD_NAMES.get(field)),
          ...M2_FIELD_NAMES.values()
        ])
      ]
      table.verifyHeaders(expectedHeaders)

      // Request the hits for this evaluator so we can verify the table contents
      cy.request(`api/events/1/evaluator/${evaluator.id}/?view=sample`).then(
        response => {
          // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
          const hits = response.body?.hits as AccountRecord[]

          // Get the list of fields that should appear in this table
          const fields = getTableFields(evaluator.fields_used)

          // Remove cons_acct_num from the list of fields to check
          // because it's in a separate table for the pinned left column.
          fields.shift()

          // Verify that the values for the expected fields are displayed
          // in the main table section.
          table.verifyTableBodyContent<AccountRecord>(
            table.getBodyRows(),
            fields,
            hits
          )

          // Verify that the consumer account numbers are displayed
          // in the pinned left column.
          table.verifyTableBodyContent<AccountRecord>(
            table.getPinnedRows(),
            ['cons_acct_num'],
            hits
          )
        }
      )
    })
  })
})
