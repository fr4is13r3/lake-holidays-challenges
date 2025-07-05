import { useState } from 'react';
import { User, MapPin, Trophy, Camera, Star, Home, Target, Plus } from 'lucide-react';

// Mock data for demonstration
const mockUser = {
  id: 1,
  name: "Sophie",
  age: 15,
  avatar: "🌺",
  points: 2850,
  dailyPoints: 125,
  streak: 5,
  badges: 12,
  rank: 2
};

const mockFamily = [
  { id: 1, name: "Papa", avatar: "🏄‍♂️", points: 3100, rank: 1 },
  { id: 2, name: "Sophie", avatar: "🌺", points: 2850, rank: 2 },
  { id: 3, name: "Maman", avatar: "🌸", points: 2750, rank: 3 },
  { id: 4, name: "Lucas", avatar: "🎯", points: 2200, rank: 4 }
];

const mockChallenges = [
  {
    id: 1,
    title: "Quiz Volcan",
    description: "Répondez aux questions sur le Piton de la Fournaise",
    type: "quiz",
    points: 50,
    timeLimit: 300,
    difficulty: "medium",
    location: "Piton de la Fournaise",
    completed: false
  },
  {
    id: 2,
    title: "Photo Caméléon",
    description: "Trouvez et photographiez un caméléon endémique",
    type: "photo",
    points: 75,
    difficulty: "hard",
    location: "Forêt de Bélouve",
    completed: false
  },
  {
    id: 3,
    title: "Défi Randonnée",
    description: "Atteignez le sommet en moins de 2h",
    type: "action",
    points: 100,
    timeLimit: 7200,
    difficulty: "hard",
    location: "Mafate",
    completed: true
  }
];

const mockPhotos = [
  {
    id: 1,
    url: "https://images.pexels.com/photos/1430931/pexels-photo-1430931.jpeg?auto=compress&cs=tinysrgb&w=800",
    author: "Papa",
    challenge: "Coucher de soleil",
    votes: 3,
    date: "2025-01-15"
  },
  {
    id: 2,
    url: "https://images.pexels.com/photos/1319270/pexels-photo-1319270.jpeg?auto=compress&cs=tinysrgb&w=800",
    author: "Sophie",
    challenge: "Faune locale",
    votes: 2,
    date: "2025-01-15"
  }
];

