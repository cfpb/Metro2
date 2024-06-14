import type EvaluatorMetadata from '../Evaluator/Evaluator'

export interface EventMetadata {
  id: number
  name: string
  portfolio?: string | null
  eid_or_matter_num?: string | null
  other_descriptor?: string | null
  date_range_start: string | null
  date_range_end: string | null
}

export default interface Event extends EventMetadata {
  evaluators: EvaluatorMetadata[]
}
