import { Link } from '@tanstack/react-router'
import type { ReactElement } from 'react'
import './Breadcrumbs.less'

export interface Breadcrumb {
  text: string
  href: string
}

interface BreadcrumbProperties {
  links: Breadcrumb[]
}

export function Breadcrumbs({ links }: BreadcrumbProperties): ReactElement {
  return (
    <nav className='m-breadcrumbs'>
      {links.map(link => (
        <Link className='m-breadcrumbs_crumb' to={link.href} key={link.href}>
          &lt; {link.text}{' '}
        </Link>
      ))}
    </nav>
  )
}
