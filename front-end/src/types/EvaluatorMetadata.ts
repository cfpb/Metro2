export default interface EvaluatorMetadata {
  id: string
  description: string
  hits: number
  accounts_affected: number
  inconsistency_start: string
  inconsistency_end: string
  long_description: string
  fields_used?: string[]
  fields_display?: string[]
  category?: string
  alternate_explanation?: string | null
  crrg_reference?: string | null
  potential_harm?: string | null
  rationale?: string | null
}
