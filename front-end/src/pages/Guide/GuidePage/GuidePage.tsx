import { Link, Outlet } from '@tanstack/react-router'
import { Layout, List, ListItem, Paragraph } from 'design-system-react'
import type { ReactElement } from 'react'
import './GuidePage.less'

export default function GuidePage(): ReactElement {
  const menuItems = [
    { name: 'Overview of Metro2 evaluator tool', path: '/guide/' },
    { name: 'Explore the Metro2 interface', path: '/guide/explore' },
    {
      name: "Use Metro2's advanced table features",
      path: '/guide/table'
    },
    {
      name: 'Contributing to an evaluator’s metadata',
      path: '/guide/contribute'
    },
    { name: 'Metro2 administrator features', path: '/guide/m2admin' }
  ]

  return (
    <Layout.Main layout='1-3'>
      <Layout.Wrapper>
        <Layout.Sidebar id='sidebar'>
          <Paragraph isLead>User guide</Paragraph>
          <div>
            <List isUnstyled>
              {menuItems.map(item => (
                <ListItem key={item.name}>
                  <Link
                    key={item.name}
                    to={item.path}
                    className='o-secondary-nav__link o-secondary-nav__link--parent'
                    activeOptions={{ exact: true }}
                    activeProps={{ className: 'o-secondary-nav__link--current' }}>
                    {item.name}
                  </Link>
                </ListItem>
              ))}
            </List>
          </div>
        </Layout.Sidebar>
        <Layout.Content>
          <div className='content-pad'>
            <Outlet />
          </div>
        </Layout.Content>
      </Layout.Wrapper>
    </Layout.Main>
  )
}
