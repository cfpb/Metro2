import { Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import './Breadcrumbs.less'

// TODO: This is a preliminary implementation rendering
// a single breadcrumb that links to parent page
export default function Breadcrumbs(): ReactElement {
  return (
    <nav className='m-breadcrumbs'>
      <Link className='m-breadcrumbs_crumb' to='../..'>
        &lt; Back to event results
      </Link>
    </nav>
  )
}
