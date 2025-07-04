"""
Steps pour la gestion des saisons de vacances
Tests BDD pour l'application Vacances Gamifiées
"""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime, timedelta


# ========== GIVEN Steps ==========

@given('je suis connecté en tant qu\'utilisateur "{user_role}"')
def step_connected_as_user(context, user_role):
    """Se connecter avec un rôle utilisateur spécifique"""
    context.current_user_role = user_role
    context.user_permissions = {
        "Papa Organisateur": ["create_season", "manage_season", "invite_members"],
        "Maman": ["join_season", "participate"],
        "Ado1": ["join_season", "participate"],
        "Ado2": ["join_season", "participate"]
    }


@given('j\'ai accès aux fonctionnalités de gestion des saisons')
def step_has_season_management_access(context):
    """Vérifier l'accès aux fonctionnalités de gestion"""
    # Vérifier que l'utilisateur a les permissions nécessaires
    user_role = getattr(context, 'current_user_role', 'unknown')
    permissions = context.user_permissions.get(user_role, [])
    assert "create_season" in permissions or "manage_season" in permissions, f"Utilisateur {user_role} sans accès gestion"


@given('je suis sur la page de gestion des saisons')
def step_on_season_management_page(context):
    """Naviguer vers la page de gestion des saisons"""
    seasons_url = f"{context.base_url}/seasons"
    context.driver.get(seasons_url)
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='seasons-page'], .seasons-container"))
    )


@given('une saison "{season_name}" existe')
def step_season_exists(context, season_name):
    """Configurer une saison existante"""
    context.existing_season = {
        "name": season_name,
        "start_date": "01/07/2025",
        "end_date": "30/07/2025",
        "location": "Île de La Réunion, France",
        "invitation_code": "REUNION2025",
        "members": ["Papa Organisateur"]
    }


@given('j\'ai reçu un code d\'invitation "{invitation_code}"')
def step_received_invitation_code(context, invitation_code):
    """Configurer un code d'invitation reçu"""
    context.invitation_code = invitation_code


@given('la saison "{season_name}" est active')
def step_season_is_active(context, season_name):
    """Configurer une saison active"""
    context.active_season = {
        "name": season_name,
        "status": "active",
        "current_day": 5,
        "total_days": 30
    }


@given('nous sommes le "{date}" de la saison')
def step_current_season_date(context, date):
    """Configurer la date actuelle de la saison"""
    context.season_current_date = date
    # Simuler la date dans l'application (injection JavaScript par exemple)
    context.driver.execute_script(f"window.mockDate = '{date}';")


# ========== WHEN Steps ==========

@when('je clique sur "Créer une nouvelle saison"')
def step_click_create_season(context):
    """Cliquer sur le bouton de création de saison"""
    create_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='create-season'], .create-season-btn, #create-season"
    )
    create_btn.click()
    
    # Attendre que le formulaire s'ouvre
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='season-form'], .season-creation-form"))
    )


@when('je saisis le titre "{title}"')
def step_enter_season_title(context, title):
    """Saisir le titre de la saison"""
    title_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='season-title'], input[name='title'], #season-title"
    )
    title_field.clear()
    title_field.send_keys(title)
    context.season_title = title


@when('je sélectionne la date de début "{start_date}"')
def step_select_start_date(context, start_date):
    """Sélectionner la date de début"""
    start_date_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='start-date'], input[name='start_date'], #start-date"
    )
    start_date_field.clear()
    start_date_field.send_keys(start_date)
    context.season_start_date = start_date


@when('je sélectionne la date de fin "{end_date}"')
def step_select_end_date(context, end_date):
    """Sélectionner la date de fin"""
    end_date_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='end-date'], input[name='end_date'], #end-date"
    )
    end_date_field.clear()
    end_date_field.send_keys(end_date)
    context.season_end_date = end_date


