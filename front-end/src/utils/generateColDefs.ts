import type { ColDef } from 'ag-grid-community'
import getHeaderName from './getHeaderName'

// Given a list of M2 fields and an object of field-specific col def props,
// generate an array of AgGrid column definition objects
// with the following format:
// {
//    field: field,
//    headerName: field's name from M2_FIELD_NAMES,
//    ...{field-specific col def props}
// }
const generateColumnDefinitions = (
  fields: string[],
  colDefProps: Record<string, object>
): ColDef[] =>
  fields.map(field => ({
    field,
    headerName: getHeaderName(field),
    ...colDefProps[field]
  }))

export default generateColumnDefinitions
