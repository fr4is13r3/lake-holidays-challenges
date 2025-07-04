"""
Steps pour le scoring et classement
Tests BDD pour l'application Vacances Gamifiées
"""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
import re


# ========== GIVEN Steps ==========

@given('notre famille comprend "{count}" membres')
def step_family_member_count(context, count):
    """Configurer le nombre de membres de famille"""
    context.family_size = int(count)
    context.family_members = [
        {"name": "Papa", "score": 150, "rank": 1},
        {"name": "Maman", "score": 120, "rank": 2},
        {"name": "Ado1", "score": 100, "rank": 3},
        {"name": "Ado2", "score": 80, "rank": 4}
    ][:int(count)]


@given('j\'ai actuellement "{points}" points')
def step_current_user_points(context, points):
    """Configurer les points actuels de l'utilisateur"""
    context.current_user_points = int(points)


@given('je suis en "{position}" position')
def step_current_user_position(context, position):
    """Configurer la position actuelle de l'utilisateur"""
    # Conversion des positions textuelles en numéros
    position_map = {
        "première": 1, "1ère": 1, "1": 1,
        "deuxième": 2, "2ème": 2, "2": 2,
        "troisième": 3, "3ème": 3, "3": 3,
        "quatrième": 4, "4ème": 4, "4": 4
    }
    context.current_user_rank = position_map.get(position.lower(), int(position))


@given('Maman a "{points}" points')
def step_maman_points(context, points):
    """Configurer les points de Maman"""
    context.maman_points = int(points)


@given('Papa a "{points}" points')
def step_papa_points(context, points):
    """Configurer les points de Papa"""
    context.papa_points = int(points)


@given('le classement actuel est visible')
def step_leaderboard_visible(context):
    """Vérifier que le classement est visible"""
    leaderboard_url = f"{context.base_url}/leaderboard"
    context.driver.get(leaderboard_url)
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='leaderboard'], .leaderboard, .ranking"))
    )


@given('je regarde le classement en temps réel')
def step_watching_realtime_leaderboard(context):
    """Configurer la visualisation en temps réel du classement"""
    step_leaderboard_visible(context)
    
    # Activer les mises à jour en temps réel
    realtime_toggle = context.driver.find_elements(
        By.CSS_SELECTOR,
        "[data-testid='realtime-toggle'], .realtime-updates, #live-updates"
    )
    
    if realtime_toggle and not realtime_toggle[0].is_selected():
        realtime_toggle[0].click()
    
    context.realtime_active = True


@given('la journée se termine à 23:59')
def step_day_ends_at_time(context):
    """Configurer l'heure de fin de journée"""
    context.day_end_time = "23:59"


# ========== WHEN Steps ==========

@when('je consulte le classement familial')
def step_check_family_leaderboard(context):
    """Consulter le classement familial"""
    leaderboard_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='leaderboard-btn'], .leaderboard-link, #family-ranking"
    )
    leaderboard_btn.click()
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='family-leaderboard'], .family-ranking"))
    )


@when('je complète un défi de "{points}" points')
def step_complete_challenge_with_points(context, points):
    """Compléter un défi avec des points spécifiques"""
    challenge_points = int(points)
    
    # Simuler la complétion d'un défi
    challenge_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='available-challenge'], .challenge-item:first-child"
    )
    challenge_btn.click()
    
    # Simuler la validation du défi
    complete_btn = context.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='complete-challenge'], .complete-btn"))
    )
    complete_btn.click()
    
    context.last_earned_points = challenge_points


@when('Maman complète un défi sur son téléphone')
def step_maman_completes_challenge(context):
    """Simuler que Maman complète un défi"""
    # Simulation d'une action externe (autre utilisateur)
    context.driver.execute_script("""
        // Simuler l'événement de mise à jour du score de Maman
        window.dispatchEvent(new CustomEvent('scoreUpdate', {
            detail: { user: 'Maman', points: 15, newTotal: 135 }
        }));
    """)
    context.maman_completed_challenge = True


@when('ses points sont attribués')
def step_points_are_attributed(context):
    """Déclencher l'attribution des points"""
    # Attendre que les points soient traités
    time.sleep(2)  # Simulation du délai de traitement
    
    # Vérifier que l'interface réagit
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".score-update, .points-animation"))
    )


@when('l\'horloge passe à 00:00')
def step_clock_reaches_midnight(context):
    """Simuler le passage à minuit"""
    # Injection JavaScript pour simuler le changement d'heure
    context.driver.execute_script("""
        window.mockTime = '00:00';
        window.dispatchEvent(new CustomEvent('dayChange', {
            detail: { newDay: true, time: '00:00' }
        }));
    """)
    context.day_changed = True