@when('je saisis la localisation "{location}"')
def step_enter_location(context, location):
    """Saisir la localisation"""
    location_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='location'], input[name='location'], #location"
    )
    location_field.clear()
    location_field.send_keys(location)
    context.season_location = location


@when('je télécharge une photo de couverture "{filename}"')
def step_upload_cover_photo(context, filename):
    """Télécharger une photo de couverture"""
    file_input = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='cover-photo'], input[type='file'], #cover-photo"
    )
    
    # Simuler le téléchargement (chemin fictif pour le test)
    file_input.send_keys(f"/tmp/{filename}")
    context.cover_photo = filename


@when('je clique sur "Créer la saison"')
def step_click_create_season_submit(context):
    """Soumettre la création de saison"""
    submit_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='submit-season'], button[type='submit'], .create-season-submit"
    )
    submit_btn.click()


@when('je clique sur "Rejoindre une saison"')
def step_click_join_season(context):
    """Cliquer sur rejoindre une saison"""
    join_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='join-season'], .join-season-btn, #join-season"
    )
    join_btn.click()
    
    # Attendre que le formulaire d'invitation s'ouvre
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='join-form'], .join-season-form"))
    )


@when('je saisis le code d\'invitation "{code}"')
def step_enter_invitation_code(context, code):
    """Saisir le code d'invitation"""
    code_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='invitation-code'], input[name='invitation_code'], #invitation-code"
    )
    code_field.clear()
    code_field.send_keys(code)
    context.entered_invitation_code = code


@when('je clique sur "Rejoindre"')
def step_click_join_submit(context):
    """Soumettre la demande de participation"""
    join_submit_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='submit-join'], button[type='submit'], .join-submit"
    )
    join_submit_btn.click()


@when('je modifie le titre en "{new_title}"')
def step_modify_season_title(context, new_title):
    """Modifier le titre de la saison"""
    edit_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='edit-season'], .edit-season, .edit-btn"
    )
    edit_btn.click()
    
    title_field = context.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='season-title'], #season-title"))
    )
    title_field.clear()
    title_field.send_keys(new_title)
    context.new_season_title = new_title


@when('je sauvegarde les modifications')
def step_save_modifications(context):
    """Sauvegarder les modifications"""
    save_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='save-changes'], .save-btn, button[type='submit']"
    )
    save_btn.click()


@when('je génère un code d\'invitation')
def step_generate_invitation_code(context):
    """Générer un code d'invitation"""
    generate_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='generate-code'], .generate-invitation, #generate-code"
    )
    generate_btn.click()
    
    # Attendre que le code soit généré
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='invitation-code-display'], .invitation-code"))
    )


@when('je supprime la saison')
def step_delete_season(context):
    """Supprimer la saison"""
    delete_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='delete-season'], .delete-season, .delete-btn"
    )
    delete_btn.click()
    
    # Confirmer la suppression
    confirm_btn = context.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='confirm-delete'], .confirm-delete"))
    )
    confirm_btn.click()


# ========== THEN Steps ==========

@then('la saison doit être créée avec succès')
def step_season_created_successfully(context):
    """Vérifier que la saison est créée avec succès"""
    context.wait.until(
        EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='season-created'], .season-success")),
            EC.url_contains("/seasons/"),
            EC.presence_of_element_located((By.CSS_SELECTOR, ".success-notification"))
        )
    )


@then('la saison doit apparaître dans ma liste des saisons')
def step_season_appears_in_list(context):
    """Vérifier que la saison apparaît dans la liste"""
    # Naviguer vers la liste des saisons si nécessaire
    if "/seasons" not in context.driver.current_url:
        context.driver.get(f"{context.base_url}/seasons")
    
    # Vérifier que la saison créée apparaît
    season_title = getattr(context, 'season_title', 'Vacances')
    context.wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".seasons-list, .season-item"),
            season_title
        )
    )


