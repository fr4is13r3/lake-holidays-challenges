"""
Steps pour la génération de contenu par IA
Tests BDD pour l'application Vacances Gamifiées
"""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
import json


# ========== GIVEN Steps ==========

@given('je suis dans la section de génération de contenu IA')
def step_in_ai_content_section(context):
    """Naviguer vers la section de génération de contenu IA"""
    ai_url = f"{context.base_url}/ai-content"
    context.driver.get(ai_url)
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='ai-content-section'], .ai-generator"))
    )


@given('les services Azure OpenAI sont configurés')
def step_azure_openai_configured(context):
    """Vérifier que les services Azure OpenAI sont configurés"""
    context.azure_openai_config = {
        "endpoint": "https://test-openai.openai.azure.com/",
        "api_key": "test_key",
        "deployment": "gpt-4",
        "status": "operational"
    }


@given('notre famille est en vacances à "{location}"')
def step_family_on_vacation_at(context, location):
    """Configurer la localisation de vacances"""
    context.vacation_location = location
    
    # Simuler la géolocalisation
    context.driver.execute_script(f"""
        window.mockLocation = '{location}';
        navigator.geolocation.getCurrentPosition = function(success) {{
            const coords = {location.lower().includes('réunion') and 
                           '{ latitude: -21.1151, longitude: 55.5364 }' or
                           '{ latitude: 0, longitude: 0 }'};
            success({{ coords: coords }});
        }};
    """)


@given('nous sommes le "{date}" pendant les vacances à "{location}"')
def step_current_vacation_date_location(context, date, location):
    """Configurer la date actuelle des vacances et le lieu"""
    context.vacation_date = date
    context.vacation_location = location
    context.driver.execute_script(f"window.mockDate = '{date}';")
    context.driver.execute_script(f"window.mockLocation = '{location}';")


@given('nous sommes le "{date}" pendant les vacances')
def step_current_vacation_date(context, date):
    """Configurer la date actuelle des vacances"""
    context.vacation_date = date
    context.driver.execute_script(f"window.mockDate = '{date}';")


@given('notre profil familial indique')
def step_family_profile_indicates(context):
    """Configurer le profil familial à partir du tableau de données"""
    if context.table:
        context.family_profile = {}
        for row in context.table:
            context.family_profile[row['Critère']] = row['Valeur']


@given('nous avons prévu d\'aller "{activity}"')
def step_planned_activity_for_ai(context, activity):
    """Configurer l'activité prévue pour la génération IA"""
    context.planned_activity = activity


@given('l\'IA a déjà généré du contenu aujourd\'hui')
def step_ai_already_generated_content(context):
    """Configurer que l'IA a déjà généré du contenu"""
    context.daily_ai_generation_count = 3
    context.last_generation_time = "09:00"


@given('la météo prévoit "{weather}"')
def step_weather_forecast(context, weather):
    """Configurer les prévisions météo"""
    context.weather_forecast = weather
    
    # Simuler les données météo
    context.driver.execute_script(f"""
        window.mockWeather = {{
            condition: '{weather}',
            temperature: 25,
            humidity: 70
        }};
    """)


@given('l\'application prend en charge "{languages}"')
def step_app_supports_languages(context, languages):
    """Configurer les langues supportées"""
    context.supported_languages = [lang.strip() for lang in languages.split(',')]


@given('ma langue préférée est "{language}"')
def step_preferred_language(context, language):
    """Configurer la langue préférée"""
    context.preferred_language = language
    
    # Définir la langue dans le navigateur
    context.driver.execute_script(f"""
        Object.defineProperty(navigator, 'language', {{
            get: function() {{ return '{language.lower()}-FR'; }}
        }});
        localStorage.setItem('preferredLanguage', '{language}');
    """)


# ========== WHEN Steps ==========

@when('je clique sur "Générer des défis personnalisés"')
def step_click_generate_personalized_challenges(context):
    """Cliquer sur le bouton de génération de défis personnalisés"""
    generate_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='generate-challenges'], .generate-personalized, #ai-generate"
    )
    generate_btn.click()
    
    context.generation_started = True


