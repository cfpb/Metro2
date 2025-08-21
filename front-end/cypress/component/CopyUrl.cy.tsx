import CopyUrl from '@src/components/CopyUrl'

describe('CopyUrl.cy.tsx', () => {
  beforeEach(() => {
    cy.mount(<CopyUrl/>)
  });

  it('displays copy url button', () => {
    cy.contains('button', 'Copy URL')
    .should('have.class', 'a-btn')
    .and('be.visible')
  })  

  it('button displays "Copy URL" after intial call/action', () => {
    cy.window().then((win) => {
      cy.stub(win.navigator.clipboard, 'writeText').as('clipboardWrite').resolves()
    })
    cy.get('button').contains('Copy URL').click().should('contain', 'URL Copied!')
    cy.get('@clipboardWrite').should('have.been.calledOnce')
    cy.wait(500)
    cy.get('.a-btn').should('contain', 'Copy URL')
  })

  it('should copy URL to the clipboard', () => {
    cy.window().then((win) => {
      cy.stub(win.navigator.clipboard, 'writeText').as('clipboardWrite').resolves()
    })
    cy.url().then((url) => {
      cy.get('button').contains('Copy URL').click().should('contain', 'URL Copied!')
      cy.get('@clipboardWrite').should('have.been.calledOnceWith', url)
    })
  }) 
        
  it('button displays "Failed to copy URL" when clipboard copy fails', () => {
    cy.window().then((win) => {
      cy.stub(win.navigator.clipboard, 'writeText').as('clipboardWrite').throws()
    })
    cy.get('button').click()  
      .should('contain', 'Failed to copy URL')
      .and('be.visible')
      cy.get('@clipboardWrite').should('have.been.calledOnce')
  })
})
