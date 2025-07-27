import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
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
    const familyCodeButton = screen.getByRole('button', { name: /code famille/i })
    const localAccountButton = screen.getByRole('button', { name: /créer un compte local/i })
    
    expect(familyCodeButton).toBeInTheDocument()
    expect(localAccountButton).toBeInTheDocument()
  })

  it('displays email and username fields in local account mode', () => {
    render(<App />)
    
    // Click on local account mode
    const localAccountButton = screen.getByRole('button', { name: /créer un compte local/i })
    fireEvent.click(localAccountButton)
    
    // Check if email and username fields are present
    const emailField = screen.getByTestId('email')
    const usernameField = screen.getByTestId('username')
    
    expect(emailField).toBeInTheDocument()
    expect(usernameField).toBeInTheDocument()
  })

  it('renders without crashing', () => {
    // This is a smoke test - just ensure the component can render
    expect(() => render(<App />)).not.toThrow()
  })
})
