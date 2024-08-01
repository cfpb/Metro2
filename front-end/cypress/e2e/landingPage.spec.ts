import { PII_COOKIE_NAME } from '../../src/utils/constants'
import { testLocatorBar } from '../helpers/page_helper'

describe('Landing page loader', () => {
  it('Should show a loading view while the user data is being fetched', () => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', '/api/users/', {
      delay: 2000,
      fixture: 'user'
    }).as('getUser')
    cy.visit('/')
    cy.get('.loader').should('be.visible')
    cy.wait('@getUser')
    cy.get('.loader').should('not.exist')
  })
})

describe('Landing page', () => {
  beforeEach(() => {
    cy.setCookie(PII_COOKIE_NAME, 'true')
    cy.intercept('GET', 'api/users/', { fixture: 'user' }).as('getUser')
    cy.visit('/')
    cy.wait('@getUser')
  })

  it('Should show username and welcome message in locator bar', () => {
    testLocatorBar('Welcome, Test user', 'Here is your events list')
  })
})
