/* eslint-disable cypress/require-data-selectors */
import { PII_COOKIE_NAME } from '../../src/utils/constants'
import { Metro2Page } from '../helpers/pageHelper'
const page = new Metro2Page()

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

  it('Should show a welcome message including username', () => {
    page.verifyLocatorBarContent('Welcome, Test user', 'Here is your events list')
  })

  it('Should show a list of events assigned to user', () => {
    cy.get('.event-item')
      .should('have.length', 2)
      .then(events => {
        // Basic event
        cy.wrap(events[0]).within(() => {
          cy.findByTestId('event-header').should(
            'have.text',
            'Browser testing event'
          )
          cy.findByTestId('event-date-range').should(
            'have.text',
            'Data from: Jan 2020 - Nov 2020'
          )
          cy.findByTestId('event-link')
            .should('have.text', 'Open evaluator results')
            .and('have.attr', 'href', '/events/1')
        })

        // Event with more metadata
        cy.wrap(events[1]).within(() => {
          cy.findByTestId('event-header').should(
            'have.text',
            'Event two: EID/Matter #123456789'
          )
          cy.findByTestId('event-date-range').should(
            'have.text',
            'Data from: Nov 2019 - Nov 2020'
          )
          cy.findByTestId('event-link')
            .should('have.text', 'Open evaluator results')
            .and('have.attr', 'href', '/events/2')
        })
      })
  })
})
