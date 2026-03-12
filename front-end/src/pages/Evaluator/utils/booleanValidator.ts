/* eslint-disable unicorn/prefer-top-level-await */

import { z } from 'zod'

const BooleanStringValidator = 
  z
    .union([
      z.boolean().transform(val => val.toString()),
      z.enum(['any', 'true', 'false', ''])
    ])
    .catch('')
    .optional()
   


export default BooleanStringValidator
