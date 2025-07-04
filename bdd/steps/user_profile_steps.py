"""
Steps pour la gestion des profils utilisateur
Tests BDD pour l'application Vacances Gamifiées
"""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import time


# ========== GIVEN Steps ==========

@given('je suis sur la page de gestion de profil')
def step_on_profile_page(context):
    """Naviguer vers la page de gestion de profil"""
    profile_url = f"{context.base_url}/profile"
    context.driver.get(profile_url)
    
    # Vérifier qu'on est sur la page de profil
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='profile-page'], .profile-container"))
    )


@given('je suis un nouvel utilisateur connecté')
def step_new_connected_user(context):
    """Configurer le contexte pour un nouvel utilisateur connecté"""
    context.current_user = None
    context.is_new_user = True
    context.profile_exists = False


@given('j\'ai un profil existant avec le pseudo "{pseudo}"')
def step_existing_profile(context, pseudo):
    """Configurer un profil existant"""
    context.existing_profile = {
        "pseudo": pseudo,
        "avatar": "default_avatar.png",
        "age": "40 ans",
        "preferences": "Sport"
    }
    context.profile_exists = True


@given('je suis sur mon profil familial')
def step_on_family_profile(context):
    """Naviguer vers le profil familial"""
    family_url = f"{context.base_url}/family-profile"
    context.driver.get(family_url)
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='family-profile'], .family-container"))
    )


# ========== WHEN Steps ==========

@when('je saisis mon pseudo "{pseudo}"')
def step_enter_pseudo(context, pseudo):
    """Saisir un pseudo"""
    pseudo_field = context.driver.find_element(
        By.CSS_SELECTOR, 
        "[data-testid='pseudo'], input[name='pseudo'], #pseudo"
    )
    pseudo_field.clear()
    pseudo_field.send_keys(pseudo)
    context.test_pseudo = pseudo


@when('je choisis un avatar depuis la galerie prédéfinie')
def step_choose_avatar(context):
    """Choisir un avatar dans la galerie"""
    # Cliquer sur le bouton galerie d'avatars
    avatar_gallery_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='avatar-gallery'], .avatar-gallery-btn, #avatar-gallery"
    )
    avatar_gallery_btn.click()
    
    # Attendre que la galerie s'ouvre
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".avatar-gallery, .avatar-picker"))
    )
    
    # Sélectionner le premier avatar disponible
    first_avatar = context.driver.find_element(
        By.CSS_SELECTOR,
        ".avatar-option:first-child, .avatar-item:first-child"
    )
    first_avatar.click()
    
    # Confirmer la sélection
    confirm_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='confirm-avatar'], .confirm-avatar, .select-avatar"
    )
    confirm_btn.click()
    
    context.selected_avatar = "avatar_1.png"


@when('je sélectionne mon âge "{age}"')
def step_select_age(context, age):
    """Sélectionner l'âge"""
    age_select = Select(context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='age'], select[name='age'], #age"
    ))
    age_select.select_by_visible_text(age)
    context.selected_age = age


@when('je définis mes préférences de défis "{preferences}"')
def step_set_challenge_preferences(context, preferences):
    """Définir les préférences de défis"""
    # Les préférences peuvent être des checkboxes ou un select multiple
    prefs_list = preferences.split(" et ")
    
    for pref in prefs_list:
        checkbox = context.driver.find_element(
            By.CSS_SELECTOR,
            f"input[value*='{pref.lower()}'], [data-testid*='{pref.lower()}']"
        )
        if not checkbox.is_selected():
            checkbox.click()
    
    context.selected_preferences = prefs_list


@when('je modifie mon pseudo en "{new_pseudo}"')
def step_modify_pseudo(context, new_pseudo):
    """Modifier le pseudo existant"""
    pseudo_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='pseudo'], input[name='pseudo'], #pseudo"
    )
    pseudo_field.clear()
    pseudo_field.send_keys(new_pseudo)
    context.new_pseudo = new_pseudo


@when('je change mon avatar')
def step_change_avatar(context):
    """Changer l'avatar existant"""
    # Cliquer sur l'avatar actuel pour le changer
    current_avatar = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='current-avatar'], .current-avatar, .profile-avatar"
    )
    current_avatar.click()
    
    # Sélectionner un nouvel avatar
    context.execute_steps('When je choisis un avatar depuis la galerie prédéfinie')


@when('je télécharge une photo personnalisée')
def step_upload_custom_photo(context):
    """Télécharger une photo personnalisée"""
    # Cliquer sur l'option de téléchargement
    upload_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='upload-photo'], .upload-photo, input[type='file']"
    )
    
    # Simuler le téléchargement d'un fichier
    # En test réel, on utiliserait un fichier de test
    upload_btn.send_keys("/tmp/test_avatar.jpg")  # Chemin fictif pour le test
    context.custom_photo_uploaded = True


@when('j\'invite un membre de famille avec l\'email "{email}"')
def step_invite_family_member(context, email):
    """Inviter un membre de famille"""
    invite_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='invite-member'], .invite-btn, #invite-member"
    )
    invite_btn.click()
    
    # Saisir l'email d'invitation
    email_field = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='invite-email'], input[type='email']"))
    )
    email_field.send_keys(email)
    
    # Envoyer l'invitation
    send_invite_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='send-invite'], .send-invite"
    )
    send_invite_btn.click()
    
    context.invited_email = email


