import getHeaderName from './getHeaderName'

/**
 * generateDownloadData()
 *
 * Generates a CSV string using a list of fields, an array of records with those fields,
 * and a map matching field names to header values.
 *
 * Generates a header string by looking up each of the fields in the header map.
 * Generates comma-separated string of field values for each record.
 * Returns all the strings joined with new line characters.
 *
 * @param {array} fields - Ordered array of field names
 * @param {array} records - Array of objects with values for the fields
 * @param {map} headerMap - Map containing header values for the fields
 * @returns {string} - CSV string containing header and body rows for each record
 *
 */
export const generateDownloadData = <T>(
  fields: string[],
  records: T[],
  headerMap: Map<string, string>
): string => {
  const csvHeader = fields.map(field => getHeaderName(field, headerMap)).join(',')
  const csvBody = records
    .map(record =>
      fields
        // For each record, extract values for each of the fields and join them with commas.
        .map(field => {
          const val = record[field as keyof T]
          // If the field's value is a string containing commas, wrap it in quotes
          // so its internal commas aren't read as separators
          if (typeof val === 'string' && val.includes(',')) return `"${val}"`
          // If the value is an array, join the array's contents with commas
          // and wrap in quotes as above.
          if (Array.isArray(val)) return `"${val.join(', ')}"`
          // Otherwise, extract the value as is.
          return val
        })
        .join(',')
    )
    .join('\n')
  return [csvHeader, csvBody].join('\n')
}

/**
 * downloadData()
 *
 * Initiates a download for a locally-generated file as a blob.
 *
 * @param {buffer | string} file - A buffer or CSV string to download
 * @param {string} fileName - Name for the file
 * @param {string} fileType - Type for the file
 *
 */
//
export const downloadData = (
  file: Buffer | string,
  fileName: string,
  fileType = 'data:text/csv'
): void => {
  const blob = new Blob([file], { type: fileType })
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = fileName
  link.click()
  window.URL.revokeObjectURL(url)
}

/**
 * downloadFileFromURL()
 *
 * Given the URL of a file, initiates a download by creating
 * and programmatically clicking an off-screen link for the file.
 *
 * @param {string} url - File URL
 *
 */
export const downloadFileFromURL = (url: string): void => {
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.click()
}
