import { fallback } from '@tanstack/router-zod-adapter'
import { z } from 'zod'

const BooleanStringValidator = fallback(
  z
    .union([
      z.boolean().transform(val => val.toString()),
      z.enum(['any', 'true', 'false', ''])
    ])
    .optional(),
  ''
)

export default BooleanStringValidator
