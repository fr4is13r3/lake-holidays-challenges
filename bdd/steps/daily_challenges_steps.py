"""
Steps pour les défis quotidiens et quiz
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

@given('je participe à la saison active "{season_name}"')
def step_participating_in_active_season(context, season_name):
    """Configurer la participation à une saison active"""
    context.active_season = {
        "name": season_name,
        "status": "active",
        "start_date": "01/07/2025",
        "end_date": "30/07/2025",
        "location": "Île de La Réunion, France"
    }
    context.user_participation = True


@given('nous sommes dans la période de la saison')
def step_within_season_period(context):
    """Vérifier que nous sommes dans la période de la saison"""
    context.within_season = True
    # Simuler la date actuelle dans la période
    context.current_date = "05/07/2025"


@given('l\'IA de génération de contenu est disponible')
def step_ai_content_generation_available(context):
    """Configurer la disponibilité de l'IA"""
    context.ai_available = True
    context.ai_status = "operational"


@given('nous sommes le "{date}" à "{time}"')
def step_current_datetime(context, date, time):
    """Configurer la date et l'heure actuelles"""
    context.current_date = date
    context.current_time = time
    # Injection JavaScript pour simuler la date/heure
    context.driver.execute_script(f"""
        window.mockDateTime = {{
            date: '{date}',
            time: '{time}'
        }};
    """)


@given('notre localisation GPS est "{location}"')
def step_gps_location(context, location):
    """Configurer la localisation GPS"""
    context.gps_location = location
    # Simuler la géolocalisation
    context.driver.execute_script(f"""
        navigator.geolocation.getCurrentPosition = function(success) {{
            success({{
                coords: {{
                    latitude: -20.8823,
                    longitude: 55.4504
                }}
            }});
        }};
        window.mockLocation = '{location}';
    """)


@given('notre activité prévue est "{activity}"')
def step_planned_activity(context, activity):
    """Configurer l'activité prévue"""
    context.planned_activity = activity


@given('un quiz sur "{topic}" est disponible')
def step_quiz_available(context, topic):
    """Configurer un quiz disponible"""
    context.available_quiz = {
        "topic": topic,
        "questions": [
            {
                "question": "Quel est l'épice emblématique de la cuisine créole ?",
                "options": ["Curcuma", "Paprika", "Safran", "Cardamome"],
                "correct": "Curcuma",
                "points": 10
            }
        ]
    }


@given('j\'ai déjà complété "{count}" défis aujourd\'hui')
def step_completed_challenges_today(context, count):
    """Configurer les défis déjà complétés"""
    context.completed_challenges_today = int(count)
    context.daily_points = int(count) * 10  # 10 points par défi


@given('il reste "{time_left}" avant la fin de la journée')
def step_time_left_in_day(context, time_left):
    """Configurer le temps restant dans la journée"""
    context.time_left_today = time_left


@given('le défi photo "{challenge_name}" est actif')
def step_photo_challenge_active(context, challenge_name):
    """Configurer un défi photo actif"""
    context.active_photo_challenge = {
        "name": challenge_name,
        "description": "Prenez une photo d'un élément architectural créole",
        "points": 20,
        "time_limit": "1 heure"
    }


# ========== WHEN Steps ==========

@when('le système génère les défis du jour')
def step_system_generates_daily_challenges(context):
    """Déclencher la génération des défis quotidiens"""
    # Naviguer vers la page des défis
    challenges_url = f"{context.base_url}/challenges"
    context.driver.get(challenges_url)
    
    # Vérifier ou déclencher la génération
    generate_btn = context.driver.find_elements(
        By.CSS_SELECTOR,
        "[data-testid='generate-challenges'], .generate-challenges, #generate-daily"
    )
    
    if generate_btn:
        generate_btn[0].click()
    
    # Attendre que les défis soient générés
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".daily-challenges, .challenges-list"))
    )


@when('je clique sur le défi quiz')
def step_click_quiz_challenge(context):
    """Cliquer sur un défi quiz"""
    quiz_challenge = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='quiz-challenge'], .quiz-challenge, .challenge-quiz"
    )
    quiz_challenge.click()
    
    # Attendre que le quiz s'ouvre
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='quiz-container'], .quiz-interface"))
    )


