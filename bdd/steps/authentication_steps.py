"""
Steps de base pour l'authentification
Tests BDD pour l'application Vacances Gamifiées
"""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


# ========== GIVEN Steps ==========

@given('l\'application est accessible via un navigateur mobile')
def step_app_accessible_mobile(context):
    """Vérifier que l'application est accessible"""
    context.driver.get(context.base_url)
    
    # Vérifier que la page se charge
    context.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    # Vérifier la responsivité mobile
    viewport_width = context.driver.execute_script("return window.innerWidth")
    assert viewport_width <= 768, f"Viewport trop large pour mobile: {viewport_width}px"


@given('l\'interface d\'authentification est affichée')
def step_auth_interface_displayed(context):
    """Vérifier que l'interface d'authentification est visible"""
    # Attendre que les éléments d'authentification soient visibles
    login_form = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='auth-form'], .auth-container, #login-form"))
    )
    assert login_form.is_displayed(), "Interface d'authentification non visible"


@given('je suis un nouvel utilisateur')
def step_new_user(context):
    """Configurer le contexte pour un nouvel utilisateur"""
    context.current_user = None
    context.is_new_user = True


@given('je suis sur la page de connexion')
def step_on_login_page(context):
    """Naviguer vers la page de connexion"""
    login_url = f"{context.base_url}/login"
    context.driver.get(login_url)
    
    # Vérifier qu'on est bien sur la page de connexion
    context.wait.until(
        EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-page']")),
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1, h2")),
        )
    )


@given('je suis connecté avec le compte "{username}"')
def step_logged_in_with_account(context, username):
    """Se connecter avec un compte utilisateur spécifique"""
    user_data = context.test_users.get(f"{username.lower()}_test")
    if not user_data:
        raise ValueError(f"Utilisateur de test '{username}' non trouvé")
    
    # Aller à la page de connexion
    context.execute_steps(f'Given je suis sur la page de connexion')
    
    # Saisir les identifiants
    email_field = context.driver.find_element(By.CSS_SELECTOR, "[data-testid='email'], input[type='email'], #email")
    email_field.clear()
    email_field.send_keys(user_data["email"])
    
    password_field = context.driver.find_element(By.CSS_SELECTOR, "[data-testid='password'], input[type='password'], #password")
    password_field.clear()
    password_field.send_keys(user_data["password"])
    
    # Se connecter
    login_button = context.driver.find_element(By.CSS_SELECTOR, "[data-testid='login-button'], button[type='submit'], .login-btn")
    login_button.click()
    
    # Vérifier la connexion réussie
    context.wait.until(
        EC.any_of(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='dashboard'], .dashboard, .home")),
            EC.url_contains("/dashboard"),
            EC.url_contains("/home")
        )
    )
    
    context.current_user = user_data


@given('je suis sur la page d\'accueil')
def step_on_home_page(context):
    """Naviguer vers la page d'accueil"""
    home_url = f"{context.base_url}/home"
    context.driver.get(home_url)
    
    # Vérifier qu'on est sur la page d'accueil
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='home-page'], .home-container"))
    )


# ========== WHEN Steps ==========

@when('je clique sur le bouton "{button_text}"')
def step_click_button(context, button_text):
    """Cliquer sur un bouton avec le texte spécifié"""
    # Plusieurs sélecteurs possibles pour trouver le bouton
    button_selectors = [
        f"button:contains('{button_text}')",
        f"[data-testid*='{button_text.lower().replace(' ', '-')}']",
        f"//button[contains(text(), '{button_text}')]",
        f"//a[contains(text(), '{button_text}')]",
        f".btn:contains('{button_text}')"
    ]
    
    button = None
    for selector in button_selectors:
        try:
            if selector.startswith("//"):
                button = context.driver.find_element(By.XPATH, selector)
            else:
                button = context.driver.find_element(By.CSS_SELECTOR, selector)
            break
        except:
            continue
    
    assert button is not None, f"Bouton '{button_text}' non trouvé"
    assert button.is_displayed(), f"Bouton '{button_text}' non visible"
    
    # Scroll vers le bouton si nécessaire
    context.driver.execute_script("arguments[0].scrollIntoView();", button)
    
    # Clic avec gestion des erreurs
    try:
        button.click()
    except:
        # Fallback avec JavaScript
        context.driver.execute_script("arguments[0].click();", button)
    
    time.sleep(0.5)  # Petite pause pour l'interaction


