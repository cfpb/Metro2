import DownloadModal from '../../src/components/Modal/DownloadModal'

describe('DownloadModal.cy.tsx', () => {
  beforeEach(() => {
    cy.mount(<DownloadModal open={true}/>)
  });

  it('Displays download modal', () => {
    cy.get('.modal')
    .should('be.visible')
  })
  
  it('PII checkbox unchecked on page load', () => {
    cy.get('.modal')
    cy.findByTestId('pii-checkbox')
    cy.get('[type="checkbox"]').should('not.be.checked')
  })

  it('Download button disabled on page load', () => {
    cy.get('.modal')
    cy.findByTestId('csv-download-button')
    .should('be.disabled')
  })

  it('Download button is enable/disabled with PII checkbox value', () => {
    cy.findByTestId('pii-checkbox')
    cy.get('label').click()
    cy.findByTestId('csv-download-button')
    .should('be.enabled')
    cy.findByTestId('pii-checkbox')
    cy.get('label').click()
    cy.findByTestId('csv-download-button')
    .should('be.disabled')
  })
})