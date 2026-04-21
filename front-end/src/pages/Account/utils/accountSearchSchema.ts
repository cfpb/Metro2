/* eslint-disable unicorn/prefer-top-level-await */
import { accountTableFields } from '@src/pages/Account/utils/accountTableFields'
import { validateSortQueryParams } from '@src/utils/sortState'
import { z } from 'zod'

export const accountSchema = z.object({
  sort: z
    .any()
    .transform(val => validateSortQueryParams(val, accountTableFields))
    .catch(['activity_date'])
    .default(['activity_date'])
})

export type AccountSearch = z.infer<typeof accountSchema>
