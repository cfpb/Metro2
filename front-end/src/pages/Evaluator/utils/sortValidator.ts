/* eslint-disable unicorn/prefer-top-level-await */
import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { validateSortQueryParams } from '@src/utils/sortState'
import { z } from 'zod'

const sortValidator = z
  .any()
  .transform(val => validateSortQueryParams(val, [...M2_FIELD_NAMES.keys()]))
  .catch(['activity_date'])
  .default(['activity_date'])

export default sortValidator
