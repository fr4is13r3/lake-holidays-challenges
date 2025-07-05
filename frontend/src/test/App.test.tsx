import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

describe('App Component', () => {
  it('renders authentication form by default', () => {
    render(<App />)
    
    // Check if auth form is rendered (app starts unauthenticated)
    const authForm = screen.getByTestId('auth-form')
    expect(authForm).toBeInTheDocument()
  })

  it('displays the app title', () => {
    render(<App />)
    
    // Check if the main title is present
    const title = screen.getByText('Game Holidays')
    expect(title).toBeInTheDocument()
  })

  it('displays authentication mode toggle buttons', () => {
    render(<App />)
    
    // Check if both auth mode buttons are present
    const familyCodeButton = screen.getByText('Code Famille')
    const localAccountButton = screen.getByText('Créer un compte local')
    
    expect(familyCodeButton).toBeInTheDocument()
    expect(localAccountButton).toBeInTheDocument()
  })

  it('renders without crashing', () => {
    // This is a smoke test - just ensure the component can render
    expect(() => render(<App />)).not.toThrow()
  })
})
