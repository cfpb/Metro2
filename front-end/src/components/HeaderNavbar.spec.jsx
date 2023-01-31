import { describe, test } from 'vitest';
import { render, screen } from '@testing-library/react';
import HeaderNavbar from './HeaderNavbar';

describe('Header test', () => {
  test('Should show logo', () => {
    render(<HeaderNavbar />);
    const logo = screen.getByRole('img');
    expect(logo).toHaveAttribute('src', '/static/images/logo_237x50@2x.png');
  });
});
