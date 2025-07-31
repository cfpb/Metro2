import TabbedNavigation from '@src/components/TabbedNavigation/TabbedNavigation'

describe('TabbedNavigation.cy.tsx', () => {
  it('displays tabs', () => {
    const tabs = [
      {
        id: 'tab-one',
        icon: 'filter',
        text: 'Tab one',
        isActive: false
      },
      {
        id: 'tab-two',
        icon: 'search',
        text: 'Tab two',
        isActive: true
      }
    ]
    cy.mount(<TabbedNavigation tabs={tabs} />)
    cy.findByTestId('tab-one')
      .should('be.visible')
      .and('not.have.class', 'active')
      .and('have.text', 'Tab one')
      .find('svg')
      .should('be.visible')
      .and('have.attr', 'alt', 'filter')
    cy.findByTestId('tab-two')
      .should('be.visible')
      .and('have.class', 'active')
      .and('have.text', 'Tab two')
      .find('svg')
      .should('be.visible')
      .and('have.attr', 'alt', 'search')
  })
})
