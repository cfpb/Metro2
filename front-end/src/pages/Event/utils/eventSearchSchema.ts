/* eslint-disable unicorn/prefer-top-level-await */
import { validateSortQueryParams } from '@src/utils/sortState'
import { z } from 'zod'
import { EVENT_COLUMN_MAP } from './eventColumns'

export const eventSchema = z.object({
  sort: z
    .any()
    .transform(val => validateSortQueryParams(val, [...EVENT_COLUMN_MAP.keys()]))
    .catch(['id'])
    .default(['id'])
})

export type EventSearch = z.infer<typeof eventSchema>