function App() {
  const [currentScreen, setCurrentScreen] = useState<'home' | 'challenges' | 'leaderboard' | 'photos' | 'profile'>('home');
  const [user, setUser] = useState<typeof mockUser>(mockUser);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  // Authentication state
  const [authMode, setAuthMode] = useState<'familyCode' | 'localAccount'>('familyCode');
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState<{[key: string]: string}>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validation functions
  const validateUsername = (username: string): string | null => {
    if (username.length < 3) return "Le nom d'utilisateur doit contenir au moins 3 caractères";
    if (username.length > 20) return "Le nom d'utilisateur ne doit pas dépasser 20 caractères";
    if (!/^[a-zA-Z0-9_-]+$/.test(username)) return "Le nom d'utilisateur ne peut contenir que des lettres, chiffres, _ et -";
    // Simulate uniqueness check (in real app, this would be an API call)
    const existingUsers = ['admin', 'test', 'user', 'famille'];
    if (existingUsers.includes(username.toLowerCase())) return "Ce nom d'utilisateur existe déjà";
    return null;
  };

  const validatePassword = (password: string): string | null => {
    if (password.length < 8) return "Le mot de passe doit contenir au moins 8 caractères";
    if (!/(?=.*[a-z])/.test(password)) return "Le mot de passe doit contenir au moins une minuscule";
    if (!/(?=.*[A-Z])/.test(password)) return "Le mot de passe doit contenir au moins une majuscule";
    if (!/(?=.*\d)/.test(password)) return "Le mot de passe doit contenir au moins un chiffre";
    if (!/(?=.*[!@#$%^&*(),.?":{}|<>])/.test(password)) return "Le mot de passe doit contenir au moins un caractère spécial";
    return null;
  };

  const validateForm = (): boolean => {
    const newErrors: {[key: string]: string} = {};
    
    const usernameError = validateUsername(formData.username);
    if (usernameError) newErrors.username = usernameError;
    
    const passwordError = validatePassword(formData.password);
    if (passwordError) newErrors.password = passwordError;
    
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Les mots de passe ne correspondent pas";
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleCreateAccount = async () => {
    if (!validateForm()) return;
    
    setIsSubmitting(true);
    
    // Simulate account creation API call
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Update user with new account info
      setUser({
        ...mockUser,
        name: formData.username,
        id: Date.now() // Simple ID generation
      });
      
      // Auto-login after account creation
      setIsAuthenticated(true);
    } catch {
      setErrors({ general: "Erreur lors de la création du compte. Veuillez réessayer." });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  // Authentication Screen
  const AuthScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-orange-400 via-red-400 to-pink-400 flex items-center justify-center p-4" data-testid="auth-form">
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🏝️</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Game Holidays</h1>
          <p className="text-gray-600">Gamifiez vos vacances à La Réunion</p>
        </div>

        {/* Mode Toggle */}
        <div className="flex bg-gray-100 rounded-2xl p-1 mb-6">
          <button
            onClick={() => setAuthMode('familyCode')}
            className={`flex-1 py-2 px-4 rounded-xl font-medium transition-all duration-200 ${
              authMode === 'familyCode'
                ? 'bg-white text-gray-800 shadow-sm'
                : 'text-gray-600'
            }`}
          >
            Code Famille
          </button>
          <button
            onClick={() => setAuthMode('localAccount')}
            className={`flex-1 py-2 px-4 rounded-xl font-medium transition-all duration-200 ${
              authMode === 'localAccount'
                ? 'bg-white text-gray-800 shadow-sm'
                : 'text-gray-600'
            }`}
          >
            Créer un compte local
          </button>
        </div>
        
        {authMode === 'familyCode' ? (
          // Family Code Mode
          <div className="space-y-4">
            <div className="text-center">
              <h2 className="text-xl font-semibold text-gray-700 mb-4">Code Famille</h2>
              <div className="flex justify-center space-x-3 mb-6">
                {[1,2,3,4,5,6].map(i => (
                  <input
                    key={i}
                    type="text"
                    maxLength={1}
                    className="w-12 h-12 border-2 border-gray-300 rounded-xl text-center text-xl font-bold focus:border-orange-400 focus:outline-none"
                  />
                ))}
              </div>
            </div>
            
            <button 
              onClick={() => setIsAuthenticated(true)}
              className="w-full bg-gradient-to-r from-orange-400 to-red-400 text-white py-4 rounded-2xl font-semibold text-lg hover:from-orange-500 hover:to-red-500 transition-all duration-200 transform hover:scale-105"
            >
              Se connecter
            </button>
            
            <button className="w-full border-2 border-gray-300 text-gray-700 py-4 rounded-2xl font-semibold text-lg hover:bg-gray-50 transition-all duration-200">
              Créer une famille
            </button>
          </div>
        ) : (
          // Local Account Creation Mode
          <div className="space-y-4">
            <div className="text-center mb-6">
              <h2 className="text-xl font-semibold text-gray-700">Créer un compte local</h2>
            </div>

            {/* General Error */}
            {errors.general && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl">
                {errors.general}
              </div>
            )}

            {/* Username Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nom d'utilisateur
              </label>
              <input
                type="text"
                data-testid="username"
                value={formData.username}
                onChange={(e) => handleInputChange('username', e.target.value)}
                className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors ${
                  errors.username
                    ? 'border-red-300 focus:border-red-400'
                    : 'border-gray-300 focus:border-orange-400'
                }`}
                placeholder="papa_vacances"
              />
              {errors.username && (
                <p className="text-red-600 text-sm mt-1">{errors.username}</p>
              )}
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Mot de passe
              </label>
              <input
                type="password"
                data-testid="password"
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors ${
                  errors.password
                    ? 'border-red-300 focus:border-red-400'
                    : 'border-gray-300 focus:border-orange-400'
                }`}
                placeholder="MonMotDePasse123!"
              />
              {errors.password && (
                <p className="text-red-600 text-sm mt-1">{errors.password}</p>
              )}
            </div>

            {/* Confirm Password Field */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Confirmer le mot de passe
              </label>
              <input
                type="password"
                data-testid="confirm-password"
                value={formData.confirmPassword}
                onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors ${
                  errors.confirmPassword
                    ? 'border-red-300 focus:border-red-400'
                    : 'border-gray-300 focus:border-orange-400'
                }`}
                placeholder="Confirmer votre mot de passe"
              />
              {errors.confirmPassword && (
                <p className="text-red-600 text-sm mt-1">{errors.confirmPassword}</p>
              )}
            </div>

            {/* Create Account Button */}
            <button
              onClick={handleCreateAccount}
              disabled={isSubmitting}
              className={`w-full py-4 rounded-2xl font-semibold text-lg transition-all duration-200 transform hover:scale-105 ${
                isSubmitting
                  ? 'bg-gray-400 text-white cursor-not-allowed'
                  : 'bg-gradient-to-r from-green-400 to-blue-400 text-white hover:from-green-500 hover:to-blue-500'
              }`}
            >
              {isSubmitting ? 'Création...' : 'Créer le compte'}
            </button>

            {/* Password Requirements */}
            <div className="bg-gray-50 rounded-xl p-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Exigences du mot de passe :</h4>
              <ul className="text-xs text-gray-600 space-y-1">
                <li>• Au moins 8 caractères</li>
                <li>• Une majuscule et une minuscule</li>
                <li>• Un chiffre</li>
                <li>• Un caractère spécial (!@#$%^&*...)</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );

  // Home Screen
  const HomeScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-orange-50">
      {/* Header */}
      <div className="bg-white shadow-lg rounded-b-3xl p-6 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-gradient-to-r from-orange-400 to-red-400 rounded-full flex items-center justify-center text-white text-2xl">
              {user.avatar}
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-800">Bonjour {user.name} !</h1>
              <p className="text-gray-600">Jour 6 • Série de {user.streak} jours</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-orange-500">{user.points}</div>
            <div className="text-sm text-gray-600">points</div>
          </div>
        </div>
      </div>

      {/* Daily Progress */}
      <div className="px-6 mb-6">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-gray-800">Progression du jour</h2>
            <div className="text-sm text-orange-500 font-semibold">+{user.dailyPoints} pts</div>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
            <div className="bg-gradient-to-r from-orange-400 to-red-400 h-3 rounded-full" style={{width: '65%'}}></div>
          </div>
          <div className="flex justify-between text-sm text-gray-600">
            <span>3/5 défis terminés</span>
            <span>65%</span>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="px-6 mb-6">
        <div className="grid grid-cols-2 gap-4">
          <button 
            onClick={() => setCurrentScreen('challenges')}
            className="bg-gradient-to-r from-purple-400 to-pink-400 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            <Target className="w-8 h-8 mb-2" />
            <div className="font-semibold">Défis</div>
            <div className="text-sm opacity-90">2 disponibles</div>
          </button>
          
          <button 
            onClick={() => setCurrentScreen('leaderboard')}
            className="bg-gradient-to-r from-yellow-400 to-orange-400 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            <Trophy className="w-8 h-8 mb-2" />
            <div className="font-semibold">Classement</div>
            <div className="text-sm opacity-90">#{user.rank}</div>
          </button>
        </div>
      </div>

      {/* Today's Activity */}
      <div className="px-6 mb-6">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-gray-800">Activité du jour</h2>
            <MapPin className="w-5 h-5 text-gray-500" />
          </div>
          <div className="bg-gradient-to-r from-green-100 to-blue-100 rounded-xl p-4">
            <div className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white">
                🌋
              </div>
              <div>
                <div className="font-semibold text-gray-800">Piton de la Fournaise</div>
                <div className="text-sm text-gray-600">Randonnée volcanique</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Photos */}
      <div className="px-6 mb-20">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-gray-800">Photos récentes</h2>
          <button 
            onClick={() => setCurrentScreen('photos')}
            className="text-orange-500 font-semibold"
          >
            Voir tout
          </button>
        </div>
        <div className="flex space-x-4 overflow-x-auto pb-2">
          {mockPhotos.map(photo => (
            <div key={photo.id} className="flex-shrink-0 w-32 h-32 rounded-xl overflow-hidden shadow-lg">
              <img 
                src={photo.url} 
                alt={photo.challenge}
                className="w-full h-full object-cover"
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Challenges Screen
  const ChallengesScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <div className="bg-white shadow-lg rounded-b-3xl p-6 mb-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-800">Défis du jour</h1>
          <div className="bg-purple-100 text-purple-600 px-3 py-1 rounded-full text-sm font-semibold">
            3 défis
          </div>
        </div>
        <p className="text-gray-600 mt-2">Piton de la Fournaise • 16 Janvier 2025</p>
      </div>

      <div className="px-6 space-y-4 mb-20">
        {mockChallenges.map(challenge => (
          <div key={challenge.id} className="bg-white rounded-2xl p-6 shadow-lg">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center text-white ${
                  challenge.type === 'quiz' ? 'bg-blue-500' :
                  challenge.type === 'photo' ? 'bg-green-500' : 'bg-orange-500'
                }`}>
                  {challenge.type === 'quiz' ? '🧠' : 
                   challenge.type === 'photo' ? '📸' : '🎯'}
                </div>
                <div>
                  <h3 className="font-bold text-gray-800">{challenge.title}</h3>
                  <p className="text-sm text-gray-600">{challenge.description}</p>
                </div>
              </div>
              <div className="text-right">
                <div className="text-lg font-bold text-orange-500">{challenge.points}</div>
                <div className="text-xs text-gray-500">points</div>
              </div>
            </div>
            
            <div className="flex items-center justify-between">
              <div className="flex space-x-2">
                <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                  challenge.difficulty === 'easy' ? 'bg-green-100 text-green-600' :
                  challenge.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-600' :
                  'bg-red-100 text-red-600'
                }`}>
                  {challenge.difficulty === 'easy' ? 'Facile' :
                   challenge.difficulty === 'medium' ? 'Moyen' : 'Difficile'}
                </span>
                {challenge.timeLimit && (
                  <span className="px-2 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-600">
                    {challenge.timeLimit > 3600 ? `${Math.floor(challenge.timeLimit/3600)}h` : `${Math.floor(challenge.timeLimit/60)}min`}
                  </span>
                )}
              </div>
              
              <button className={`px-6 py-2 rounded-full font-semibold text-sm transition-all duration-200 ${
                challenge.completed 
                  ? 'bg-green-100 text-green-600 cursor-not-allowed'
                  : 'bg-gradient-to-r from-purple-400 to-pink-400 text-white hover:from-purple-500 hover:to-pink-500 transform hover:scale-105'
              }`}>
                {challenge.completed ? 'Terminé ✓' : 'Commencer'}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  // Leaderboard Screen
  const LeaderboardScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50">
      <div className="bg-white shadow-lg rounded-b-3xl p-6 mb-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Classement</h1>
        <p className="text-gray-600">Famille Dupont • Jour 6</p>
      </div>

      <div className="px-6 mb-6">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Classement général</h2>
          <div className="space-y-4">
            {mockFamily.map((member, index) => (
              <div key={member.id} className="flex items-center space-x-4">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-white ${
                  index === 0 ? 'bg-yellow-500' :
                  index === 1 ? 'bg-gray-400' :
                  index === 2 ? 'bg-orange-600' : 'bg-gray-300'
                }`}>
                  {index + 1}
                </div>
                <div className="w-12 h-12 bg-gradient-to-r from-orange-400 to-red-400 rounded-full flex items-center justify-center text-white text-xl">
                  {member.avatar}
                </div>
                <div className="flex-1">
                  <div className="font-semibold text-gray-800">{member.name}</div>
                  <div className="text-sm text-gray-600">{member.points} points</div>
                </div>
                {index === 0 && <Trophy className="w-6 h-6 text-yellow-500" />}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="px-6 mb-6">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Statistiques</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-blue-50 rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-blue-600">28</div>
              <div className="text-sm text-blue-600">Défis terminés</div>
            </div>
            <div className="bg-green-50 rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-green-600">15</div>
              <div className="text-sm text-green-600">Photos partagées</div>
            </div>
            <div className="bg-purple-50 rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-purple-600">12</div>
              <div className="text-sm text-purple-600">Badges obtenus</div>
            </div>
            <div className="bg-orange-50 rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-orange-600">6</div>
              <div className="text-sm text-orange-600">Jours consécutifs</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Photos Screen
  const PhotosScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <div className="bg-white shadow-lg rounded-b-3xl p-6 mb-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-800">Album famille</h1>
          <button className="bg-gradient-to-r from-green-400 to-blue-400 text-white p-3 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200">
            <Plus className="w-6 h-6" />
          </button>
        </div>
        <p className="text-gray-600 mt-2">47 photos • Vote photo du jour</p>
      </div>

      <div className="px-6 mb-6">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Photo du jour</h2>
          <div className="bg-gradient-to-r from-yellow-100 to-orange-100 rounded-xl p-4">
            <div className="text-center">
              <div className="text-4xl mb-2">📸</div>
              <div className="font-semibold text-gray-800">Votez pour votre photo préférée</div>
              <div className="text-sm text-gray-600">Résultats à 20h</div>
            </div>
          </div>
        </div>
      </div>

      <div className="px-6 mb-20">
        <div className="grid grid-cols-2 gap-4">
          {mockPhotos.map(photo => (
            <div key={photo.id} className="bg-white rounded-2xl overflow-hidden shadow-lg">
              <img 
                src={photo.url} 
                alt={photo.challenge}
                className="w-full h-48 object-cover"
              />
              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="font-semibold text-gray-800 text-sm">{photo.challenge}</div>
                  <div className="flex items-center space-x-1">
                    <Star className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="text-sm text-gray-600">{photo.votes}</span>
                  </div>
                </div>
                <div className="text-xs text-gray-500">Par {photo.author}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  // Profile Screen
  const ProfileScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-50">
      <div className="bg-white shadow-lg rounded-b-3xl p-6 mb-6">
        <div className="text-center">
          <div className="w-24 h-24 bg-gradient-to-r from-indigo-400 to-purple-400 rounded-full flex items-center justify-center text-white text-4xl mx-auto mb-4">
            {user.avatar}
          </div>
          <h1 className="text-2xl font-bold text-gray-800">{user.name}</h1>
          <p className="text-gray-600">{user.age} ans • Famille Dupont</p>
        </div>
      </div>

      <div className="px-6 space-y-6 mb-20">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Mes statistiques</h2>
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-indigo-600">{user.points}</div>
              <div className="text-sm text-gray-600">Points totaux</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{user.badges}</div>
              <div className="text-sm text-gray-600">Badges</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{user.streak}</div>
              <div className="text-sm text-gray-600">Série (jours)</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">#{user.rank}</div>
              <div className="text-sm text-gray-600">Classement</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Badges récents</h2>
          <div className="grid grid-cols-3 gap-4">
            {['🏆', '📸', '🌋', '🎯', '⭐', '🔥'].map((badge, index) => (
              <div key={index} className="bg-gradient-to-r from-yellow-100 to-orange-100 rounded-xl p-4 text-center">
                <div className="text-2xl mb-1">{badge}</div>
                <div className="text-xs text-gray-600">Badge</div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Paramètres</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Notifications</span>
              <div className="w-12 h-6 bg-indigo-500 rounded-full relative">
                <div className="w-5 h-5 bg-white rounded-full absolute right-0.5 top-0.5"></div>
              </div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-700">Mode hors-ligne</span>
              <div className="w-12 h-6 bg-gray-300 rounded-full relative">
                <div className="w-5 h-5 bg-white rounded-full absolute left-0.5 top-0.5"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  // Bottom Navigation
  const BottomNavigation = () => (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-4">
      <div className="flex justify-around">
        {[
          { id: 'home', icon: Home, label: 'Accueil' },
          { id: 'challenges', icon: Target, label: 'Défis' },
          { id: 'leaderboard', icon: Trophy, label: 'Classement' },
          { id: 'photos', icon: Camera, label: 'Photos' },
          { id: 'profile', icon: User, label: 'Profil' }
        ].map(item => (
          <button
            key={item.id}
            onClick={() => setCurrentScreen(item.id)}
            className={`flex flex-col items-center space-y-1 p-2 rounded-xl transition-all duration-200 ${
              currentScreen === item.id 
                ? 'bg-orange-100 text-orange-600' 
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <item.icon className="w-6 h-6" />
            <span className="text-xs font-medium">{item.label}</span>
          </button>
        ))}
      </div>
    </div>
  );

  if (!isAuthenticated) {
    return <AuthScreen />;
  }

  return (
    <div className="pb-20">
      {currentScreen === 'home' && <HomeScreen />}
      {currentScreen === 'challenges' && <ChallengesScreen />}
      {currentScreen === 'leaderboard' && <LeaderboardScreen />}
      {currentScreen === 'photos' && <PhotosScreen />}
      {currentScreen === 'profile' && <ProfileScreen />}
      <BottomNavigation />
    </div>
  );
}

export default App;