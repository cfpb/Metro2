import type { ReactElement } from 'react'

/**
 * EvaluatorLongDescription
 *
 * Long descriptions for evaluators are created and stored in an Excel spreadsheet
 * where they are formatted for readability with things like bold subheadings.
 * That formatting is mostly lost -- with the exception of line breaks --
 * when the spreadsheet is converted into a CSV for inport into the tool's database.
 *
 * Eventually the spreadsheet's contents may be maintained in a location
 * where they can be styled with a WYSIWYG editor. For now, this component provides
 * a workaround by taking a long description string that is only formatted with
 * line breaks and restoring some of the formatting from the spreadsheet by:
 *     - splitting the string into segments at double line breaks
 *     - splitting the segements into lines at single line breaks
 *     - formatting the first line of a segment as an H4 if it does not contain a
 *       pseudo code symbol
 *     - formatting all other lines as paragraphs
 *
 */

interface LongDescriptionData {
  content: string
}

const pseudoCodeSymbols = [':', '<', '>', '=', '≠']

export default function EvaluatorLongDescription({
  content
}: LongDescriptionData): ReactElement {
  return (
    <>
      {content.split('\n\n').map(segment => (
        <>
          {' '}
          {segment.split('\n').map((line, lineIndex) =>
            lineIndex === 0 &&
            !pseudoCodeSymbols.some(char => line.includes(char)) ? (
              // eslint-disable-next-line react/no-array-index-key
              <h4 key={lineIndex}>{line}</h4>
            ) : (
              // eslint-disable-next-line react/no-array-index-key
              <p key={lineIndex}>{line}</p>
            )
          )}
        </>
      ))}
    </>
  )
}
