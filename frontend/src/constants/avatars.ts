/**
 * Predefined avatar gallery for user profile creation
 * Based on the BDD feature file examples
 */

export interface Avatar {
  id: string;
  emoji: string;
  label: string;
  type: string;
}

export const PREDEFINED_AVATARS: Avatar[] = [
  // Aventurier
  { id: 'adventurer-1', emoji: '🏄‍♂️', label: 'Aventurier Surf', type: 'Aventurier' },
  { id: 'adventurer-2', emoji: '🧗‍♂️', label: 'Aventurier Escalade', type: 'Aventurier' },
  { id: 'adventurer-3', emoji: '🏔️', label: 'Aventurier Montagne', type: 'Aventurier' },

  // Sportif  
  { id: 'sportif-1', emoji: '🏃‍♂️', label: 'Sportif Course', type: 'Sportif' },
  { id: 'sportif-2', emoji: '🚴‍♂️', label: 'Sportif Vélo', type: 'Sportif' },
  { id: 'sportif-3', emoji: '🏊‍♂️', label: 'Sportif Natation', type: 'Sportif' },

  // Photographe
  { id: 'photographe-1', emoji: '📸', label: 'Photographe Classique', type: 'Photographe' },
  { id: 'photographe-2', emoji: '🌺', label: 'Photographe Nature', type: 'Photographe' },
  { id: 'photographe-3', emoji: '🌸', label: 'Photographe Fleurs', type: 'Photographe' },

  // Explorateur
  { id: 'explorateur-1', emoji: '🗺️', label: 'Explorateur Carte', type: 'Explorateur' },
  { id: 'explorateur-2', emoji: '🧭', label: 'Explorateur Boussole', type: 'Explorateur' },
  { id: 'explorateur-3', emoji: '🔍', label: 'Explorateur Loupe', type: 'Explorateur' },

  // Gourmand
  { id: 'gourmand-1', emoji: '🍽️', label: 'Gourmand Restaurant', type: 'Gourmand' },
  { id: 'gourmand-2', emoji: '🥥', label: 'Gourmand Tropical', type: 'Gourmand' },
  { id: 'gourmand-3', emoji: '🍹', label: 'Gourmand Boisson', type: 'Gourmand' },

  // Famille
  { id: 'famille-1', emoji: '👨‍👩‍👧‍👦', label: 'Famille Complète', type: 'Famille' },
  { id: 'famille-2', emoji: '🎯', label: 'Famille Jeux', type: 'Famille' },
  { id: 'famille-3', emoji: '🌴', label: 'Famille Vacances', type: 'Famille' },
];

export const CHALLENGE_PREFERENCES = [
  { id: 'sport', label: 'Sport', emoji: '🏃‍♂️' },
  { id: 'culture', label: 'Culture', emoji: '🏛️' },
  { id: 'photo', label: 'Photographie', emoji: '📸' },
  { id: 'nature', label: 'Nature', emoji: '🌿' },
  { id: 'aventure', label: 'Aventure', emoji: '🗺️' },
  { id: 'gastronomie', label: 'Gastronomie', emoji: '🍽️' },
  { id: 'histoire', label: 'Histoire', emoji: '📚' },
  { id: 'famille', label: 'Famille', emoji: '👨‍👩‍👧‍👦' },
];

export const getAvatarById = (id: string): Avatar | undefined => {
  return PREDEFINED_AVATARS.find(avatar => avatar.id === id);
};

export const getAvatarsByType = (type: string): Avatar[] => {
  return PREDEFINED_AVATARS.filter(avatar => avatar.type === type);
};