"""
Configuration de l'environnement Behave pour les tests BDD
de l'application Vacances Gamifiées
"""

import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def before_all(context):
    """Configuration globale avant tous les tests"""
    
    # Configuration des URLs selon l'environnement
    context.environment = os.getenv('TEST_ENV', 'dev')
    
    url_mapping = {
        'dev': context.config.userdata.get('base_url_dev', 'http://localhost:3000'),
        'staging': context.config.userdata.get('base_url_staging'),
        'prod': context.config.userdata.get('base_url_prod')
    }
    
    context.base_url = url_mapping.get(context.environment)
    
    # Configuration des utilisateurs de test
    context.test_users = {
        "papa_test": {
            "email": "papa.test@example.com",
            "password": "TestPass123!",
            "name": "Papa Aventurier",
            "age": 45,
            "preferences": ["Sport", "Histoire"]
        },
        "maman_test": {
            "email": "maman.test@example.com", 
            "password": "TestPass123!",
            "name": "Maman Photographe",
            "age": 45,
            "preferences": ["Photo", "Culture"]
        },
        "ado1_test": {
            "email": "ado1.test@example.com",
            "password": "TestPass123!",
            "name": "Ado1 Sportif", 
            "age": 18,
            "preferences": ["Sport", "Gaming"]
        },
        "ado2_test": {
            "email": "ado2.test@example.com",
            "password": "TestPass123!",
            "name": "Ado2 Créatif",
            "age": 15,
            "preferences": ["Art", "Photo"]
        }
    }
    
    # Configuration des saisons de test
    context.test_seasons = {
        "reunion_2025": {
            "title": "Vacances Réunion 2025",
            "start_date": "2025-07-01",
            "end_date": "2025-07-30", 
            "location": "Île de La Réunion, France",
            "invitation_code": "REUNION2025TEST"
        }
    }
    
    # Configuration Azure OpenAI pour les tests
    context.azure_config = {
        "endpoint": os.getenv('AZURE_OPENAI_ENDPOINT', 'test_endpoint'),
        "api_key": os.getenv('AZURE_OPENAI_KEY', 'test_key'),
        "deployment_name": "gpt-4"
    }


def before_feature(context, feature):
    """Configuration avant chaque feature"""
    
    # Tags spéciaux pour la configuration
    if 'web' in feature.tags or 'ui' in feature.tags:
        # Configuration du navigateur pour les tests UI
        chrome_options = Options()
        
        if context.config.userdata.getbool('headless', True):
            chrome_options.add_argument('--headless')
            
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=375,667')  # iPhone dimensions
        
        # Simulation mobile
        mobile_emulation = {
            "deviceMetrics": {"width": 375, "height": 667, "pixelRatio": 2.0},
            "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        }
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        context.driver = webdriver.Chrome(options=chrome_options)
        context.wait = WebDriverWait(context.driver, 10)
        
    # Configuration de la base de données de test
    if 'database' in feature.tags:
        context.test_db_url = context.config.userdata.get('test_db_url')
        # Ici on pourrait initialiser la connexion DB
        
    # Configuration des mocks pour les tests API
    if 'api' in feature.tags:
        context.api_base_url = f"{context.base_url}/api/v1"
        context.auth_tokens = {}


def before_scenario(context, scenario):
    """Configuration avant chaque scenario"""
    
    # Reset des données de test pour chaque scenario
    context.current_user = None
    context.current_season = None
    context.current_challenges = []
    context.current_scores = {}
    
    # Configuration spécifique selon les tags
    if 'mobile' in scenario.tags and hasattr(context, 'driver'):
        # S'assurer que nous sommes en mode mobile
        context.driver.set_window_size(375, 667)
        
    if 'clean_db' in scenario.tags:
        # Nettoyer la base de données de test
        pass  # Implémenter le nettoyage si nécessaire


def after_scenario(context, scenario):
    """Nettoyage après chaque scenario"""
    
    # Capture d'écran en cas d'échec pour les tests UI
    if scenario.status == "failed" and hasattr(context, 'driver'):
        screenshot_name = f"failed_{scenario.name.replace(' ', '_')}.png"
        screenshot_path = os.path.join('reports', 'screenshots', screenshot_name)
        
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        context.driver.save_screenshot(screenshot_path)
        
        print(f"Screenshot saved: {screenshot_path}")


def after_feature(context, feature):
    """Nettoyage après chaque feature"""
    
    # Fermeture du navigateur
    if hasattr(context, 'driver'):
        context.driver.quit()


def after_all(context):
    """Nettoyage global après tous les tests"""
    
    # Génération du rapport final
    reports_dir = 'reports'
    os.makedirs(reports_dir, exist_ok=True)
    
    # Ici on pourrait générer des rapports personnalisés
    print(f"Tests terminés. Rapports disponibles dans {reports_dir}/")
