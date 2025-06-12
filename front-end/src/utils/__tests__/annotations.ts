import { M2_FIELD_LOOKUPS } from '../../constants/annotationLookups'
import { annotateAccountRecords, getM2Definition } from '../annotations'

describe('getM2Definition', () => {
  it('should return undefined when field has no lookup', () => {
    const definition = getM2Definition('fake_field', 'fake_value')
    expect(definition).toBeUndefined()
  })

  it('should return undefined when value does not exist on field', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2Definition(validField, 'fake_value')
    expect(definition).toBeUndefined()
  })

  it('should return undefined when value is null', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2Definition(validField, null)
    expect(definition).toBeUndefined()
  })

  it('should return undefined when value is undefined', () => {
    const validField = Object.keys(M2_FIELD_LOOKUPS)[0]
    const definition = getM2Definition(validField)
    expect(definition).toBeUndefined()
  })

  it('should return definitions for valid fields and values', () => {
    const validFields = Object.keys(M2_FIELD_LOOKUPS)
    for (const field of validFields) {
      const lookup = M2_FIELD_LOOKUPS[field as keyof typeof M2_FIELD_LOOKUPS]
      const validValues = Object.keys(lookup)
      for (const value of validValues) {
        const definition = getM2Definition(field, value)
        expect(definition).toEqual(lookup[value as keyof typeof lookup])
      }
    }
  })
})

describe('annotateAccountRecords', () => {
  it('annotates fields with coded values, including arrays', () => {
    const records = [
      {
        id_num: '1601',
        cons_acct_num: '123456789',
        inconsistencies: ['Test-Eval-1', 'Test-Eval-2'],
        activity_date: '2018-10-31',
        acct_stat: '11',
        amt_past_due: 100,
        current_bal: 100,
        orig_chg_off_amt: 0,
        dofd: '2018-01-31',
        php: '111110010010000000000DDD',
        account_holder__cons_info_ind_assoc: ['A', 'B'],
        terms_freq: 'M'
      },
      {
        id_num: '1602',
        cons_acct_num: '987654321',
        inconsistencies: ['Test-Eval-1'],
        activity_date: '2018-10-31',
        acct_stat: '11',
        amt_past_due: 1000,
        current_bal: 1000,
        orig_chg_off_amt: 0,
        dofd: '2018-01-31',
        php: '011110010010000000000DDD',
        php1: '0',
        account_holder__cons_info_ind_assoc: null,
        terms_freq: 'D',
        spc_com_cd: 'AI'
      }
    ]
    const annotatedRecords = [
      {
        id_num: '1601',
        cons_acct_num: '123456789',
        inconsistencies: ['Test-Eval-1', 'Test-Eval-2'],
        activity_date: '2018-10-31',
        acct_stat: '11 (0-29 days past the due date (current account))',
        amt_past_due: 100,
        current_bal: 100,
        orig_chg_off_amt: 0,
        dofd: '2018-01-31',
        php: '111110010010000000000DDD',
        account_holder__cons_info_ind_assoc: [
          'A (Petition for Chapter 7 Bankruptcy)',
          'B (Petition for Chapter 11 Bankruptcy)'
        ],
        terms_freq: 'M (Monthly)'
      },
      {
        id_num: '1602',
        cons_acct_num: '987654321',
        inconsistencies: ['Test-Eval-1'],
        activity_date: '2018-10-31',
        acct_stat: '11 (0-29 days past the due date (current account))',
        amt_past_due: 1000,
        current_bal: 1000,
        orig_chg_off_amt: 0,
        dofd: '2018-01-31',
        php: '011110010010000000000DDD',
        php1: '0 (0 – 29 days past due date (current account))',
        account_holder__cons_info_ind_assoc: '',
        terms_freq: 'D (Deferred)',
        spc_com_cd: 'AI (Recalled to active military duty.)'
      }
    ]
    expect(annotateAccountRecords(records)).toEqual(annotatedRecords)
  })
})
