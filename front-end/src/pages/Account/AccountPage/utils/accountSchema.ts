/* eslint-disable unicorn/prefer-top-level-await */
import { accountTableFields } from '@src/pages/Account/AccountPage/utils/accountTableFields'
import { validateSortQueryParams } from '@src/utils/sortState'
import { z } from 'zod'

export const accountPageSchema = z.object({
  sort: z
    .any()
    .transform(val => validateSortQueryParams(val, accountTableFields))
    .catch(['activity_date'])
    .default(['activity_date'])
})

export type AccountSchema = z.infer<typeof accountPageSchema>
