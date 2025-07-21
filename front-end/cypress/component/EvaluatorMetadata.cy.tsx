import EvaluatorMetadataSection from '@src/pages/Evaluator/overview/components/Metadata'

describe('EvaluatorMetadataSection.cy.tsx', () => {
  it('should display all metadata fields', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      long_description: 'Long description of evaluator',
      rationale: 'This evaluator checks for a mismatch between two fields.',
      potential_harm: 'Description of potential harm.',
      alternate_explanation: 'Description of alternate explanation.',
      crrg_reference: 'Where to look in the CRRG.'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin />)
    cy.findByTestId('metadata-populated-fields')
      .should('be.visible')
      .within(() => {
        cy.get('li').should('have.length', 4)
        cy.get('li')
          .eq(0)
          .should('include.text', 'Rationale')
          .and('include.text', metadata.rationale)
        cy.get('li')
          .eq(1)
          .should('include.text', 'Potential harm')
          .and('include.text', metadata.potential_harm)
        cy.get('li')
          .eq(2)
          .should('include.text', 'Alternate explanation')
          .and('include.text', metadata.alternate_explanation)
        cy.get('li')
          .eq(3)
          .should('include.text', 'CRRG reference')
          .and('include.text', metadata.crrg_reference)
      })
    cy.findByTestId('metadata-contribute').should('not.exist')
  })

  it('should display partial metadata fields', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      long_description: 'Long description of evaluator',
      rationale: 'This evaluator checks for a mismatch between two fields.',
      crrg_reference: 'Where to look in the CRRG.'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin />)
    cy.findByTestId('metadata-populated-fields')
      .should('be.visible')
      .within(() => {
        cy.get('li').should('have.length', 2)
        cy.get('li')
          .eq(0)
          .should('include.text', 'Rationale')
          .and('include.text', metadata.rationale)
        cy.get('li')
          .eq(1)
          .should('include.text', 'CRRG reference')
          .and('include.text', metadata.crrg_reference)
      })
    cy.findByTestId('metadata-contribute').should('be.visible')
    cy.findByTestId('metadata-empty-fields')
      .should('be.visible')
      .within(() => {
        cy.get('li').should('have.length', 2)
        cy.get('li').eq(0).should('include.text', 'Potential harm')
        cy.get('li').eq(1).should('include.text', 'Alternate explanation')
      })
  })

  it('should display missing metadata fields', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      long_description: 'Long description of evaluator'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin />)
    cy.findByTestId('metadata-populated-fields').should('not.exist')
    cy.findByTestId('metadata-contribute').should('be.visible')
    cy.findByTestId('metadata-empty-fields')
      .should('be.visible')
      .within(() => {
        cy.get('li').should('have.length', 4)
        cy.get('li').eq(0).should('include.text', 'Rationale')
        cy.get('li').eq(1).should('include.text', 'Potential harm')
        cy.get('li').eq(2).should('include.text', 'Alternate explanation')
        cy.get('li').eq(3).should('include.text', 'CRRG reference')
      })
  })

  it('should display contribute call to action', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      long_description: 'Long description of evaluator',
      rationale: 'This evaluator checks for a mismatch between two fields.',
      crrg_reference: 'Where to look in the CRRG.'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin />)
    cy.findByTestId('metadata-contribute').should('be.visible')
    cy.findByTestId('metadata-cta').should('be.visible')
    cy.findByTestId('metadata-cta_general').should('be.visible')
    cy.findByTestId('metadata-cta_admin').should('be.visible')
  })

  it('should not show admin contribute call to action to non-admins', () => {
    const metadata = {
      id: 'test-eval',
      description: 'Description of evaluator',
      hits: 2222,
      accounts_affected: 1111,
      inconsistency_start: '1/1/24',
      inconsistency_end: '1/1/25',
      long_description: 'Long description of evaluator',
      rationale: 'This evaluator checks for a mismatch between two fields.',
      crrg_reference: 'Where to look in the CRRG.'
    }
    cy.mount(<EvaluatorMetadataSection metadata={metadata} isAdmin={false} />)
    cy.findByTestId('metadata-contribute').should('be.visible')
    cy.findByTestId('metadata-cta').should('be.visible')
    cy.findByTestId('metadata-cta_general').should('be.visible')
    cy.findByTestId('metadata-cta_admin').should('not.exist')
  })
})
