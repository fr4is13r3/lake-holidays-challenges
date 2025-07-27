import React, { useState, useEffect } from 'react';
import { User, MapPin, Trophy, Camera, Star, Home, Target, Plus, Calendar,  Clock, HelpCircle, Upload, MapPin as LocationIcon, X, CheckCircle, XCircle } from 'lucide-react';

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
    completed: false,
    content: {
      questions: [
        {
          question: "Quel est l'épice emblématique de la cuisine créole ?",
          options: ["Poivre", "Curcuma", "Paprika", "Gingembre"],
          correct_answer: 1,
          hint: "Cette épice donne une couleur dorée aux plats créoles"
        },
        {
          question: "Quelle est la hauteur approximative du Piton de la Fournaise ?",
          options: ["2631m", "3071m", "2000m", "4000m"],
          correct_answer: 0,
          hint: "Le point culminant fait plus de 2600 mètres"
        },
        {
          question: "Comment appelle-t-on la dernière éruption en date ?",
          options: ["Cratère Dolomieu", "Cratère Bory", "Enclos Fouqué", "Pas de Bellecombe"],
          correct_answer: 2,
          hint: "C'est le nom de l'enceinte où se produisent la plupart des éruptions"
        }
      ],
      time_limit: 30
    }
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
  const [currentScreen, setCurrentScreen] = useState<'home' | 'challenges' | 'leaderboard' | 'photos' | 'profile' | 'seasons'>('home');
  const [user, setUser] = useState<typeof mockUser>(mockUser);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isHandlingOAuth, setIsHandlingOAuth] = useState<boolean>(false);


  // Quiz types
  interface QuizQuestion {
    question: string;
    options: string[];
    correct_answer: number;
    hint: string;
  }

  interface QuizChallenge {
    id: number;
    title: string;
    content: {
      questions: QuizQuestion[];
      time_limit: number;
    };
    points: number;
  }

  interface QuizResult {
    correct_count: number;
    total_questions: number;
    percentage: number;
    points_awarded: number;
    hints_used: number;
    time_taken: number;
    feedback_message: string;
    detailed_results: Array<{
      question_index: number;
      question: string;
      selected_answer: number;
      correct_answer: number;
      is_correct: boolean;
      options: string[];
    }>;
  }

  // Quiz state
  const [activeQuiz, setActiveQuiz] = useState<QuizChallenge | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<number[]>([]);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [showHint, setShowHint] = useState(false);
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);
  const [startTime, setStartTime] = useState<number>(0);

  // Season creation state
  const [showSeasonForm, setShowSeasonForm] = useState<boolean>(false);
  const [seasonFormData, setSeasonFormData] = useState({
    title: '',
    description: '',
    location: '',
    start_date: '',
    end_date: '',
    cover_image: null as File | null
  });
  const [seasonErrors, setSeasonErrors] = useState<{[key: string]: string}>({});
  const [isCreatingSeason, setIsCreatingSeason] = useState<boolean>(false);
  const [createdSeason, setCreatedSeason] = useState<any>(null);

  // Check for OAuth callback on component mount
  React.useEffect(() => {
    const handleOAuthCallback = async () => {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      const state = urlParams.get('state');
      const error = urlParams.get('error');
      
      if (error) {
        setErrors({ general: `Erreur OAuth: ${error}` });
        // Clean URL
        window.history.replaceState({}, document.title, window.location.pathname);
        return;
      }
      
      if (code && state && (state === 'google' || state === 'microsoft')) {
        setIsHandlingOAuth(true);
        
        try {
          const redirectUri = `${window.location.origin}/auth/callback`;
          
          const response = await fetch(`http://localhost:8000/auth/oauth/${state}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              provider: state,
              code: code,
              redirect_uri: redirectUri
            }),
          });
          
          if (!response.ok) {
            throw new Error(`OAuth authentication failed`);
          }
          
          const tokenData = await response.json();
          
          // Update user with OAuth data
          setUser({
            ...mockUser,
            name: tokenData.username || tokenData.email,
            id: tokenData.user_id
          });
          
          // Set authenticated
          setIsAuthenticated(true);
          
          // Clean URL
          window.history.replaceState({}, document.title, window.location.pathname);
          
        } catch (error) {
          console.error('OAuth callback error:', error);
          setErrors({ general: `Erreur lors de la connexion OAuth. Veuillez réessayer.` });
          // Clean URL
          window.history.replaceState({}, document.title, window.location.pathname);
        } finally {
          setIsHandlingOAuth(false);
        }
      }
    };
    
    handleOAuthCallback();
  }, []);

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

  const handleOAuthLogin = async (provider: 'google' | 'microsoft') => {
    try {
      const redirectUri = `${window.location.origin}/auth/callback`;
      
      // Get OAuth authorization URL from backend
      const response = await fetch(`http://localhost:8000/auth/oauth/${provider}/url?redirect_uri=${encodeURIComponent(redirectUri)}&state=${provider}`);
      
      if (!response.ok) {
        throw new Error(`Failed to get ${provider} OAuth URL`);
      }
      
      const data = await response.json();
      
      // Redirect to OAuth provider
      window.location.href = data.auth_url;
      
    } catch (error) {
      console.error(`${provider} OAuth error:`, error);
      setErrors({ general: `Erreur lors de la connexion avec ${provider === 'google' ? 'Google' : 'Microsoft'}. Veuillez réessayer.` });
    }
  };

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };


  // Quiz Functions
  const startQuiz = (challenge: QuizChallenge) => {
    setActiveQuiz(challenge);
    setCurrentQuestionIndex(0);
    setSelectedAnswers([]);
    setTimeRemaining(challenge.content.time_limit * challenge.content.questions.length);
    setHintsUsed(0);
    setShowHint(false);
    setQuizResult(null);
    setStartTime(Date.now());
  };

  const closeQuiz = () => {
    setActiveQuiz(null);
    setCurrentQuestionIndex(0);
    setSelectedAnswers([]);
    setTimeRemaining(0);
    setHintsUsed(0);
    setShowHint(false);
    setQuizResult(null);
    setStartTime(0);
  };

  const selectAnswer = (answerIndex: number) => {
    const newAnswers = [...selectedAnswers];
    newAnswers[currentQuestionIndex] = answerIndex;
    setSelectedAnswers(newAnswers);
  };

  const useHint = () => {
    setHintsUsed(prev => prev + 1);
    setShowHint(true);
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < activeQuiz.content.questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setShowHint(false);
    } else {
      submitQuiz();
    }
  };

  const submitQuiz = React.useCallback(async () => {
    if (!activeQuiz) return;

    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    
    // Simulate quiz submission (in real app, this would be an API call)
    const questions = activeQuiz.content.questions;
    let correctCount = 0;
    const detailedResults = selectedAnswers.map((answer, index) => {
      const question = questions[index];
      const isCorrect = answer === question.correct_answer;
      if (isCorrect) correctCount++;
      
      return {
        question_index: index,
        question: question.question,
        selected_answer: answer,
        correct_answer: question.correct_answer,
        is_correct: isCorrect,
        options: question.options
      };
    });

    // Calculate points
    const basePoints = activeQuiz.points;
    const pointsPerQuestion = Math.floor(basePoints / questions.length);
    let earnedPoints = correctCount * pointsPerQuestion;

    // Apply hint penalty
    if (hintsUsed > 0) {
      earnedPoints = Math.floor(earnedPoints * Math.max(0, 1 - (0.5 * hintsUsed)));
    }

    const percentage = (correctCount / questions.length) * 100;
    let feedbackMessage = '';
    
    if (percentage === 100) {
      feedbackMessage = hintsUsed === 0 
        ? `Parfait ! Vous avez tout bon sans aide ! +${earnedPoints} points 🎉`
        : `Excellent ! Toutes les bonnes réponses ! +${earnedPoints} points ⭐`;
    } else if (percentage >= 80) {
      feedbackMessage = `Très bien ! ${percentage.toFixed(0)}% de bonnes réponses. +${earnedPoints} points 👏`;
    } else if (percentage >= 60) {
      feedbackMessage = `Bien joué ! ${percentage.toFixed(0)}% de réussite. +${earnedPoints} points 👍`;
    } else if (percentage >= 40) {
      feedbackMessage = `Pas mal ! ${percentage.toFixed(0)}% de bonnes réponses. +${earnedPoints} points 📚`;
    } else {
      feedbackMessage = `Continue tes efforts ! ${percentage.toFixed(0)}% cette fois. +${earnedPoints} points 💪`;
    }

    setQuizResult({
      correct_count: correctCount,
      total_questions: questions.length,
      percentage,
      points_awarded: earnedPoints,
      hints_used: hintsUsed,
      time_taken: timeTaken,
      feedback_message: feedbackMessage,
      detailed_results: detailedResults
    });

    // Update user points
    setUser(prev => ({
      ...prev,
      points: prev.points + earnedPoints,
      dailyPoints: prev.dailyPoints + earnedPoints
    }));
  }, [activeQuiz, startTime, selectedAnswers, hintsUsed, setUser]);

  // Timer effect
  useEffect(() => {
    if (activeQuiz && timeRemaining > 0 && !quizResult) {
      const timer = setTimeout(() => {
        setTimeRemaining(prev => prev - 1);
      }, 1000);
      
      return () => clearTimeout(timer);
    } else if (timeRemaining === 0 && activeQuiz && !quizResult) {
      // Time's up, auto-submit
      submitQuiz();
    }
  }, [timeRemaining, activeQuiz, quizResult, submitQuiz]);

  // Quiz Modal Component
  const QuizModal = () => {
    if (!activeQuiz) return null;

    const currentQuestion = activeQuiz.content.questions[currentQuestionIndex];
    const isLastQuestion = currentQuestionIndex === activeQuiz.content.questions.length - 1;
    const hasSelectedAnswer = selectedAnswers[currentQuestionIndex] !== undefined;

    if (quizResult) {
      // Quiz Results Screen
      return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-3xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
            <div className="text-center mb-6">
              <div className="text-6xl mb-4">
                {quizResult.percentage === 100 ? '🎉' : quizResult.percentage >= 80 ? '🌟' : 
                 quizResult.percentage >= 60 ? '👏' : '📚'}
              </div>
              <h2 className="text-2xl font-bold text-gray-800 mb-2">Quiz terminé !</h2>
              <p className="text-lg text-gray-600">{quizResult.feedback_message}</p>
            </div>

            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-4 mb-6">
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {quizResult.correct_count}/{quizResult.total_questions}
                  </div>
                  <div className="text-sm text-gray-600">Bonnes réponses</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-purple-600">{quizResult.points_awarded}</div>
                  <div className="text-sm text-gray-600">Points gagnés</div>
                </div>
                <div>
                  <div className="text-lg font-semibold text-orange-600">{quizResult.hints_used}</div>
                  <div className="text-sm text-gray-600">Indices utilisés</div>
                </div>
                <div>
                  <div className="text-lg font-semibold text-green-600">{quizResult.time_taken}s</div>
                  <div className="text-sm text-gray-600">Temps pris</div>
                </div>
              </div>
            </div>

            <div className="space-y-3 mb-6">
              <h3 className="font-bold text-gray-800">Détail des réponses :</h3>
              {quizResult.detailed_results.map((result, index: number) => (
                <div key={index} className="bg-gray-50 rounded-xl p-3">
                  <div className="flex items-start space-x-2 mb-2">
                    {result.is_correct ? (
                      <CheckCircle className="w-5 h-5 text-green-500 mt-0.5" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-500 mt-0.5" />
                    )}
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-800">{result.question}</p>
                      <p className={`text-sm ${result.is_correct ? 'text-green-600' : 'text-red-600'}`}>
                        Votre réponse: {result.options[result.selected_answer]}
                      </p>
                      {!result.is_correct && (
                        <p className="text-sm text-green-600">
                          Bonne réponse: {result.options[result.correct_answer]}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <button
              onClick={closeQuiz}
              className="w-full bg-gradient-to-r from-green-400 to-blue-400 text-white py-4 rounded-2xl font-semibold text-lg hover:from-green-500 hover:to-blue-500 transition-all duration-200"
            >
              Continuer
            </button>
          </div>
        </div>
      );
    }

    // Quiz Question Screen
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-3xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-bold text-gray-800">{activeQuiz.title}</h2>
              <p className="text-sm text-gray-600">
                Question {currentQuestionIndex + 1} sur {activeQuiz.content.questions.length}
              </p>
            </div>
            <button onClick={closeQuiz} className="text-gray-400 hover:text-gray-600">
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Timer */}
          <div className="flex items-center justify-center mb-6">
            <div className="bg-gradient-to-r from-orange-100 to-red-100 rounded-full px-4 py-2 flex items-center space-x-2">
              <Clock className="w-5 h-5 text-orange-600" />
              <span className={`font-bold ${timeRemaining <= 10 ? 'text-red-600' : 'text-orange-600'}`}>
                {Math.floor(timeRemaining / 60)}:{(timeRemaining % 60).toString().padStart(2, '0')}
              </span>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2 mb-6">
            <div 
              className="bg-gradient-to-r from-blue-400 to-purple-400 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentQuestionIndex + 1) / activeQuiz.content.questions.length) * 100}%` }}
            ></div>
          </div>

          {/* Question */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              {currentQuestion.question}
            </h3>

            {/* Hint */}
            {showHint && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-3 mb-4">
                <div className="flex items-center space-x-2">
                  <HelpCircle className="w-5 h-5 text-yellow-600" />
                  <span className="text-sm font-medium text-yellow-800">Indice :</span>
                </div>
                <p className="text-sm text-yellow-700 mt-1">{currentQuestion.hint}</p>
              </div>
            )}

            {/* Answer Options */}
            <div className="space-y-3">
              {currentQuestion.options.map((option: string, index: number) => (
                <button
                  key={index}
                  onClick={() => selectAnswer(index)}
                  className={`w-full text-left p-4 border-2 rounded-xl transition-all duration-200 ${
                    selectedAnswers[currentQuestionIndex] === index
                      ? 'border-blue-400 bg-blue-50 text-blue-800'
                      : 'border-gray-200 hover:border-gray-300 text-gray-700'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                      selectedAnswers[currentQuestionIndex] === index
                        ? 'border-blue-400 bg-blue-400'
                        : 'border-gray-300'
                    }`}>
                      {selectedAnswers[currentQuestionIndex] === index && (
                        <div className="w-2 h-2 bg-white rounded-full"></div>
                      )}
                    </div>
                    <span className="font-medium">{option}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex space-x-3">
            {!showHint && (
              <button
                onClick={useHint}
                className="flex-1 bg-yellow-100 text-yellow-700 py-3 rounded-xl font-semibold hover:bg-yellow-200 transition-all duration-200 flex items-center justify-center space-x-2"
              >
                <HelpCircle className="w-5 h-5" />
                <span>Indice</span>
              </button>
            )}
            
            <button
              onClick={nextQuestion}
              disabled={!hasSelectedAnswer}
              className={`flex-1 py-3 rounded-xl font-semibold transition-all duration-200 ${
                hasSelectedAnswer
                  ? 'bg-gradient-to-r from-blue-400 to-purple-400 text-white hover:from-blue-500 hover:to-purple-500'
                  : 'bg-gray-200 text-gray-400 cursor-not-allowed'
              }`}
            >
              {isLastQuestion ? 'Terminer' : 'Suivant'}
            </button>
          </div>
        </div>
      </div>
    );

  // Season validation functions
  const validateSeasonTitle = (title: string): string | null => {
    if (!title.trim()) return "Le titre de la saison est obligatoire";
    if (title.length < 3) return "Le titre doit contenir au moins 3 caractères";
    if (title.length > 200) return "Le titre ne doit pas dépasser 200 caractères";
    return null;
  };

  const validateSeasonDates = (startDate: string, endDate: string): string | null => {
    if (!startDate) return "La date de début est obligatoire";
    if (!endDate) return "La date de fin est obligatoire";
    
    const start = new Date(startDate + "T00:00:00");
    const end = new Date(endDate + "T00:00:00");
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (start < today) return "La saison ne peut pas être dans le passé";
    if (end <= start) return "La date de fin doit être après le début";
    
    return null;
  };

  const validateSeasonLocation = (location: string): string | null => {
    if (!location.trim()) return "La localisation est obligatoire";
    if (location.length < 3) return "La localisation doit contenir au moins 3 caractères";
    if (location.length > 200) return "La localisation ne doit pas dépasser 200 caractères";
    return null;
  };

  const validateSeasonForm = (): boolean => {
    const newErrors: {[key: string]: string} = {};
    
    const titleError = validateSeasonTitle(seasonFormData.title);
    if (titleError) newErrors.title = titleError;
    
    const locationError = validateSeasonLocation(seasonFormData.location);
    if (locationError) newErrors.location = locationError;
    
    const dateError = validateSeasonDates(seasonFormData.start_date, seasonFormData.end_date);
    if (dateError) newErrors.dates = dateError;
    
    setSeasonErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSeasonInputChange = (field: string, value: string | File | null) => {
    setSeasonFormData(prev => ({ ...prev, [field]: value }));
    // Clear error when user starts typing
    if (seasonErrors[field]) {
      setSeasonErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  const handleCreateSeason = async () => {
    if (!validateSeasonForm()) return;
    
    setIsCreatingSeason(true);
    
    try {
      // Prepare form data for backend
      const formData = new FormData();
      formData.append('title', seasonFormData.title);
      formData.append('description', seasonFormData.description);
      formData.append('location', seasonFormData.location);
      formData.append('start_date', seasonFormData.start_date);
      formData.append('end_date', seasonFormData.end_date);
      if (seasonFormData.cover_image) {
        formData.append('cover_image', seasonFormData.cover_image);
      }
      
      // Create season via backend API
      const response = await fetch('http://localhost:8000/seasons/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: seasonFormData.title,
          description: seasonFormData.description,
          location: seasonFormData.location,
          start_date: new Date(seasonFormData.start_date).toISOString(),
          end_date: new Date(seasonFormData.end_date).toISOString(),
          latitude: null,
          longitude: null,
          cover_image_url: null,
          is_active: false,
          max_members: null
        }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Erreur lors de la création de la saison');
      }
      
      const seasonData = await response.json();
      setCreatedSeason(seasonData);
      
      // Reset form
      setSeasonFormData({
        title: '',
        description: '',
        location: '',
        start_date: '',
        end_date: '',
        cover_image: null
      });
      setShowSeasonForm(false);
      
    } catch (error) {
      console.error('Season creation error:', error);
      setSeasonErrors({ general: `Erreur lors de la création de la saison: ${error.message}` });
    } finally {
      setIsCreatingSeason(false);
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

        {/* OAuth Processing */}
        {isHandlingOAuth && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
            <p className="text-gray-600">Connexion en cours...</p>
          </div>
        )}

        {/* Normal Auth UI */}
        {!isHandlingOAuth && (
          <>
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

        {/* OAuth Buttons - Always visible */}
        <div className="mt-6 space-y-3">
          <div className="text-center text-sm text-gray-500 mb-4">
            Ou se connecter avec
          </div>
          
          <button 
            onClick={() => handleOAuthLogin('google')}
            className="w-full flex items-center justify-center space-x-3 border-2 border-gray-300 text-gray-700 py-3 rounded-2xl font-semibold hover:bg-gray-50 transition-all duration-200"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285f4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34a853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#fbbc05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#ea4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            <span>Se connecter avec Google</span>
          </button>
          
          <button 
            onClick={() => handleOAuthLogin('microsoft')}
            className="w-full flex items-center justify-center space-x-3 border-2 border-gray-300 text-gray-700 py-3 rounded-2xl font-semibold hover:bg-gray-50 transition-all duration-200"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#f25022" d="M1 1h10v10H1z"/>
              <path fill="#00a4ef" d="M13 1h10v10H13z"/>
              <path fill="#7fba00" d="M1 13h10v10H1z"/>
              <path fill="#ffb900" d="M13 13h10v10H13z"/>
            </svg>
            <span>Se connecter avec Microsoft</span>
          </button>
        </div>
        </>
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
              
              <button 
                onClick={() => {
                  if (challenge.type === 'quiz') {
                    startQuiz(challenge);
                  }
                }}
                className={`px-6 py-2 rounded-full font-semibold text-sm transition-all duration-200 ${
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

  // Seasons Screen
  const SeasonsScreen = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="bg-white shadow-lg rounded-b-3xl p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Saisons de vacances</h1>
            <p className="text-gray-600">Gérez vos saisons familiales</p>
          </div>
          <button 
            onClick={() => setShowSeasonForm(true)}
            data-testid="create-season"
            className="bg-gradient-to-r from-blue-400 to-indigo-400 text-white p-3 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
          >
            <Plus className="w-6 h-6" />
          </button>
        </div>
      </div>

      {/* Success message */}
      {createdSeason && (
        <div className="px-6 mb-6">
          <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-xl">
            <div className="font-semibold">Saison créée avec succès !</div>
            <div className="text-sm">Code d'invitation: <span className="font-mono font-bold">{createdSeason.invitation_code}</span></div>
          </div>
        </div>
      )}

      {/* Seasons list - mock data for now */}
      <div className="px-6 space-y-4 mb-20">
        {createdSeason && (
          <div className="bg-white rounded-2xl p-6 shadow-lg" data-testid="seasons-page">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-4">
                <div className="w-16 h-16 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-xl flex items-center justify-center text-white text-2xl">
                  🏝️
                </div>
                <div>
                  <h3 className="font-bold text-gray-800 text-lg">{createdSeason.title}</h3>
                  <p className="text-gray-600">{createdSeason.location}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(createdSeason.start_date).toLocaleDateString()} - {new Date(createdSeason.end_date).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm text-indigo-600 font-semibold">Code: {createdSeason.invitation_code}</div>
                <div className="text-xs text-gray-500">{createdSeason.member_count} membre(s)</div>
              </div>
            </div>
            
            {createdSeason.description && (
              <p className="text-gray-600 mb-4">{createdSeason.description}</p>
            )}
            
            <div className="flex space-x-2">
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-600">
                {createdSeason.is_active ? 'Active' : 'À venir'}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-600">
                Créée par vous
              </span>
            </div>
          </div>
        )}
        
        {/* Empty state */}
        {!createdSeason && (
          <div className="bg-white rounded-2xl p-8 shadow-lg text-center">
            <div className="text-6xl mb-4">🏖️</div>
            <h3 className="text-xl font-bold text-gray-800 mb-2">Aucune saison créée</h3>
            <p className="text-gray-600 mb-6">Créez votre première saison de vacances pour commencer l'aventure familiale !</p>
            <button 
              onClick={() => setShowSeasonForm(true)}
              className="bg-gradient-to-r from-blue-400 to-indigo-400 text-white px-6 py-3 rounded-2xl font-semibold hover:from-blue-500 hover:to-indigo-500 transition-all duration-200 transform hover:scale-105"
            >
              Créer une saison
            </button>
          </div>
        )}
      </div>

      {/* Season Creation Modal */}
      {showSeasonForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-md max-h-[90vh] overflow-y-auto" data-testid="season-form">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800">Créer une nouvelle saison</h2>
                <button 
                  onClick={() => setShowSeasonForm(false)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ×
                </button>
              </div>

              {/* General Error */}
              {seasonErrors.general && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-4">
                  {seasonErrors.general}
                </div>
              )}

              <div className="space-y-4">
                {/* Title Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Titre de la saison *
                  </label>
                  <input
                    type="text"
                    data-testid="season-title"
                    value={seasonFormData.title}
                    onChange={(e) => handleSeasonInputChange('title', e.target.value)}
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors ${
                      seasonErrors.title
                        ? 'border-red-300 focus:border-red-400'
                        : 'border-gray-300 focus:border-blue-400'
                    }`}
                    placeholder="Vacances Réunion 2025"
                  />
                  {seasonErrors.title && (
                    <p className="text-red-600 text-sm mt-1">{seasonErrors.title}</p>
                  )}
                </div>

                {/* Description Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Description (optionnel)
                  </label>
                  <textarea
                    data-testid="season-description"
                    value={seasonFormData.description}
                    onChange={(e) => handleSeasonInputChange('description', e.target.value)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-blue-400 transition-colors"
                    placeholder="Nos vacances en famille à la Réunion"
                    rows={3}
                  />
                </div>

                {/* Location Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Localisation *
                  </label>
                  <input
                    type="text"
                    data-testid="location"
                    value={seasonFormData.location}
                    onChange={(e) => handleSeasonInputChange('location', e.target.value)}
                    className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors ${
                      seasonErrors.location
                        ? 'border-red-300 focus:border-red-400'
                        : 'border-gray-300 focus:border-blue-400'
                    }`}
                    placeholder="Île de La Réunion, France"
                  />
                  {seasonErrors.location && (
                    <p className="text-red-600 text-sm mt-1">{seasonErrors.location}</p>
                  )}
                </div>

                {/* Date Fields */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Date de début *
                    </label>
                    <input
                      type="date"
                      data-testid="start-date"
                      value={seasonFormData.start_date}
                      onChange={(e) => handleSeasonInputChange('start_date', e.target.value)}
                      className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors ${
                        seasonErrors.dates
                          ? 'border-red-300 focus:border-red-400'
                          : 'border-gray-300 focus:border-blue-400'
                      }`}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Date de fin *
                    </label>
                    <input
                      type="date"
                      data-testid="end-date"
                      value={seasonFormData.end_date}
                      onChange={(e) => handleSeasonInputChange('end_date', e.target.value)}
                      className={`w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors ${
                        seasonErrors.dates
                          ? 'border-red-300 focus:border-red-400'
                          : 'border-gray-300 focus:border-blue-400'
                      }`}
                    />
                  </div>
                </div>
                {seasonErrors.dates && (
                  <p className="text-red-600 text-sm mt-1">{seasonErrors.dates}</p>
                )}

                {/* Cover Photo Field */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Photo de couverture (optionnel)
                  </label>
                  <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-blue-400 transition-colors">
                    <input
                      type="file"
                      data-testid="cover-photo"
                      accept="image/*"
                      onChange={(e) => handleSeasonInputChange('cover_image', e.target.files?.[0] || null)}
                      className="hidden"
                      id="cover-upload"
                    />
                    <label htmlFor="cover-upload" className="cursor-pointer">
                      <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">
                        {seasonFormData.cover_image ? seasonFormData.cover_image.name : 'Cliquez pour télécharger une photo'}
                      </p>
                    </label>
                  </div>
                </div>

                {/* Create Button */}
                <button
                  onClick={handleCreateSeason}
                  data-testid="submit-season"
                  disabled={isCreatingSeason}
                  className={`w-full py-4 rounded-2xl font-semibold text-lg transition-all duration-200 transform hover:scale-105 ${
                    isCreatingSeason
                      ? 'bg-gray-400 text-white cursor-not-allowed'
                      : 'bg-gradient-to-r from-blue-400 to-indigo-400 text-white hover:from-blue-500 hover:to-indigo-500'
                  }`}
                >
                  {isCreatingSeason ? 'Création...' : 'Créer la saison'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
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
          { id: 'seasons', icon: Calendar, label: 'Saisons' },
          { id: 'challenges', icon: Target, label: 'Défis' },
          { id: 'leaderboard', icon: Trophy, label: 'Classement' },
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
      {currentScreen === 'seasons' && <SeasonsScreen />}
      {currentScreen === 'challenges' && <ChallengesScreen />}
      {currentScreen === 'leaderboard' && <LeaderboardScreen />}
      {currentScreen === 'photos' && <PhotosScreen />}
      {currentScreen === 'profile' && <ProfileScreen />}
      <BottomNavigation />
      <QuizModal />
    </div>
  );
}

export default App;