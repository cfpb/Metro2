import {
  AppFooter,
  Link as DSRLink,
  type LinkProperties
} from '@cfpb/design-system-react'
import DOMPurify from 'dompurify'
import type { ReactElement } from 'react'
import { HTMLProps } from 'react'

type footerLinkType = Omit<LinkProperties, 'preload'>

interface FooterProps extends HTMLProps<HTMLElement> {
  content?: string
  links?: footerLinkType[] | null
  showTagline?: boolean
}

export function Metro2Footer({
  content,
  links,
  showTagline = false
}: FooterProps): ReactElement {
  return (
    <AppFooter
      navLinks={
        Array.isArray(links) && links.length > 0
          ? links.map(link => {
              const { label, ...others } = link
              return <DSRLink key={label} label={label} {...others} />
            })
          : undefined
      }
      footerContent={
        content ? (
          <div
            data-testid='footer-content'
            dangerouslySetInnerHTML={{ __html: content }}
          />
        ) : undefined
      }
      className={showTagline ? undefined : 'o-footer--no-tagline'}
    />
  )
}

const footerContent = DOMPurify.sanitize(
  import.meta.env.VITE_FOOTER_CONTENT as string
)
const showFooterTagline =
  (import.meta.env.VITE_SHOW_FOOTER_TAGLINE as string) === 'true' ? true : false

const footerLinkContent = import.meta.env.VITE_FOOTER_LINKS as string

let footerLinks = [] as footerLinkType[]
try {
  footerLinks = JSON.parse(footerLinkContent) as footerLinkType[]
} catch (error) {
  // eslint-disable-next-line no-console
  console.log(error)
}

export const M2Footer = (
  <Metro2Footer
    content={footerContent}
    links={footerLinks}
    showTagline={showFooterTagline}
  />
)