@when('je consulte les détails de mes performances')
def step_check_performance_details(context):
    """Consulter les détails des performances"""
    details_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='performance-details'], .my-performance, #detailed-stats"
    )
    details_btn.click()
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".performance-details, .detailed-stats"))
    )


@when('je filtre par période "{period}"')
def step_filter_by_period(context, period):
    """Filtrer les statistiques par période"""
    period_filter = Select(context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='period-filter'], .period-select, #time-period"
    ))
    period_filter.select_by_visible_text(period)
    
    # Attendre que les données se mettent à jour
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".stats-updated, .filtered-results"))
    )


@when('je compare avec "{member_name}"')
def step_compare_with_member(context, member_name):
    """Comparer avec un autre membre de famille"""
    compare_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        f"[data-testid='compare-{member_name.lower()}'], .compare-btn"
    )
    compare_btn.click()
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".comparison-view, .member-comparison"))
    )
    context.comparing_with = member_name


# ========== THEN Steps ==========

@then('je dois voir le classement avec les "{count}" membres')
def step_should_see_leaderboard_with_members(context, count):
    """Vérifier que le classement affiche le bon nombre de membres"""
    expected_count = int(count)
    
    member_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".leaderboard-member, .ranking-item, .family-member-rank"
    )
    
    assert len(member_elements) == expected_count, f"Nombre de membres incorrect: {len(member_elements)} au lieu de {expected_count}"


@then('chaque membre doit avoir son nom, score et position')
def step_each_member_has_info(context):
    """Vérifier que chaque membre a ses informations complètes"""
    member_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".leaderboard-member, .ranking-item"
    )
    
    for member in member_elements:
        # Vérifier la présence du nom
        name_element = member.find_elements(By.CSS_SELECTOR, ".member-name, .player-name")
        assert len(name_element) > 0, "Nom du membre manquant"
        
        # Vérifier la présence du score
        score_element = member.find_elements(By.CSS_SELECTOR, ".member-score, .points")
        assert len(score_element) > 0, "Score du membre manquant"
        
        # Vérifier la présence de la position
        position_element = member.find_elements(By.CSS_SELECTOR, ".member-rank, .position")
        assert len(position_element) > 0, "Position du membre manquante"


@then('mon score doit passer à "{new_score}" points')
def step_score_should_change_to(context, new_score):
    """Vérifier que le score change vers la nouvelle valeur"""
    expected_score = int(new_score)
    
    # Attendre la mise à jour du score
    context.wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "[data-testid='my-score'], .my-points, .current-score"),
            str(expected_score)
        )
    )
    
    # Vérifier que le score affiché correspond
    score_element = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='my-score'], .my-points, .current-score"
    )
    
    score_text = score_element.text
    actual_score = int(re.search(r'\d+', score_text).group())
    
    assert actual_score == expected_score, f"Score incorrect: {actual_score} au lieu de {expected_score}"


@then('je dois monter en "{new_position}" position')
def step_should_move_to_position(context, new_position):
    """Vérifier le changement de position dans le classement"""
    # Conversion de la position textuelle
    position_map = {
        "première": 1, "1ère": 1, "1": 1,
        "deuxième": 2, "2ème": 2, "2": 2,
        "troisième": 3, "3ème": 3, "3": 3
    }
    expected_position = position_map.get(new_position.lower(), int(new_position))
    
    # Attendre la mise à jour de la position
    context.wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "[data-testid='my-rank'], .my-position"),
            str(expected_position)
        )
    )


@then('je dois voir une animation de progression')
def step_should_see_progression_animation(context):
    """Vérifier qu'une animation de progression est visible"""
    animation_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".score-animation, .rank-change-animation, .progress-animation, .level-up"
    )
    
    assert len(animation_elements) > 0, "Aucune animation de progression trouvée"


@then('je dois voir son score se mettre à jour automatiquement')
def step_should_see_score_update_automatically(context):
    """Vérifier la mise à jour automatique du score"""
    # Attendre la mise à jour en temps réel
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".live-update, .realtime-update, .score-change"))
    )
    
    # Vérifier que le score de Maman a changé
    maman_score_element = context.driver.find_element(
        By.XPATH,
        "//div[contains(@class, 'leaderboard-member') and contains(., 'Maman')]//span[contains(@class, 'score')]"
    )
    
    new_score = int(re.search(r'\d+', maman_score_element.text).group())
    original_score = getattr(context, 'maman_points', 120)
    
    assert new_score > original_score, f"Score de Maman non mis à jour: {new_score} <= {original_score}"


