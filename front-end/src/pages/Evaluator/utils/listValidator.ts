import { M2_FIELD_LOOKUPS } from '@src/constants/annotationLookups'
import { z } from 'zod'

export const validateFieldValues = (
  val: unknown,
  field: keyof typeof M2_FIELD_LOOKUPS
): string[] => {
  const arr = Array.isArray(val) ? val : [val]
  const lookup = M2_FIELD_LOOKUPS[field]

  return arr
    .filter(item => item in lookup || Number(item) in lookup || item === 'blank')
    .map(String)
}

export const listValueValidator = (
  field: keyof typeof M2_FIELD_LOOKUPS
): z.ZodOptional<z.ZodPipe<z.ZodAny, z.ZodTransform<string[], unknown>>> =>
  z
    .any()
    .transform(val => validateFieldValues(val, field))
    .optional()
