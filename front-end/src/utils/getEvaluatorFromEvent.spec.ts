import getEvaluatorDataFromEvent from './getEvaluatorFromEvent'

const testEval = {
  hits: 1000,
  accounts_affected: 450,
  inconsistency_start: '2020-01-30',
  inconsistency_end: '2020-11-30',
  id: 'Test-Eval-1',
  description: 'This is a test evaluator.',
  long_description: 'This is a test evaluator.\nTest value 1 < test value 2',
  fields_used: ['dofd', 'current_bal'],
  fields_display: [],
  crrg_reference: '',
  potential_harm: '',
  rationale: '',
  alternate_explanation: '',
  category: 'Delinquency'
}

const testEvent = {
  id: 1,
  name: 'Test event',
  portfolio: '',
  eid_or_matter_num: '',
  other_descriptor: '',
  directory: '',
  date_range_start: '2020-01-30',
  date_range_end: '2020-11-30',
  evaluators: [testEval]
}

describe('getEvaluatorFromEvent', () => {
  it('returns evaluator metadata object from event', () => {
    expect(getEvaluatorDataFromEvent(testEvent, 'Test-Eval-1')).toEqual(testEval)
  })

  it('returns undefined when evaluator id not found on event', () => {
    expect(getEvaluatorDataFromEvent(testEvent, 'Fake-Eval')).toEqual(undefined)
  })
})
