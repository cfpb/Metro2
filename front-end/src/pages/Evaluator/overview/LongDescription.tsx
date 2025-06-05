import type { ReactElement } from 'react'

interface LongDescriptionData {
  content: string
}

// Generates html for an evaluator long description that is only formatted with line breaks.
// Splits string into segments at double line breaks. Breaks segments into lines.
// If the first line of a segment is explanatory rather than pseudo-code
// -- determined by checking for absence of symbols used in pseudo code lines --
// it's formatted as an H4. All other lines are formatted as paragraphs.

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
            ![':', '<', '>', '=', '≠'].some(char => line.includes(char)) ? (
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