@when('je sélectionne "{answer}"')
def step_select_quiz_answer(context, answer):
    """Sélectionner une réponse au quiz"""
    # Trouver l'option de réponse
    answer_option = context.driver.find_element(
        By.XPATH,
        f"//div[contains(@class, 'quiz-option') and contains(text(), '{answer}')]"
    )
    answer_option.click()
    context.selected_answer = answer


@when('je clique sur "Valider ma réponse"')
def step_validate_quiz_answer(context):
    """Valider la réponse au quiz"""
    validate_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='validate-answer'], .validate-answer, #validate-quiz"
    )
    validate_btn.click()


@when('je prends une photo avec mon téléphone')
def step_take_photo_with_phone(context):
    """Simuler la prise de photo"""
    # Cliquer sur le bouton appareil photo
    camera_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='camera-btn'], .camera-button, #take-photo"
    )
    camera_btn.click()
    
    # Simuler l'autorisation de la caméra
    context.driver.execute_script("""
        navigator.mediaDevices.getUserMedia = function() {
            return Promise.resolve({
                getTracks: function() { return []; }
            });
        };
    """)
    
    # Simuler la capture d'image
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".camera-preview, .photo-preview"))
    )
    
    context.photo_taken = True


@when('je télécharge la photo')
def step_upload_photo(context):
    """Télécharger la photo prise"""
    upload_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='upload-photo'], .upload-photo, #submit-photo"
    )
    upload_btn.click()
    
    context.photo_uploaded = True


@when('je saisis ma réponse "{response}"')
def step_enter_text_response(context, response):
    """Saisir une réponse textuelle"""
    response_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='text-response'], textarea, .response-input"
    )
    response_field.clear()
    response_field.send_keys(response)
    context.text_response = response


@when('je soumets ma réponse')
def step_submit_response(context):
    """Soumettre la réponse"""
    submit_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='submit-response'], .submit-response, button[type='submit']"
    )
    submit_btn.click()


@when('je consulte le récapitulatif de la journée')
def step_check_daily_summary(context):
    """Consulter le récapitulatif quotidien"""
    summary_url = f"{context.base_url}/daily-summary"
    context.driver.get(summary_url)
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='daily-summary'], .daily-recap"))
    )


@when('je consulte mes statistiques personnelles')
def step_check_personal_stats(context):
    """Consulter les statistiques personnelles"""
    stats_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='my-stats'], .my-statistics, #personal-stats"
    )
    stats_btn.click()
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".statistics-panel, .stats-container"))
    )


# ========== THEN Steps ==========

@then('je dois recevoir "{count}" défis différents')
def step_should_receive_challenges(context, count):
    """Vérifier que le nombre correct de défis est reçu"""
    expected_count = int(count)
    
    challenge_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".challenge-item, .daily-challenge, [data-testid='challenge']"
    )
    
    assert len(challenge_elements) == expected_count, f"Nombre de défis incorrect: {len(challenge_elements)} au lieu de {expected_count}"


@then('les défis doivent être adaptés à la localisation')
def step_challenges_adapted_to_location(context):
    """Vérifier que les défis sont adaptés à la localisation"""
    challenge_texts = [
        elem.text for elem in context.driver.find_elements(By.CSS_SELECTOR, ".challenge-description")
    ]
    
    location_keywords = ["réunion", "créole", "saint-denis", "marché"]
    location_adapted = any(
        any(keyword in text.lower() for keyword in location_keywords)
        for text in challenge_texts
    )
    
    assert location_adapted, "Aucun défi adapté à la localisation trouvé"


@then('les défis doivent être en rapport avec l\'activité prévue')
def step_challenges_related_to_activity(context):
    """Vérifier que les défis sont liés à l'activité prévue"""
    challenge_texts = [
        elem.text for elem in context.driver.find_elements(By.CSS_SELECTOR, ".challenge-description")
    ]
    
    activity_keywords = ["marché", "visite", "découverte", "culture"]
    activity_related = any(
        any(keyword in text.lower() for keyword in activity_keywords)
        for text in challenge_texts
    )
    
    assert activity_related, "Aucun défi en rapport avec l'activité trouvé"


