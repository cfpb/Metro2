import { z } from 'zod'

const BooleanStringValidator = z
  .union([
    z.boolean().transform(val => val.toString()),
    z.enum(['any', 'true', 'false', ''])
  ])
  .optional()
  .catch('') // eslint-disable-line unicorn/prefer-top-level-await

export default BooleanStringValidator
