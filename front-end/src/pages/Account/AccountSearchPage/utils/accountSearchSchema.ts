import DOMPurify from 'dompurify'
import { z } from 'zod'

/**
 * cons_acct_num param in account search can be:
 *   - a string
 *   - a number
 *   - an array of strings or numbers
 *   - an empty string
 *   - undefined
 *
 * We sanitize the cons_acct_num value by:
 *   - removing any html tags
 *   - removing any leading/trailing spaces
 *   - removing any empty values if it's an array
 */
export const accountSearchSchema = z.object({
  cons_acct_num: z
    .union([
      z.string().transform(val => DOMPurify.sanitize(val, { ALLOWED_TAGS: [] })),
      z.number(),
      z
        .array(
          z.union([
            z
              .string()
              .transform(val => DOMPurify.sanitize(val, { ALLOWED_TAGS: [] })),
            z.number()
          ])
        )
        .transform(val => {
          return val.filter(str => String(str).trim() !== '')
        })
    ])
    .nullable()
    .optional()
})

export type AccountSearchSchema = z.infer<typeof accountSearchSchema>