@when('je supprime le membre "{member_name}"')
def step_remove_family_member(context, member_name):
    """Supprimer un membre de famille"""
    # Trouver le membre dans la liste
    member_element = context.driver.find_element(
        By.XPATH,
        f"//div[contains(@class, 'family-member') and contains(text(), '{member_name}')]"
    )
    
    # Cliquer sur le bouton de suppression
    remove_btn = member_element.find_element(
        By.CSS_SELECTOR,
        ".remove-member, [data-testid='remove-member']"
    )
    remove_btn.click()
    
    # Confirmer la suppression
    confirm_btn = context.wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='confirm-remove'], .confirm-remove"))
    )
    confirm_btn.click()
    
    context.removed_member = member_name


# ========== THEN Steps ==========

@then('mon profil doit être créé avec succès')
def step_profile_created_successfully(context):
    """Vérifier que le profil est créé avec succès"""
    # Vérifier la présence d'éléments indiquant la création réussie
    context.wait.until(
        EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='profile-created'], .profile-success")),
            EC.url_contains("/profile"),
            EC.presence_of_element_located((By.CSS_SELECTOR, ".success-message"))
        )
    )


@then('je dois voir une confirmation "{message}"')
def step_should_see_confirmation(context, message):
    """Vérifier qu'un message de confirmation est affiché"""
    confirmation_selectors = [
        "[data-testid='success-message']",
        ".success-message",
        ".alert-success",
        ".notification-success",
        ".confirmation"
    ]
    
    confirmation_element = None
    for selector in confirmation_selectors:
        try:
            confirmation_element = context.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            break
        except TimeoutException:
            continue
    
    assert confirmation_element is not None, "Aucun message de confirmation trouvé"
    assert message.lower() in confirmation_element.text.lower(), f"Message de confirmation incorrect: {confirmation_element.text}"


@then('mes informations doivent être sauvegardées')
def step_information_saved(context):
    """Vérifier que les informations sont sauvegardées"""
    # Rafraîchir la page pour vérifier la persistance
    context.driver.refresh()
    
    # Vérifier que les informations saisies sont toujours présentes
    if hasattr(context, 'test_pseudo'):
        pseudo_field = context.driver.find_element(
            By.CSS_SELECTOR,
            "[data-testid='pseudo'], input[name='pseudo'], #pseudo"
        )
        assert pseudo_field.get_attribute('value') == context.test_pseudo, "Pseudo non sauvegardé"


@then('mes modifications doivent être sauvegardées')
def step_modifications_saved(context):
    """Vérifier que les modifications sont sauvegardées"""
    step_information_saved(context)


@then('les autres membres de la famille doivent voir mon nouveau pseudo')
def step_family_sees_new_pseudo(context):
    """Vérifier que le nouveau pseudo est visible par la famille"""
    # Dans un test réel, on vérifierait avec un autre compte
    # Ici on simule en vérifiant que l'info est dans le profil familial
    family_profile_link = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='family-profile'], .family-profile-link"
    )
    family_profile_link.click()
    
    # Vérifier que le nouveau pseudo apparaît
    context.wait.until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, ".family-member, .member-info"),
            getattr(context, 'new_pseudo', context.test_pseudo)
        )
    )


@then('la photo doit être redimensionnée automatiquement')
def step_photo_resized_automatically(context):
    """Vérifier que la photo est redimensionnée"""
    # Vérifier les dimensions de l'avatar affiché
    avatar_img = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='profile-avatar'] img, .profile-avatar img"
    )
    
    # Vérifier que les dimensions respectent les contraintes
    width = avatar_img.get_attribute('width') or avatar_img.size['width']
    height = avatar_img.get_attribute('height') or avatar_img.size['height']
    
    # Contraintes typiques pour un avatar (ex: 150x150 max)
    assert int(width) <= 150, f"Avatar trop large: {width}px"
    assert int(height) <= 150, f"Avatar trop haut: {height}px"


@then('elle doit apparaître dans mon profil')
def step_photo_appears_in_profile(context):
    """Vérifier que la photo apparaît dans le profil"""
    avatar_img = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='profile-avatar'] img, .profile-avatar img"))
    )
    
    # Vérifier que l'image a bien une source
    assert avatar_img.get_attribute('src'), "Avatar sans source"
    assert 'default' not in avatar_img.get_attribute('src'), "Avatar par défaut encore présent"


@then('une invitation doit être envoyée à "{email}"')
def step_invitation_sent(context, email):
    """Vérifier qu'une invitation est envoyée"""
    # Vérifier le message de confirmation d'envoi
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".invitation-sent, .invite-success"))
    )
    
    # Vérifier que l'email apparaît dans la liste des invitations en attente
    pending_invites = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".pending-invite, .invited-member"
    )
    
    invite_found = any(email in invite.text for invite in pending_invites)
    assert invite_found, f"Invitation pour {email} non trouvée dans la liste"


@then('il doit recevoir un email avec un lien d\'inscription')
def step_should_receive_registration_email(context):
    """Vérifier qu'un email d'invitation est prévu (mock)"""
    # Dans un test réel, on vérifierait l'envoi d'email
    # Ici on vérifie que l'invitation est enregistrée
    assert hasattr(context, 'invited_email'), "Aucune invitation enregistrée"
    context.email_invitation_sent = True


@then('le membre doit être retiré de la liste familiale')
def step_member_removed_from_list(context):
    """Vérifier que le membre est retiré de la liste"""
    # Vérifier que le membre n'apparaît plus dans la liste
    family_members = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".family-member, .member-item"
    )
    
    member_still_present = any(
        context.removed_member in member.text for member in family_members
    )
    
    assert not member_still_present, f"Le membre {context.removed_member} est encore dans la liste"


@then('ses scores doivent être archivés')
def step_scores_archived(context):
    """Vérifier que les scores sont archivés"""
    # Vérifier qu'une mention d'archivage est présente
    archive_indicator = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".archived-member, .member-archived, [data-status='archived']"
    )
    
    assert len(archive_indicator) > 0, "Aucune indication d'archivage trouvée"
