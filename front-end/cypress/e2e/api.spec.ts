/* eslint-disable unicorn/prefer-set-has */
import { M2_FIELD_NAMES } from 'utils/constants'

describe('API', () => {
  it('Should return only the expected fields for an account record', () => {
    // TODO: may want to check evaluator results and / or more accounts
    cy.request('GET', '/api/events/1/account/20160907019898/').then(response => {
      expect(response.status).to.eq(200)
      // Get a list of all the Metro2 account record fields we expect in the front end code
      const expectedFields = [...M2_FIELD_NAMES.keys()]
      // Get a list of all the fields returned on this account's records
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
      const sampleRecord = response.body.account_activity[0]
      // filter out fields we expect but aren't part of a Metro 2 account record
      // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
      const fields = Object.keys(sampleRecord).filter(
        field => !['id', 'inconsistencies'].includes(field)
      )
      // Verify that there aren't any unexpected fields in the records returned for this account
      expect(fields.every(field => expectedFields.includes(field))).to.be.true
    })
  })
})