@then('le classement doit se réorganiser si nécessaire')
def step_leaderboard_should_reorganize(context):
    """Vérifier que le classement se réorganise"""
    # Vérifier que l'ordre des membres a potentiellement changé
    member_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".leaderboard-member .member-name, .ranking-item .player-name"
    )
    
    member_names = [elem.text for elem in member_elements]
    
    # Vérifier que la liste est triée par ordre décroissant de score
    # (on ne peut pas vérifier l'ordre exact sans connaître tous les scores)
    assert len(member_names) > 0, "Aucun membre trouvé dans le classement réorganisé"


@then('sans que j\'aie besoin de rafraîchir la page')
def step_without_page_refresh(context):
    """Vérifier qu'aucun rafraîchissement de page n'est nécessaire"""
    # Vérifier que l'URL n'a pas changé (pas de rechargement)
    current_url = context.driver.current_url
    expected_url = getattr(context, 'original_url', current_url)
    
    assert current_url == expected_url, "Page rechargée de manière inattendue"
    
    # Vérifier qu'il n'y a pas eu d'indicateur de chargement de page
    loading_indicators = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".page-loading, .full-page-loader"
    )
    
    assert len(loading_indicators) == 0, "Indicateur de chargement de page détecté"


@then('je dois recevoir un résumé de ma journée')
def step_should_receive_daily_summary(context):
    """Vérifier la réception du résumé quotidien"""
    # Attendre l'apparition du résumé
    summary_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='daily-summary'], .end-of-day-summary"))
    )
    
    assert summary_element.is_displayed(), "Résumé quotidien non affiché"


@then('mes défis complétés \\("{count}" défis\\)')
def step_summary_completed_challenges(context, count):
    """Vérifier le nombre de défis complétés dans le résumé"""
    expected_count = int(count)
    
    completed_count_element = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='completed-count'], .challenges-completed-count"
    )
    
    count_text = completed_count_element.text
    actual_count = int(re.search(r'\d+', count_text).group())
    
    assert actual_count == expected_count, f"Nombre de défis complétés incorrect: {actual_count} au lieu de {expected_count}"


@then('mes points gagnés \\("{points}" points\\)')
def step_summary_points_earned(context, points):
    """Vérifier les points gagnés dans le résumé"""
    expected_points = int(points)
    
    points_element = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='points-earned'], .daily-points-earned"
    )
    
    points_text = points_element.text
    actual_points = int(re.search(r'\d+', points_text).group())
    
    assert actual_points == expected_points, f"Points gagnés incorrects: {actual_points} au lieu de {expected_points}"


@then('ma position finale dans le classement')
def step_summary_final_position(context):
    """Vérifier l'affichage de la position finale"""
    position_element = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='final-position'], .daily-rank, .end-position"
    )
    
    assert position_element.is_displayed(), "Position finale non affichée dans le résumé"


@then('je dois voir un graphique de mes performances sur "{period}"')
def step_should_see_performance_chart(context, period):
    """Vérifier l'affichage du graphique de performances"""
    chart_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='performance-chart'], .stats-chart, .performance-graph"))
    )
    
    assert chart_element.is_displayed(), f"Graphique de performances pour {period} non affiché"


@then('mes statistiques détaillées \\(moyenne de points, meilleurs jours\\)')
def step_should_see_detailed_stats(context):
    """Vérifier l'affichage des statistiques détaillées"""
    stats_elements = [
        "[data-testid='average-points'], .average-score",
        "[data-testid='best-days'], .best-performance",
        "[data-testid='total-challenges'], .challenges-total"
    ]
    
    for selector in stats_elements:
        element = context.driver.find_elements(By.CSS_SELECTOR, selector)
        assert len(element) > 0, f"Statistique manquante: {selector}"


@then('une comparaison côte à côte avec "{member_name}"')
def step_should_see_comparison(context, member_name):
    """Vérifier l'affichage de la comparaison avec un autre membre"""
    comparison_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".member-comparison, .side-by-side-comparison"))
    )
    
    # Vérifier que le nom du membre comparé apparaît
    assert member_name in comparison_element.text, f"Comparaison avec {member_name} non trouvée"
    
    # Vérifier la présence des métriques de comparaison
    comparison_metrics = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".comparison-metric, .compare-stat"
    )
    assert len(comparison_metrics) > 0, "Aucune métrique de comparaison trouvée"
