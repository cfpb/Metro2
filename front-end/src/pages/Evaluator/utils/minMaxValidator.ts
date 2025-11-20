import { z } from 'zod'

/**
 * Validation for an optional number in search params.
 */
const minMaxValidator = z
  .union([z.number(), z.enum([''])])
  .optional()
  .catch('') // eslint-disable-line unicorn/prefer-top-level-await

export default minMaxValidator
