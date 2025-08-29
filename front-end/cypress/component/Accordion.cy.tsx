import Accordion from '../../src/components/Accordion/Accordion'
import '../../src/components/Accordion/Accordion.less'
import '../fixtures/event_1.json'

describe('Accordion.cy.tsx', () => {
  beforeEach(() => {
      // Code to run before each 'it'in describe block
      cy.mount(<Accordion header='Criteria evaluated'>
      //   <div className="long-description">
      //     <h4>Subheading</h4>
      //     <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
      //   </div>
      // </Accordion>)
  })
      
  it('displays accordion', () => {
    cy.findByTestId('accordion')
    .find('button')
    .contains('Criteria evaluated')
    .and('be.visible')
  })

  it('accordion has a border', () => {
    cy.findByTestId('accordion')
    .should('have.css', 'border')
  })

  it('accordion is closed on load', () => {
    cy.findByTestId('accordion')
    .find('button') 
    .should('have.text', 'Criteria evaluated')
    cy.findByTestId('expandable-content')
    cy.findByTestId('accordion-inner')
    .should('not.be.visible')
  })

  it('accordion expands', () => {
    cy.findByTestId('accordion')
    .find('button') 
    .should('have.text', 'Criteria evaluated').click()
    cy.findByTestId('expandable-content')
    cy.findByTestId('accordion-inner')
    .should('be.visible')
  })

  it('load accordion child content', () => {
    cy.findByTestId('accordion')
    .find('button').click()
    cy.findByTestId('accordion-inner')
    .should('be.visible')
    .get('div.long-description').within(() => {
      cy.get('h4').should('exist');
      cy.get('p').should('exist')
    })
  })

  it('down arrow displayed on load', () => {
     cy.findByTestId('accordion')
    .find('button')
    .find('svg')
    .should('have.attr', 'alt', 'down')
  })

  it('down arrow switches to up arrow on click', () => {
    cy.findByTestId('accordion')
    .find('button')
    .find('svg').click()
    .get('svg.cf-icon-svg--up')
    .should('have.attr', 'alt', 'up')
  })
})