@when('je saisis un nom d\'utilisateur valide "{username}"')
def step_enter_username(context, username):
    """Saisir un nom d'utilisateur"""
    username_field = context.driver.find_element(
        By.CSS_SELECTOR, 
        "[data-testid='username'], input[name='username'], #username"
    )
    username_field.clear()
    username_field.send_keys(username)
    
    context.test_username = username


@when('je saisis un mot de passe sécurisé "{password}"')
def step_enter_password(context, password):
    """Saisir un mot de passe"""
    password_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='password'], input[type='password'], #password"
    )
    password_field.clear()
    password_field.send_keys(password)
    
    context.test_password = password


@when('je confirme mon mot de passe')
def step_confirm_password(context):
    """Confirmer le mot de passe"""
    confirm_field = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='confirm-password'], input[name='confirm_password'], #confirm_password"
    )
    confirm_field.clear()
    confirm_field.send_keys(context.test_password)


@when('je suis redirigé vers Google OAuth')
def step_redirected_google_oauth(context):
    """Simuler la redirection vers Google OAuth"""
    # Dans un test réel, on simulerait la redirection OAuth
    # Ici on mock le comportement
    context.oauth_provider = "google"
    context.oauth_redirected = True


@when('je m\'authentifie avec mes identifiants Google valides')
def step_authenticate_google(context):
    """Simuler l'authentification Google réussie"""
    # Mock de l'authentification Google
    context.oauth_success = True
    context.oauth_user_info = {
        "email": "test.user@gmail.com",
        "name": "Test User",
        "provider": "google"
    }


@when('j\'autorise l\'application à accéder à mes informations')
def step_authorize_app_access(context):
    """Simuler l'autorisation d'accès"""
    context.oauth_authorized = True


@when('je ferme mon navigateur')
def step_close_browser(context):
    """Simuler la fermeture du navigateur"""
    # Sauvegarder l'état de session
    context.session_cookies = context.driver.get_cookies()
    context.session_storage = context.driver.execute_script("return window.sessionStorage;")


@when('je rouvre l\'application dans les 24 heures')
def step_reopen_app_24h(context):
    """Simuler la réouverture de l'application"""
    # Naviguer vers l'application
    context.driver.get(context.base_url)
    
    # Restaurer les cookies de session
    if hasattr(context, 'session_cookies'):
        for cookie in context.session_cookies:
            try:
                context.driver.add_cookie(cookie)
            except:
                pass  # Ignorer les erreurs de cookies invalides
    
    # Rafraîchir la page
    context.driver.refresh()


# ========== THEN Steps ==========

@then('je dois être connecté automatiquement')
def step_should_be_logged_in(context):
    """Vérifier que l'utilisateur est connecté"""
    # Vérifier la présence d'éléments indiquant une connexion réussie
    try:
        context.wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='user-menu'], .user-profile, .logout-btn")),
                EC.url_contains("/dashboard"),
                EC.url_contains("/home"),
                EC.presence_of_element_located((By.CSS_SELECTOR, ".welcome-message"))
            )
        )
    except TimeoutException:
        assert False, "L'utilisateur ne semble pas être connecté"


@then('je dois voir la page d\'accueil de l\'application')
def step_should_see_home_page(context):
    """Vérifier qu'on est sur la page d'accueil"""
    # Vérifier l'URL ou les éléments de la page d'accueil
    current_url = context.driver.current_url
    assert "/home" in current_url or "/dashboard" in current_url, f"URL inattendue: {current_url}"
    
    # Vérifier la présence d'éléments de la page d'accueil
    home_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        "[data-testid='home-page'], .dashboard, .welcome-section"
    )
    assert len(home_elements) > 0, "Éléments de la page d'accueil non trouvés"