@when('l\'IA analyse notre profil et localisation')
def step_ai_analyzes_profile_location(context):
    """Simuler l'analyse du profil et localisation par l'IA"""
    # Attendre l'analyse
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ai-analyzing, .profile-analysis"))
    )
    
    # Simuler le processus d'analyse
    context.driver.execute_script("""
        window.aiAnalysis = {
            profile: 'family_with_teens',
            location: 'reunion_island',
            interests: ['culture', 'adventure', 'gastronomy'],
            weather: 'sunny'
        };
    """)
    
    time.sleep(2)  # Délai d'analyse réaliste


@when('je demande un nouveau défi')
def step_request_new_challenge(context):
    """Demander un nouveau défi"""
    new_challenge_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='new-challenge'], .request-challenge, #generate-one"
    )
    new_challenge_btn.click()


@when('je sélectionne la catégorie "{category}"')
def step_select_challenge_category(context, category):
    """Sélectionner une catégorie de défi"""
    category_select = Select(context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='category-select'], .category-filter, #challenge-category"
    ))
    category_select.select_by_visible_text(category)
    context.selected_category = category


@when('je clique sur "Générer un quiz"')
def step_click_generate_quiz(context):
    """Cliquer sur la génération de quiz"""
    quiz_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='generate-quiz'], .quiz-generator, #ai-quiz"
    )
    quiz_btn.click()
    context.quiz_generation_started = True


@when('je spécifie le thème "{theme}"')
def step_specify_quiz_theme(context, theme):
    """Spécifier le thème du quiz"""
    theme_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='quiz-theme'], input[name='theme'], #quiz-topic"
    )
    theme_field.clear()
    theme_field.send_keys(theme)
    context.quiz_theme = theme


@when('je confirme la génération')
def step_confirm_generation(context):
    """Confirmer la génération"""
    confirm_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='confirm-generate'], .confirm-generation, button[type='submit']"
    )
    confirm_btn.click()


@when('je change ma langue en "{language}"')
def step_change_language(context, language):
    """Changer la langue de l'interface"""
    # Ouvrir le sélecteur de langue
    language_selector = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='language-select'], .language-switcher, #lang-select"
    )
    language_selector.click()
    
    # Sélectionner la nouvelle langue
    language_option = context.driver.find_element(
        By.CSS_SELECTOR,
        f"[data-lang='{language.lower()}'], option[value='{language}']"
    )
    language_option.click()
    
    context.current_language = language


@when('je demande une traduction des défis')
def step_request_challenge_translation(context):
    """Demander la traduction des défis"""
    translate_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='translate-challenges'], .translate-btn, #translate-content"
    )
    translate_btn.click()
    context.translation_requested = True


@when('je saisis des préférences personnalisées')
def step_enter_custom_preferences(context):
    """Saisir des préférences personnalisées"""
    if context.table:
        for row in context.table:
            preference_field = context.driver.find_element(
                By.CSS_SELECTOR,
                f"[data-preference='{row['Préférence'].lower()}'], #{row['Préférence'].lower()}-pref"
            )
            preference_field.clear()
            preference_field.send_keys(row['Valeur'])


@when('je sauvegarde ces préférences')
def step_save_preferences(context):
    """Sauvegarder les préférences"""
    save_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='save-preferences'], .save-prefs, #save-settings"
    )
    save_btn.click()
    
    # Attendre la confirmation de sauvegarde
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".preferences-saved, .save-success"))
    )


# ========== THEN Steps ==========

@then('l\'IA doit générer "{count}" défis personnalisés')
def step_ai_should_generate_personalized_challenges(context, count):
    """Vérifier que l'IA génère le bon nombre de défis personnalisés"""
    expected_count = int(count)
    
    # Attendre la génération complète
    generated_challenges = context.wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".generated-challenge, .ai-challenge"))
    )
    
    assert len(generated_challenges) == expected_count, f"Nombre de défis incorrect: {len(generated_challenges)} au lieu de {expected_count}"


@then('chaque défi doit être adapté à notre profil familial')
def step_challenges_adapted_to_family_profile(context):
    """Vérifier que les défis sont adaptés au profil familial"""
    challenge_descriptions = [
        elem.text for elem in context.driver.find_elements(By.CSS_SELECTOR, ".challenge-description, .ai-challenge-text")
    ]
    
    # Vérifier que les défis contiennent des éléments du profil familial
    family_keywords = ["famille", "adolescent", "culture", "aventure"]
    profile_adapted = any(
        any(keyword in desc.lower() for keyword in family_keywords)
        for desc in challenge_descriptions
    )
    
    assert profile_adapted, "Défis non adaptés au profil familial"


