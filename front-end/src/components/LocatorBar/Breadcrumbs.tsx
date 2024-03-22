import type { ReactElement } from 'react'
import './Breadcrumbs.less'
import { Link } from '@tanstack/react-router'

// TODO: This is a preliminary implementation rendering 
// a single breadcrumb that links to parent page
export default function Breadcrumbs(): ReactElement {
  return (
    <nav className='m-breadcrumbs'>
      <Link className='m-breadcrumbs_crumb' to='../..'>
        &lt; Back to results
      </Link>
    </nav>
  )
}
