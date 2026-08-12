import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import Event from '@src/types/Event'
import { expect } from 'chai'

import { EvaluatorPage } from '@cypress/helpers/evaluatorPageHelpers'

const evalPage = new EvaluatorPage()
let evaluatorName: string | undefined = 'Portfolio-Type-1'

describe('API accepts account fields as sort params on evaluator view', () => {
  before(() => {
    cy.request('api/events/1/').then(response => {
      const body = response.body as Event
      const evaluators = body?.evaluators
      if (Array.isArray(evaluators) && evaluators.length > 0 && evaluators[0]?.id) {
        evaluatorName = evaluators[0].id
      }
    })
  })
  const sortableFields = [...M2_FIELD_NAMES.keys()]
  for (const field of sortableFields) {
    it(`Should accept ${field} as sort param on evaluator view`, () => {
      const query = evalPage.apiExt({ view: 'all', sort: [field] })
      const apiEndpoint = `/api/events/1/evaluator/${evaluatorName}/${query}`
      cy.request('GET', apiEndpoint).then(response => {
        expect(response.status).to.eq(200)
      })
    })
  }
})