@then('tenir compte de la localisation "{location}"')
def step_challenges_consider_location(context, location):
    """Vérifier que les défis tiennent compte de la localisation"""
    challenge_texts = [
        elem.text for elem in context.driver.find_elements(By.CSS_SELECTOR, ".challenge-description")
    ]
    
    location_keywords = location.lower().split()
    location_considered = any(
        any(keyword in text.lower() for keyword in location_keywords)
        for text in challenge_texts
    )
    
    assert location_considered, f"Localisation {location} non prise en compte"


@then('être variés \\(photo, quiz, action\\)')
def step_challenges_should_be_varied(context):
    """Vérifier que les défis sont variés en types"""
    challenge_types = [
        elem.get_attribute('data-type') or elem.get_attribute('class')
        for elem in context.driver.find_elements(By.CSS_SELECTOR, ".challenge-item, .generated-challenge")
    ]
    
    # Vérifier la présence de différents types
    type_indicators = ['photo', 'quiz', 'action', 'exploration']
    found_types = [t for t in type_indicators if any(t in str(ct).lower() for ct in challenge_types)]
    
    assert len(found_types) >= 2, f"Types de défis insuffisamment variés: {found_types}"


@then('l\'IA doit s\'adapter aux conditions actuelles')
def step_ai_should_adapt_to_current_conditions(context):
    """Vérifier que l'IA s'adapte aux conditions actuelles"""
    # Vérifier que l'IA a pris en compte les conditions (météo, lieu, etc.)
    adaptation_indicators = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".weather-adapted, .location-adapted, .condition-aware"
    )
    
    assert len(adaptation_indicators) > 0, "Aucune adaptation aux conditions détectée"


@then('proposer un défi faisable : "{challenge_example}"')
def step_propose_feasible_challenge(context, challenge_example):
    """Vérifier qu'un défi faisable spécifique est proposé"""
    challenge_descriptions = [
        elem.text for elem in context.driver.find_elements(By.CSS_SELECTOR, ".challenge-description")
    ]
    
    # Vérifier qu'un défi similaire à l'exemple est présent
    example_keywords = challenge_example.lower().split()
    feasible_challenge_found = any(
        all(keyword in desc.lower() for keyword in example_keywords[:2])  # Les 2 premiers mots clés
        for desc in challenge_descriptions
    )
    
    assert feasible_challenge_found, f"Défi faisable '{challenge_example}' non trouvé"


@then('éviter un défi visuel impossible')
def step_avoid_impossible_visual_challenge(context):
    """Vérifier qu'aucun défi visuel impossible n'est proposé"""
    challenge_descriptions = [
        elem.text for elem in context.driver.find_elements(By.CSS_SELECTOR, ".challenge-description")
    ]
    
    # Mots-clés indiquant des défis visuels potentiellement impossibles
    impossible_visual_keywords = ["regarder", "voir", "observer", "photographier"] 
    
    # Dans le contexte de conditions défavorables (nuit, pluie, etc.)
    weather = getattr(context, 'weather_forecast', '').lower()
    if 'nuit' in weather or 'pluie' in weather:
        visual_challenges = [
            desc for desc in challenge_descriptions
            if any(keyword in desc.lower() for keyword in impossible_visual_keywords)
        ]
        
        assert len(visual_challenges) == 0 or not any('extérieur' in desc.lower() for desc in visual_challenges), \
            "Défis visuels impossibles détectés"


@then('je dois voir un quiz avec "{question_count}" questions')
def step_should_see_quiz_with_questions(context, question_count):
    """Vérifier qu'un quiz avec le bon nombre de questions est généré"""
    expected_count = int(question_count)
    
    # Attendre la génération du quiz
    quiz_questions = context.wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quiz-question, .generated-question"))
    )
    
    assert len(quiz_questions) == expected_count, f"Nombre de questions incorrect: {len(quiz_questions)} au lieu de {expected_count}"


