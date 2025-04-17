import type EvaluatorMetadata from 'types/Evaluator'

export interface EventMetadata {
  id: number
  name: string
  portfolio?: string | null
  eid_or_matter_num?: string | null
  other_descriptor?: string | null
  date_range_start: string | null
  date_range_end: string | null
}

export const EVENT_FIELDS = new Map([
  ['id', 'ID'],
  ['name', 'Name'],
  ['eid_or_matter_num', 'EID or matter number'],
  ['other_descriptor', 'Description'],
  ['portfolio', 'Portfolio'],
  ['date_range_start', 'Date range start'],
  ['date_range_end', 'Date range end']
])

export default interface Event extends EventMetadata {
  evaluators: EvaluatorMetadata[]
}
