/* eslint-disable unicorn/prefer-top-level-await */

import { z } from 'zod'

/**
 * Validation for an optional number in search params.
 *
 * The empty string fallback is used because it causes
 * Tanstack router to remove the parameter
 * from the query string if its value is invalid.
 */
const minMaxValidator = z.union([z.number(), z.enum([''])]).optional().catch('')

export default minMaxValidator
