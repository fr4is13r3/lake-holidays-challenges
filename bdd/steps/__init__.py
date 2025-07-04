"""
Package pour les steps BDD de l'application Vacances Gamifiées

Ce package contient tous les steps nécessaires pour les tests BDD:
- authentication_steps: Authentification et gestion des sessions
- user_profile_steps: Gestion des profils utilisateur et famille
- season_management_steps: Création et gestion des saisons de vacances
- daily_challenges_steps: Défis quotidiens et quiz
- scoring_leaderboard_steps: Système de scoring et classements
- mobile_ui_ux_steps: Interface mobile et expérience utilisateur
- ai_content_generation_steps: Génération de contenu par IA
"""

# Imports pour s'assurer que tous les steps sont disponibles
from . import authentication_steps
from . import user_profile_steps
from . import season_management_steps
from . import daily_challenges_steps
from . import scoring_leaderboard_steps
from . import mobile_ui_ux_steps
from . import ai_content_generation_steps

__all__ = [
    'authentication_steps',
    'user_profile_steps', 
    'season_management_steps',
    'daily_challenges_steps',
    'scoring_leaderboard_steps',
    'mobile_ui_ux_steps',
    'ai_content_generation_steps'
]
