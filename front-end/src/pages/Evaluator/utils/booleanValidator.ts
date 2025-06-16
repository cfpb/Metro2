import { z } from 'zod'

const BooleanStringValidator = z
  .union([
    z.boolean().transform(val => val.toString()),
    z.enum(['any', 'true', 'false'])
  ])
  .optional()

export default BooleanStringValidator