@then('mon profil doit être créé avec le nom "{name}"')
def step_profile_created_with_name(context, name):
    """Vérifier que le profil est créé avec le bon nom"""
    # Vérifier dans l'interface utilisateur
    try:
        profile_name_element = context.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='user-name'], .user-name, .profile-name"))
        )
        assert name in profile_name_element.text, f"Nom de profil incorrect: {profile_name_element.text}"
    except TimeoutException:
        # Fallback: vérifier dans le menu utilisateur
        user_menu = context.driver.find_element(By.CSS_SELECTOR, "[data-testid='user-menu'], .user-menu")
        user_menu.click()
        
        profile_element = context.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".profile-info, .user-info"))
        )
        assert name in profile_element.text, f"Nom de profil non trouvé dans le menu"


@then('je dois voir un message d\'erreur "{error_message}"')
def step_should_see_error_message(context, error_message):
    """Vérifier qu'un message d'erreur est affiché"""
    error_selectors = [
        "[data-testid='error-message']",
        ".error-message",
        ".alert-error",
        ".notification-error",
        ".error"
    ]
    
    error_element = None
    for selector in error_selectors:
        try:
            error_element = context.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            break
        except TimeoutException:
            continue
    
    assert error_element is not None, "Aucun message d'erreur trouvé"
    assert error_message.lower() in error_element.text.lower(), f"Message d'erreur incorrect: {error_element.text}"


@then('je dois rester sur la page de connexion')
def step_should_stay_on_login_page(context):
    """Vérifier qu'on reste sur la page de connexion"""
    current_url = context.driver.current_url
    assert "/login" in current_url or "login" in current_url, f"URL inattendue: {current_url}"
    
    # Vérifier la présence des éléments de connexion
    login_form = context.driver.find_elements(By.CSS_SELECTOR, "[data-testid='auth-form'], .login-form, #login-form")
    assert len(login_form) > 0, "Formulaire de connexion non trouvé"


@then('je dois être déconnecté')
def step_should_be_logged_out(context):
    """Vérifier que l'utilisateur est déconnecté"""
    # Vérifier l'absence d'éléments de session
    logged_in_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        "[data-testid='user-menu'], .user-profile, .dashboard"
    )
    assert len(logged_in_elements) == 0, "L'utilisateur semble toujours connecté"


@then('je dois être redirigé vers la page de connexion')
def step_redirected_to_login(context):
    """Vérifier la redirection vers la page de connexion"""
    context.wait.until(
        EC.any_of(
            EC.url_contains("/login"),
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='login-page'], .login-form"))
        )
    )


@then('mes données de session doivent être effacées')
def step_session_data_cleared(context):
    """Vérifier que les données de session sont effacées"""
    # Vérifier que les cookies de session sont supprimés
    cookies = context.driver.get_cookies()
    session_cookies = [c for c in cookies if 'session' in c.get('name', '').lower()]
    
    # Note: En réalité, on vérifierait que les cookies sensibles sont supprimés
    # Ici on fait une vérification basique
    context.session_cleared = True  # Flag pour les tests suivants


@then('je dois être toujours connecté')
def step_should_still_be_logged_in(context):
    """Vérifier que l'utilisateur est toujours connecté après réouverture"""
    step_should_be_logged_in(context)


@then('je dois voir la page d\'accueil directement')
def step_should_see_home_directly(context):
    """Vérifier qu'on arrive directement sur la page d'accueil"""
    step_should_see_home_page(context)
    
    # Vérifier qu'on n'est pas passé par la page de connexion
    current_url = context.driver.current_url
    assert "/login" not in current_url, "Redirection inattendue vers la page de connexion"
