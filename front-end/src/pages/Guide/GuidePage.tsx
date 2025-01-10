import { Layout, Heading, Divider } from 'design-system-react'
import type { ReactElement } from 'react'
import './GuidePage.less'
import { Outlet, Link } from '@tanstack/react-router'
import Overview from './Overview'

export default function GuidePage(): ReactElement {

  const menuItems =[
    {name:'1. Metro2 evaluator tool overview', path: '/guide/'}, 
    {name:'2. Explore the Metro2 UI', path: '/guide/explore'}, 
    {name:'3. Contributing to an evaluator’s metadata', path: '/guide/contribute'}, 
    {name:'4. Help us improve the Metro2 evaluator tool for you', path: '/guide/help-us'}, 
    {name:'5. Metro 2 administrator features', path: '/guide/m2admin'}]

  return (
    <Layout.Main layout="1-3">
        <Layout.Wrapper>
          <Layout.Sidebar id='sidebar'>
            <Heading type="4">
                  Table of contents
            </Heading>
            <div>
              {menuItems.map(item => (
              <Link
                key={item.name}
                to={item.path}
                className='??'
                activeOptions={{ exact:true }}
                activeProps={{ className: 'hover' }}>
                {item.name}
              </Link>
              ))}
            </div>
          </Layout.Sidebar>
          <Layout.Content>

            <div className='content-pad'>
              <Heading type="2">
                User guide for Metro 2
              </Heading>

            <Divider />

              <Outlet/>
            </div>
              
          </Layout.Content>      
      </Layout.Wrapper>
    </Layout.Main>
  )
}