export default interface EventMetadata {
  id: number
  name: string
  portfolio?: string | null
  eid_or_matter_num?: string | null
  other_descriptor?: string | null
  date_range_start: string | null
  date_range_end: string | null
}
