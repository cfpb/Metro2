import type { ReactElement } from 'react'
import LocatorBar from 'components/LocatorBar/LocatorBar'

export default function EvaluatorPage(): ReactElement {
  return (
    <LocatorBar
      eyebrow='Inconsistency'
      heading='7-1a'
      subhead='SCC indicates paid but account status does not indicate paid'
      breadcrumbs
    />
  )
}
