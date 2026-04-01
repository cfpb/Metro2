/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { expect } from 'chai'

import { EvaluatorPage } from '../helpers/evaluatorPageHelpers'

const evalPage = new EvaluatorPage()

describe('API', () => {
  it('Should accept all account fields as sort params on evaluator view', () => {
    const sortableFields = [...M2_FIELD_NAMES.keys()]
    for (const field of sortableFields) {
      const query = evalPage.apiExt({view: 'all', sort:[field]})
      cy.request('GET', `/api/events/1/evaluator/Portfolio-Type-1/${query}`).then(response => {
        expect(response.status).to.eq(200)
      })
    }
  })
})