@then('chaque question doit porter sur "{topic}"')
def step_questions_should_be_about_topic(context, topic):
    """Vérifier que les questions portent sur le bon sujet"""
    question_texts = [
        elem.text for elem in context.driver.find_elements(By.CSS_SELECTOR, ".quiz-question, .question-text")
    ]
    
    topic_keywords = topic.lower().split()
    topic_related = any(
        any(keyword in question.lower() for keyword in topic_keywords)
        for question in question_texts
    )
    
    assert topic_related, f"Questions non liées au sujet '{topic}'"


@then('avoir des options de réponse pertinentes')
def step_should_have_relevant_answer_options(context):
    """Vérifier que les options de réponse sont pertinentes"""
    answer_options = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".quiz-option, .answer-choice, .response-option"
    )
    
    # Vérifier qu'il y a au moins 3 options par question
    questions_count = len(context.driver.find_elements(By.CSS_SELECTOR, ".quiz-question"))
    min_expected_options = questions_count * 3
    
    assert len(answer_options) >= min_expected_options, f"Options de réponse insuffisantes: {len(answer_options)}"


@then('l\'interface doit s\'afficher en "{language}"')
def step_interface_should_display_in_language(context, language):
    """Vérifier que l'interface s'affiche dans la bonne langue"""
    # Vérifier la langue de quelques éléments clés
    page_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        "h1, h2, button, .main-text, [data-translatable]"
    )
    
    # Dictionnaire de mots-clés par langue pour vérification basique
    language_keywords = {
        "Français": ["défis", "générer", "famille", "points"],
        "English": ["challenges", "generate", "family", "points"],
        "Español": ["desafíos", "generar", "familia", "puntos"]
    }
    
    expected_keywords = language_keywords.get(language, [])
    language_detected = any(
        any(keyword.lower() in elem.text.lower() for keyword in expected_keywords)
        for elem in page_elements if elem.text.strip()
    )
    
    assert language_detected, f"Interface non affichée en {language}"


@then('les défis générés doivent être traduits en "{language}"')
def step_generated_challenges_should_be_translated(context, language):
    """Vérifier que les défis générés sont traduits"""
    challenge_texts = [
        elem.text for elem in context.driver.find_elements(By.CSS_SELECTOR, ".challenge-description, .ai-challenge")
    ]
    
    # Vérification basique de la langue (à améliorer avec un détecteur de langue réel)
    if language == "English":
        english_indicators = ["take a photo", "find", "discover", "explore"]
        translation_detected = any(
            any(indicator in text.lower() for indicator in english_indicators)
            for text in challenge_texts
        )
    elif language == "Español":
        spanish_indicators = ["tomar una foto", "encontrar", "descubrir", "explorar"]
        translation_detected = any(
            any(indicator in text.lower() for indicator in spanish_indicators)
            for text in challenge_texts
        )
    else:
        translation_detected = True  # Assume French is default
    
    assert translation_detected, f"Défis non traduits en {language}"


@then('les prochaines générations doivent tenir compte de mes préférences')
def step_future_generations_should_consider_preferences(context):
    """Vérifier que les préférences sont sauvegardées pour les futures générations"""
    # Vérifier que les préférences sont stockées
    saved_preferences = context.driver.execute_script("""
        return localStorage.getItem('aiPreferences') || sessionStorage.getItem('userPreferences');
    """)
    
    assert saved_preferences is not None, "Préférences non sauvegardées"
    
    # Vérifier l'indication que les préférences seront utilisées
    preference_confirmation = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".preferences-applied, .settings-saved, .future-generation-notice"
    )
    
    assert len(preference_confirmation) > 0, "Aucune confirmation d'utilisation des préférences"


@then('l\'IA doit apprendre de nos interactions précédentes')
def step_ai_should_learn_from_previous_interactions(context):
    """Vérifier que l'IA apprend des interactions précédentes"""
    # Vérifier la présence d'indicateurs d'apprentissage
    learning_indicators = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".ai-learning, .interaction-history, .personalization-active"
    )
    
    assert len(learning_indicators) > 0, "Aucun indicateur d'apprentissage IA détecté"
    
    # Vérifier que l'historique des interactions est pris en compte
    interaction_history = context.driver.execute_script("""
        return localStorage.getItem('interactionHistory') || window.aiInteractionHistory;
    """)
    
    assert interaction_history is not None, "Historique des interactions non conservé"
