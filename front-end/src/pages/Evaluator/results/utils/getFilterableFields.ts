import { evaluatorSchema } from '@src/pages/Evaluator/utils/evaluatorSearchSchema'

// List of filters that can be applied to evaluator results
const filterableFields: string[] = evaluatorSchema
  .keyof()
  .options.filter(key => !['page', 'view', 'page_size', 'sort'].includes(key))

export default filterableFields