@then('je dois voir une notification "{notification_text}"')
def step_should_see_notification(context, notification_text):
    """Vérifier qu'une notification est affichée"""
    notification = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".notification, .alert, .toast"))
    )
    
    assert notification_text.lower() in notification.text.lower(), f"Notification incorrecte: {notification.text}"


@then('je dois voir une question "{question_text}"')
def step_should_see_quiz_question(context, question_text):
    """Vérifier qu'une question de quiz est affichée"""
    question_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".quiz-question, .question-text"))
    )
    
    assert question_text in question_element.text, f"Question incorrecte: {question_element.text}"


@then('je dois voir "{count}" options de réponse')
def step_should_see_answer_options(context, count):
    """Vérifier que le bon nombre d'options de réponse est affiché"""
    expected_count = int(count)
    
    option_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".quiz-option, .answer-option, .response-choice"
    )
    
    assert len(option_elements) == expected_count, f"Nombre d'options incorrect: {len(option_elements)} au lieu de {expected_count}"


@then('je dois voir "{feedback_message}"')
def step_should_see_feedback(context, feedback_message):
    """Vérifier qu'un message de feedback est affiché"""
    feedback_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".quiz-feedback, .answer-feedback, .result-message"))
    )
    
    assert feedback_message in feedback_element.text, f"Feedback incorrect: {feedback_element.text}"


@then('mes points doivent être mis à jour automatiquement')
def step_points_updated_automatically(context):
    """Vérifier que les points sont mis à jour automatiquement"""
    # Attendre une mise à jour des points
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".points-update, .score-animation"))
    )
    
    # Vérifier que le score a changé
    current_score = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='user-score'], .user-points, .current-score"
    ).text
    
    # Extraire la valeur numérique
    import re
    score_value = int(re.search(r'\d+', current_score).group())
    
    # Vérifier que le score a augmenté
    previous_score = getattr(context, 'previous_score', 0)
    assert score_value > previous_score, f"Score non mis à jour: {score_value} <= {previous_score}"
    
    context.previous_score = score_value


@then('la photo doit être analysée par l\'IA')
def step_photo_analyzed_by_ai(context):
    """Vérifier que la photo est analysée par l'IA"""
    # Attendre l'analyse IA
    analysis_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".ai-analysis, .photo-analysis, .ai-feedback"))
    )
    
    assert "analyse" in analysis_element.text.lower() or "IA" in analysis_element.text, "Analyse IA non détectée"


@then('je dois recevoir un score basé sur la pertinence')
def step_receive_relevance_score(context):
    """Vérifier que le score est basé sur la pertinence"""
    score_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".relevance-score, .photo-score"))
    )
    
    # Vérifier que le score est accompagné d'une explication
    explanation = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".score-explanation, .relevance-feedback"
    )
    
    assert len(explanation) > 0, "Aucune explication du score trouvée"


@then('je dois voir mes "{count}" défis complétés')
def step_should_see_completed_challenges(context, count):
    """Vérifier le nombre de défis complétés visibles"""
    expected_count = int(count)
    
    completed_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".completed-challenge, .challenge-completed, [data-status='completed']"
    )
    
    assert len(completed_elements) == expected_count, f"Nombre de défis complétés incorrect: {len(completed_elements)} au lieu de {expected_count}"


@then('mes points totaux de la journée')
def step_see_total_daily_points(context):
    """Vérifier l'affichage des points totaux de la journée"""
    daily_total = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='daily-total'], .daily-points, .points-today"
    )
    
    assert daily_total.is_displayed(), "Points totaux de la journée non affichés"
    
    # Vérifier que c'est un nombre valide
    points_text = daily_total.text
    import re
    points_value = re.search(r'\d+', points_text)
    assert points_value is not None, f"Valeur de points invalide: {points_text}"


@then('ma position dans le classement familial')
def step_see_family_ranking_position(context):
    """Vérifier l'affichage de la position dans le classement"""
    ranking_element = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='my-rank'], .my-ranking, .family-position"
    )
    
    assert ranking_element.is_displayed(), "Position dans le classement non affichée"
    
    ranking_text = ranking_element.text.lower()
    position_indicators = ["position", "place", "#", "rang"]
    
    has_position = any(indicator in ranking_text for indicator in position_indicators)
    assert has_position, f"Indication de position non trouvée: {ranking_text}"
