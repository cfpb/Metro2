export default interface EvaluatorMetadata {
  id: string
  name: string
  description: string
  hits: number | null
  accounts: number | null
  long_description?: string
  category?: string | null
  ipl?: string | null
  product_line?: string[] | null
  fields_used?: string[] | null
  fields_display?: string[] | null
  risk_level?: string | null
  crrg_topics?: string | null
  crrg_page?: number | null
  pdf_page?: number | null
  use_notes?: string | null
  alternative_explanation?: string | null
}
