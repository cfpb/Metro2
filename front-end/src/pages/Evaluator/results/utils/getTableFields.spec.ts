import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { getTableFields } from './getTableFields'

describe('getTableFields', () => {
  it('should return fields in correct order', () => {
    const result = getTableFields(['acct_type', 'port_type'])

    const expectedFields = [
      ...new Set([
        // Identifier fields come first
        'cons_acct_num',
        'activity_date',

        // Then fields used
        'acct_type',
        'port_type',

        // Then filterable fields
        'acct_stat',
        'current_bal',
        'amt_past_due',
        'dofd',
        'compl_cond_cd',
        'php1',
        'php',
        'pmt_rating',
        'spc_com_cd',
        'terms_freq',
        'cons_info_ind',
        'cons_info_ind_assoc',
        'l1__change_ind',
        'date_closed',

        // Then the remaining fields
        ...M2_FIELD_NAMES.keys()
      ])
    ]

    expect(result).toEqual(expectedFields)
  })
})
