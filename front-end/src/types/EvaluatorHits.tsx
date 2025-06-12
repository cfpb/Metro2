import type AccountRecord from './AccountRecord'

export default interface EvaluatorHits {
  hits: AccountRecord[]
  count: number
}
