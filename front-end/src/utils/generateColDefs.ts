import type { ColDef } from 'ag-grid-community'
import getHeaderName from './getHeaderName'

/**
 * generateColumnDefinitions()
 *
 * Generates AG Grid column definitions for a list of Metro 2 fields.
 *
 * @param {array} fields - An array of Metro 2 field names
 * @param {object} colDefProps - Optional additional props for individual fields,
 *                               with format:
 *                                 {
 *                                    fieldName: {prop1: value, prop2: value}
 *                                 }
 * @returns {array} An array of column definitions, with the following format:
 *                  {
 *                    field: field,
 *                    headerName: title for field from M2_FIELD_NAMES map,
 *                    ...any extra field-specific props
 *                   }
 */
const generateColumnDefinitions = (
  fields: string[],
  colDefProps: Record<string, object> = {}
): ColDef[] =>
  fields.map(field => ({
    field,
    headerName: getHeaderName(field),
    ...colDefProps[field]
  }))

export default generateColumnDefinitions
