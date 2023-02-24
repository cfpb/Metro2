describe('', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000');
  });

  it('displays a logo image', () => {
    cy.get('img').should(
      'have.attr',
      'src',
      '/static/images/logo_237x50@2x.png'
    );
  });
});
