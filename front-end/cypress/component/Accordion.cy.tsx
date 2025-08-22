import Accordion from '../../src/components/Accordion/Accordion'
import '../../src/components/Accordion/Accordion.less'
import '../fixtures/event_1.json'

describe('Accordion.cy.tsx', () => {
  beforeEach(() => {
      // Code to run before each 'it'in describe block
      cy.mount(<Accordion header='Criteria evaluated'>
      //   <div className="long-description">
      //     <h4>Current balance is less than amount past due</h4>
      //     <p>Current balance &lt; amount past due</p>
      //   </div>
      // </Accordion>)
  })
      
  it('displays accordion', () => {
    cy.get('[data-test-id="accordion"]')
    .find('button')
    .contains('Criteria evaluated')
    .and('be.visible')
  })

  it('accordion has a border', () => {
    cy.get('[data-test-id="accordion"]')
    .should('have.css', 'border')
  })

  it('accordion is closed on load', () => {
    cy.get('[data-test-id="accordion"]')
    .find('button') 
    .should('have.text', 'Criteria evaluated')
    .get('[data-test-id="expandable-content"]')
    .find('[data-test-id="accordion-inner"]')
    .should('not.be.visible')
  })

  it('accordion expands', () => {
    cy.get('[data-test-id="accordion"]')
    .find('button') 
    .should('have.text', 'Criteria evaluated').click()
    .get('[data-test-id="expandable-content"]')
    .find('[data-test-id="accordion-inner"]')
    .should('be.visible')
  })

  it('load accordion child content', () => {
    cy.get('[data-test-id="accordion"]')
    .find('button').click()
    .get('[data-test-id="accordion-inner"]')
    .should('be.visible')
    .get('div.long-description').within(() => {
      cy.get('h4').should('exist');
      cy.get('p').should('exist')
    })
  })

  it('down arrow displayed on load', () => {
     cy.get('[data-test-id="accordion"]')
    .find('button')
    .find('svg')
    .should('have.attr', 'alt', 'down')
  })

  it('down arrow switches to up arrow on click', () => {
    cy.get('[data-test-id="accordion"]')
    .find('button')
    .find('svg').click()
    .get('svg.cf-icon-svg--up')
    .should('have.attr', 'alt', 'up')
  })
})