@then('je dois être ajouté à la saison')
def step_should_be_added_to_season(context):
    """Vérifier que l'utilisateur est ajouté à la saison"""
    # Vérifier la confirmation d'ajout
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".join-success, .welcome-message"))
    )
    
    # Vérifier l'accès à la saison
    season_dashboard = context.driver.find_elements(
        By.CSS_SELECTOR,
        "[data-testid='season-dashboard'], .season-content, .season-view"
    )
    assert len(season_dashboard) > 0, "Accès à la saison non confirmé"


@then('je dois voir les informations de la saison')
def step_should_see_season_info(context):
    """Vérifier que les informations de la saison sont visibles"""
    # Vérifier les éléments d'information de la saison
    season_info_elements = [
        ".season-title",
        ".season-dates",
        ".season-location",
        ".season-members"
    ]
    
    for element_class in season_info_elements:
        info_element = context.driver.find_elements(By.CSS_SELECTOR, element_class)
        assert len(info_element) > 0, f"Élément {element_class} non trouvé"


@then('les modifications doivent être visibles pour tous les membres')
def step_modifications_visible_to_all(context):
    """Vérifier que les modifications sont visibles par tous"""
    # Rafraîchir pour voir les changements
    context.driver.refresh()
    
    # Vérifier que le nouveau titre est visible
    if hasattr(context, 'new_season_title'):
        context.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".season-title, h1"),
                context.new_season_title
            )
        )


@then('un code d\'invitation unique doit être généré')
def step_unique_invitation_code_generated(context):
    """Vérifier qu'un code d'invitation unique est généré"""
    code_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='invitation-code-display'], .invitation-code"))
    )
    
    invitation_code = code_element.text.strip()
    assert len(invitation_code) >= 6, f"Code d'invitation trop court: {invitation_code}"
    assert invitation_code.isalnum(), f"Code d'invitation avec caractères invalides: {invitation_code}"
    
    context.generated_invitation_code = invitation_code


@then('ce code doit être partageable')
def step_code_should_be_shareable(context):
    """Vérifier que le code est partageable"""
    # Vérifier la présence d'options de partage
    share_options = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".share-code, [data-testid='share-invitation'], .copy-code"
    )
    assert len(share_options) > 0, "Aucune option de partage trouvée"


@then('la saison doit être supprimée définitivement')
def step_season_deleted_permanently(context):
    """Vérifier que la saison est supprimée définitivement"""
    # Vérifier le message de suppression
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".delete-success, .deletion-confirmed"))
    )
    
    # Vérifier que la saison n'apparaît plus dans la liste
    if hasattr(context, 'season_title'):
        season_items = context.driver.find_elements(By.CSS_SELECTOR, ".season-item")
        season_still_present = any(
            context.season_title in item.text for item in season_items
        )
        assert not season_still_present, "La saison apparaît encore dans la liste"


@then('tous les défis de cette saison doivent être archivés')
def step_challenges_archived(context):
    """Vérifier que les défis sont archivés"""
    # Vérifier la mention d'archivage des défis
    archive_message = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".challenges-archived, .archive-notification"
    )
    assert len(archive_message) > 0, "Aucune confirmation d'archivage des défis"


@then('je dois voir le calendrier des "{days}" jours')
def step_should_see_calendar(context, days):
    """Vérifier que le calendrier des jours est visible"""
    calendar_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='season-calendar'], .season-calendar"))
    )
    
    # Vérifier que le nombre de jours correspond
    day_elements = context.driver.find_elements(By.CSS_SELECTOR, ".calendar-day, .day-item")
    expected_days = int(days)
    assert len(day_elements) == expected_days, f"Nombre de jours incorrect: {len(day_elements)} au lieu de {expected_days}"


@then('le jour actuel doit être mis en évidence')
def step_current_day_highlighted(context):
    """Vérifier que le jour actuel est mis en évidence"""
    current_day = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".current-day, .day-current, [data-current='true']"
    )
    assert len(current_day) > 0, "Jour actuel non mis en évidence"
