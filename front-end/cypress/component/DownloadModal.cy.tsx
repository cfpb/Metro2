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
    cy.get('.modal').within( () => {  
       cy.findByTestId('pii-checkbox').should('not.be.checked')  
    })  
  })

  it('Download button disabled on page load', () => {
    cy.get('.modal').within( () => {
       cy.findByTestId('csv-download-button')
        .should('be.disabled')
    })
  })

  it('Download button is enable/disabled with PII checkbox value', () => {
    cy.findByTestId('pii-checkbox')
    cy.get('label').click()
    cy.findByTestId('csv-download-button')
    .should('be.enabled')
    cy.get('label').contains('PII').click()
    cy.findByTestId('csv-download-button')
    .should('be.disabled')
  })
})