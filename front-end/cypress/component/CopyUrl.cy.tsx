import CopyUrl from '@src/components/CopyUrl'
import { isEmpty } from 'cypress/types/lodash';

describe('Accordion.cy.tsx', () => {
    beforeEach(() => {
        // Code to run before each 'it'in describe block
        cy.mount(<CopyUrl/>)
      });

  it('displays copy url button', () => {
    cy.contains('button', 'Copy URL')
    .should('have.class', 'a-btn')
    .and('be.visible')
  })  

  it('button displays "Copy URL" after intial call/action', () => {
    cy.get('button').contains('Copy URL').click()
    .should('contain', 'URL Copied!')
    cy.wait(500)
    cy.get('.a-btn').should('contain', 'Copy URL')
  })

  it('should copy URL to the clipboard', { browser: 'electron' }, () => {

    cy.url().then((url) => {
    let currentUrl = url
    cy.wrap(currentUrl).as('currentUrl')
    cy.log('The current URL is: ' + currentUrl)
    cy.get('button').click(); 

    // compare clipboard to url
    cy.window().then(async (win) => {
      const clipboardContent = await win.navigator.clipboard.readText()
      expect(clipboardContent).to.eq(currentUrl)
      })
    })
  });

    describe('copy button failure', () =>{
        beforeEach(() => {
          window.history.pushState({}, '', null)
          cy.mount(<CopyUrl />)
      });
        
        it.only('button displays "Failed to copy URL" when clicked', () => {
            cy.get('button').click()  
            .should('contain', 'Failed to copy URL')
            .and('be.visible')
            // query cypress for result **as alias**
      //   cy.wait('@responseRole').then(({ request, response }) => {
      //   console.log(request.body)
      //   console.log(response.body)
      // })
    })
  })
})