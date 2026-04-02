import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { expect } from 'chai'

import { EvaluatorPage } from '../helpers/evaluatorPageHelpers'

const evalPage = new EvaluatorPage()

describe('API accepts account fields as sort params on evaluator view', () => {
  const sortableFields = [...M2_FIELD_NAMES.keys()]
  for (const field of sortableFields) {
    it(`Should accept ${field} as sort param on evaluator view`, () => {
      const query = evalPage.apiExt({ view: 'all', sort: [field] })
      cy.request('GET', `/api/events/1/evaluator/Portfolio-Type-1/${query}`).then(
        response => {
          expect(response.status).to.eq(200)
        }
      )
    })
  }
})
