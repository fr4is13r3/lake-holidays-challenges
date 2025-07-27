import React, { useState } from 'react';
import { Check, ChevronDown, ChevronUp } from 'lucide-react';
import { PREDEFINED_AVATARS, CHALLENGE_PREFERENCES, Avatar, getAvatarById } from '../constants/avatars';
import { ProfileData } from '../types/profile';

interface ProfileData {
  display_name: string;
  avatar_url: string;
  age: number | null;
  challenge_preferences: Record<string, boolean>;
}

interface ProfileCreationProps {
  onSubmit: (profileData: ProfileData) => Promise<void>;
  onCancel?: () => void;
  initialData?: Partial<ProfileData>;
  isEdit?: boolean;
}

export const ProfileCreation: React.FC<ProfileCreationProps> = ({
  onSubmit,
  onCancel,
  initialData,
  isEdit = false
}) => {
  const [formData, setFormData] = useState<ProfileData>({
    display_name: initialData?.display_name || '',
    avatar_url: initialData?.avatar_url || '',
    age: initialData?.age || null,
    challenge_preferences: initialData?.challenge_preferences || {}
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showAvatarGallery, setShowAvatarGallery] = useState(false);
  const [selectedAvatarType, setSelectedAvatarType] = useState<string>('Tous');

  const avatarTypes = ['Tous', ...Array.from(new Set(PREDEFINED_AVATARS.map(avatar => avatar.type)))];

  const filteredAvatars = selectedAvatarType === 'Tous' 
    ? PREDEFINED_AVATARS 
    : PREDEFINED_AVATARS.filter(avatar => avatar.type === selectedAvatarType);

  const selectedAvatar = getAvatarById(formData.avatar_url);

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Pseudo obligatoire
    if (!formData.display_name.trim()) {
      newErrors.display_name = 'Le pseudo est obligatoire';
    } else if (formData.display_name.trim().length < 2) {
      newErrors.display_name = 'Le pseudo doit contenir au moins 2 caractères';
    } else if (formData.display_name.trim().length > 50) {
      newErrors.display_name = 'Le pseudo ne doit pas dépasser 50 caractères';
    }

    // Age validation (optional but if provided must be valid)
    if (formData.age !== null && (formData.age < 1 || formData.age > 150)) {
      newErrors.age = 'L\'âge doit être entre 1 et 150 ans';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Error submitting profile:', error);
      setErrors({ general: 'Erreur lors de la sauvegarde. Veuillez réessayer.' });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field: keyof ProfileData, value: string | number | null) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field as string]) {
      setErrors(prev => ({ ...prev, [field as string]: '' }));
    }
  };

  const handlePreferenceToggle = (preferenceId: string) => {
    setFormData(prev => ({
      ...prev,
      challenge_preferences: {
        ...prev.challenge_preferences,
        [preferenceId]: !prev.challenge_preferences[preferenceId]
      }
    }));
  };

  const handleAvatarSelect = (avatar: Avatar) => {
    handleInputChange('avatar_url', avatar.id);
    setShowAvatarGallery(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50 p-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            {isEdit ? 'Modifier mon profil' : 'Créer mon profil'}
          </h1>
          <p className="text-gray-600">
            Personnalisez votre profil pour une expérience unique
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* General Error */}
          {errors.general && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
              {errors.general}
            </div>
          )}

          {/* Pseudo Field */}
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <label className="block text-lg font-semibold text-gray-800 mb-3">
              Pseudo <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              data-testid="display-name"
              value={formData.display_name}
              onChange={(e) => handleInputChange('display_name', e.target.value)}
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-lg ${
                errors.display_name
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-300 focus:border-indigo-400'
              }`}
              placeholder="Papa Aventurier"
              maxLength={50}
            />
            {errors.display_name && (
              <p className="text-red-600 text-sm mt-2">{errors.display_name}</p>
            )}
            <p className="text-gray-500 text-sm mt-2">
              Votre nom d'affichage dans les défis familiaux
            </p>
          </div>

          {/* Avatar Selection */}
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <label className="block text-lg font-semibold text-gray-800 mb-3">
              Choisir un avatar
            </label>
            
            {/* Current Avatar Display */}
            <div 
              onClick={() => setShowAvatarGallery(!showAvatarGallery)}
              className="flex items-center justify-between p-4 border-2 border-gray-300 rounded-xl cursor-pointer hover:border-indigo-400 transition-colors"
            >
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-gradient-to-r from-indigo-400 to-purple-400 rounded-full flex items-center justify-center text-white text-2xl">
                  {selectedAvatar ? selectedAvatar.emoji : '👤'}
                </div>
                <div>
                  <div className="font-semibold text-gray-800">
                    {selectedAvatar ? selectedAvatar.label : 'Sélectionner un avatar'}
                  </div>
                  {selectedAvatar && (
                    <div className="text-sm text-gray-600">{selectedAvatar.type}</div>
                  )}
                </div>
              </div>
              {showAvatarGallery ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
            </div>

            {/* Avatar Gallery */}
            {showAvatarGallery && (
              <div className="mt-4 p-4 border border-gray-200 rounded-xl bg-gray-50">
                {/* Avatar Type Filter */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {avatarTypes.map(type => (
                    <button
                      key={type}
                      type="button"
                      onClick={() => setSelectedAvatarType(type)}
                      className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                        selectedAvatarType === type
                          ? 'bg-indigo-500 text-white'
                          : 'bg-white text-gray-600 hover:bg-gray-100'
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>

                {/* Avatar Grid */}
                <div className="grid grid-cols-4 sm:grid-cols-6 gap-3 max-h-64 overflow-y-auto">
                  {filteredAvatars.map(avatar => (
                    <button
                      key={avatar.id}
                      type="button"
                      onClick={() => handleAvatarSelect(avatar)}
                      className={`relative p-3 rounded-xl transition-all duration-200 hover:scale-105 ${
                        formData.avatar_url === avatar.id
                          ? 'bg-indigo-100 border-2 border-indigo-400'
                          : 'bg-white border-2 border-gray-200 hover:border-indigo-300'
                      }`}
                      title={avatar.label}
                    >
                      <div className="text-2xl">{avatar.emoji}</div>
                      {formData.avatar_url === avatar.id && (
                        <div className="absolute -top-1 -right-1 w-5 h-5 bg-indigo-500 rounded-full flex items-center justify-center">
                          <Check className="w-3 h-3 text-white" />
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Age Field */}
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <label className="block text-lg font-semibold text-gray-800 mb-3">
              Âge
            </label>
            <input
              type="number"
              data-testid="age"
              value={formData.age || ''}
              onChange={(e) => handleInputChange('age', e.target.value ? parseInt(e.target.value) : null)}
              className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-lg ${
                errors.age
                  ? 'border-red-300 focus:border-red-400'
                  : 'border-gray-300 focus:border-indigo-400'
              }`}
              placeholder="45"
              min="1"
              max="150"
            />
            {errors.age && (
              <p className="text-red-600 text-sm mt-2">{errors.age}</p>
            )}
            <p className="text-gray-500 text-sm mt-2">
              Pour adapter les défis à votre profil (optionnel)
            </p>
          </div>

          {/* Challenge Preferences */}
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <label className="block text-lg font-semibold text-gray-800 mb-3">
              Préférences de défis
            </label>
            <p className="text-gray-600 text-sm mb-4">
              Sélectionnez vos types de défis préférés
            </p>
            
            <div className="grid grid-cols-2 gap-3">
              {CHALLENGE_PREFERENCES.map(preference => (
                <button
                  key={preference.id}
                  type="button"
                  onClick={() => handlePreferenceToggle(preference.id)}
                  className={`flex items-center space-x-3 p-4 rounded-xl border-2 transition-all duration-200 ${
                    formData.challenge_preferences[preference.id]
                      ? 'bg-indigo-50 border-indigo-400 text-indigo-700'
                      : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-gray-300'
                  }`}
                >
                  <span className="text-xl">{preference.emoji}</span>
                  <span className="font-medium">{preference.label}</span>
                  {formData.challenge_preferences[preference.id] && (
                    <Check className="w-4 h-4 ml-auto" />
                  )}
                </button>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4 pt-4">
            {onCancel && (
              <button
                type="button"
                onClick={onCancel}
                className="flex-1 bg-gray-200 text-gray-700 py-4 rounded-2xl font-semibold text-lg hover:bg-gray-300 transition-colors"
              >
                Annuler
              </button>
            )}
            
            <button
              type="submit"
              disabled={isSubmitting}
              className={`flex-1 py-4 rounded-2xl font-semibold text-lg transition-all duration-200 transform hover:scale-105 ${
                isSubmitting
                  ? 'bg-gray-400 text-white cursor-not-allowed'
                  : 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:from-indigo-600 hover:to-purple-600'
              }`}
            >
              {isSubmitting 
                ? 'Enregistrement...' 
                : isEdit 
                  ? 'Mettre à jour' 
                  : 'Enregistrer le profil'
              }
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};