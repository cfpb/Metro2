import { PII_COOKIE_NAME } from '@src/constants/settings'

describe('Errors', () => {
  beforeEach(() => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
  })

  describe('General errors', () => {
    it('Should render a permissions error for an unauthorized response', () => {
      cy.intercept('GET', '/api/events/2/', { statusCode: 401 })
      cy.visit('/events/2/')

      cy.get('[data-testid="error-title"]').should(
        'have.text',
        'Sorry, we can’t show you this page.'
      )
    })

    it('Should render a general error for a 500 response', () => {
      cy.intercept('GET', '/api/events/2/', { statusCode: 500 })

      cy.visit('/events/2/')

      cy.get('[data-testid="error-title"]').should(
        'have.text',
        'Something went wrong.'
      )
    })
  })

  describe('Not found errors', () => {
    it('Should render a not found message for a non-existent route', () => {
      cy.visit('/not-a-real-route')

      cy.get('[data-testid="error-title"]').should(
        'have.text',
        'The page doesn’t exist.'
      )
    })

    it('Should render a not found message for a non-existent event', () => {
      cy.intercept('GET', '/api/events/123456789/', { statusCode: 404 })

      cy.visit('/events/123456789')

      cy.get('[data-testid="error-title"]').should(
        'have.text',
        'The page doesn’t exist.'
      )
    })

    it('Should render a not found message for a non-existent evaluator', () => {
      cy.intercept('GET', 'api/events/1/', { fixture: 'event_1' }).as('getEvent')
      cy.intercept('GET', '/api/users/', { fixture: 'user' }).as('getUser')

      cy.visit('/events/1/evaluators/not-an-evaluator')
      cy.wait(['@getEvent', '@getUser'])

      cy.get('[data-testid="error-title"]').should(
        'have.text',
        `The results for this evaluator don’t exist.`
      )
    })

    it('Should render a not found message for a non-existent account', () => {
      cy.intercept('GET', '/api/events/1/', { fixture: 'event_1' }).as('getEvent')
      cy.intercept('GET', '/api/events/1/account/not-an-account/', {
        statusCode: 404
      }).as('nonexistentAccount')

      cy.visit('/events/1/accounts/not-an-account')

      cy.wait(['@getEvent', '@nonexistentAccount'])

      cy.get('[data-testid="error-title"]').should(
        'have.text',
        `The account doesn’t exist.`
      )
    })

    it('Should show a mailto link if admin email env variable is set', () => {
      cy.intercept('GET', '/api/events/1/', { fixture: 'event_1' }).as('getEvent')
      cy.intercept('GET', '/api/events/1/account/not-an-account/', {
        statusCode: 404
      }).as('nonexistentAccount')

      cy.visit('/events/1/accounts/not-an-account')

      cy.wait(['@getEvent', '@nonexistentAccount'])
      cy.env(['VITE_ADMIN_EMAIL']).then(({ VITE_ADMIN_EMAIL }) => {
        if (VITE_ADMIN_EMAIL) {
          cy.findByTestId('contact-link')
            .should('exist')
            .and('have.attr', 'href')
            .and('include', `mailto:${VITE_ADMIN_EMAIL}`)
        } else {
          cy.findByTestId('contact-link').should('not.exist')
        }
      })
    })
  })
})
