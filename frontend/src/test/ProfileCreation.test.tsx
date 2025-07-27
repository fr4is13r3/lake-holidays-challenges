import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ProfileCreation } from '../components/ProfileCreation';

describe('ProfileCreation Component', () => {
  const mockOnSubmit = async () => {};
  const mockOnCancel = () => {};

  it('should render profile creation form', () => {
    render(
      <ProfileCreation 
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByText('Créer mon profil')).toBeInTheDocument();
    expect(screen.getByTestId('display-name')).toBeInTheDocument();
    expect(screen.getByText('Choisir un avatar')).toBeInTheDocument();
    expect(screen.getByTestId('age')).toBeInTheDocument();
    expect(screen.getByText('Préférences de défis')).toBeInTheDocument();
  });

  it('should show validation error for empty pseudo', async () => {
    render(
      <ProfileCreation 
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const submitButton = screen.getByText('Enregistrer le profil');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Le pseudo est obligatoire')).toBeInTheDocument();
    });
  });

  it('should accept valid pseudo input', async () => {
    render(
      <ProfileCreation 
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    const nameInput = screen.getByTestId('display-name');
    fireEvent.change(nameInput, { target: { value: 'Papa Aventurier' } });

    expect(nameInput).toHaveValue('Papa Aventurier');
  });

  it('should display challenge preferences', () => {
    render(
      <ProfileCreation 
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByText('Sport')).toBeInTheDocument();
    expect(screen.getByText('Culture')).toBeInTheDocument();
    expect(screen.getByText('Photographie')).toBeInTheDocument();
    expect(screen.getByText('Nature')).toBeInTheDocument();
    expect(screen.getByText('Aventure')).toBeInTheDocument();
    expect(screen.getByText('Gastronomie')).toBeInTheDocument();
    expect(screen.getByText('Histoire')).toBeInTheDocument();
    expect(screen.getByText('Famille')).toBeInTheDocument();
  });

  it('should show edit mode when isEdit is true', () => {
    render(
      <ProfileCreation 
        onSubmit={mockOnSubmit}
        onCancel={mockOnCancel}
        isEdit={true}
      />
    );

    expect(screen.getByText('Modifier mon profil')).toBeInTheDocument();
    expect(screen.getByText('Mettre à jour')).toBeInTheDocument();
  });
});