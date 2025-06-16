import { fallback } from '@tanstack/router-zod-adapter'
import { z } from 'zod'

/**
 * Validation for an optional number in search params.
 *
 * The empty string fallback is used because it causes
 * Tanstack router to remove the parameter
 * from the query string if its value is invalid.
 */
const minMaxValidator = fallback(z.union([z.number(), z.enum([''])]).optional(), '')

export default minMaxValidator
