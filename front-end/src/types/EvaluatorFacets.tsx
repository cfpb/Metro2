import { FILTER_VALUES } from '@src/constants/annotationLookups'

export interface EvaluatorFacets {
  acct_stat?: Partial<Record<(typeof FILTER_VALUES.acct_stat)[number], number>>
  php1?: Partial<Record<(typeof FILTER_VALUES.php1)[number], number>>
  pmt_rating?: Partial<Record<(typeof FILTER_VALUES.pmt_rating)[number], number>>
  spc_com_cd?: Partial<Record<(typeof FILTER_VALUES.spc_com_cd)[number], number>>
  terms_freq?: Partial<Record<(typeof FILTER_VALUES.terms_freq)[number], number>>
  compl_cond_cd?: Partial<
    Record<(typeof FILTER_VALUES.compl_cond_cd)[number], number>
  >
  cons_info_ind?: Partial<
    Record<(typeof FILTER_VALUES.cons_info_ind)[number], number>
  >
  l1__change_ind?: Partial<
    Record<(typeof FILTER_VALUES.l1__change_ind)[number], number>
  >
}

export interface EvaluatorFacetData {
  count: number
  facets?: EvaluatorFacets
}
