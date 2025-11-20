import { validateSortParams } from '@src/components/Table/tableUtils'
import M2_FIELD_NAMES from '@src/constants/m2FieldNames'
import { z } from 'zod'

const sortValidator = z
  .any()
  .transform(val => validateSortParams(val, [...M2_FIELD_NAMES.keys()]))
  .default(['activity_date'])
  .catch(['activity_date']) // eslint-disable-line unicorn/prefer-top-level-await

export default sortValidator
