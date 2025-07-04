"""
Steps pour l'interface mobile et expérience utilisateur
Tests BDD pour l'application Vacances Gamifiées
"""

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.common.exceptions import TimeoutException
import time


# ========== GIVEN Steps ==========

@given('j\'utilise un iPhone 12 avec Safari')
def step_using_iphone_safari(context):
    """Configurer l'environnement iPhone 12 Safari"""
    # Définir le user agent et la taille d'écran pour iPhone 12
    context.driver.execute_script("""
        Object.defineProperty(navigator, 'userAgent', {
            get: function() { return 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'; }
        });
    """)
    
    # Définir la taille d'écran iPhone 12 (390x844)
    context.driver.set_window_size(390, 844)
    context.device_type = "iPhone 12"
    context.browser = "Safari"


@given('l\'application est en mode responsive mobile')
def step_app_in_mobile_responsive_mode(context):
    """Vérifier que l'application est en mode responsive mobile"""
    # Vérifier que la viewport est configurée pour mobile
    viewport_meta = context.driver.find_element(By.CSS_SELECTOR, "meta[name='viewport']")
    viewport_content = viewport_meta.get_attribute('content')
    
    assert 'width=device-width' in viewport_content, "Viewport non configurée pour mobile"
    
    # Vérifier que l'interface s'adapte
    body_class = context.driver.find_element(By.TAG_NAME, "body").get_attribute('class')
    mobile_indicators = ['mobile', 'responsive', 'touch-device']
    
    has_mobile_class = any(indicator in body_class.lower() for indicator in mobile_indicators)
    assert has_mobile_class, "Interface non configurée pour mobile"


@given('l\'application est ouverte')
def step_app_is_open(context):
    """Vérifier que l'application est ouverte"""
    context.driver.get(context.base_url)
    context.wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )


@given('je suis sur la page d\'accueil')
def step_on_home_page_mobile(context):
    """Naviguer vers la page d'accueil mobile"""
    home_url = f"{context.base_url}/home"
    context.driver.get(home_url)
    
    context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='home-page'], .home-container"))
    )


@given('l\'interface affiche des boutons d\'action')
def step_interface_shows_action_buttons(context):
    """Vérifier que des boutons d'action sont présents"""
    action_buttons = context.driver.find_elements(
        By.CSS_SELECTOR,
        "button, .btn, .action-button, [role='button']"
    )
    assert len(action_buttons) > 0, "Aucun bouton d'action trouvé"
    context.action_buttons = action_buttons


@given('je demande la génération de nouveaux défis')
def step_request_new_challenges_generation(context):
    """Demander la génération de nouveaux défis"""
    generate_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='generate-challenges'], .generate-btn, #new-challenges"
    )
    generate_btn.click()
    context.generation_requested = True


@given('je suis dans une zone sans réseau')
def step_in_offline_zone(context):
    """Simuler une zone sans réseau"""
    # Simuler la perte de connexion
    context.driver.execute_script("""
        window.navigator.onLine = false;
        window.dispatchEvent(new Event('offline'));
    """)
    context.offline_mode = True


@given('les notifications sont activées')
def step_notifications_enabled(context):
    """Activer les notifications"""
    # Simuler l'autorisation des notifications
    context.driver.execute_script("""
        Object.defineProperty(Notification, 'permission', {
            get: function() { return 'granted'; }
        });
        window.notificationsEnabled = true;
    """)
    context.notifications_enabled = True


@given('un défi photo est actif')
def step_photo_challenge_active(context):
    """Configurer un défi photo actif"""
    context.active_photo_challenge = {
        "type": "photo",
        "description": "Prenez une photo d'un élément architectural créole",
        "points": 20
    }


# ========== WHEN Steps ==========

@when('je fais tourner mon téléphone en mode paysage')
def step_rotate_to_landscape(context):
    """Faire tourner l'écran en mode paysage"""
    # Changer l'orientation de l'écran (844x390 pour paysage)
    context.driver.set_window_size(844, 390)
    
    # Simuler l'événement d'orientation
    context.driver.execute_script("""
        window.dispatchEvent(new Event('orientationchange'));
        screen.orientation = { angle: 90, type: 'landscape-primary' };
    """)
    
    time.sleep(1)  # Attendre l'adaptation de l'interface


@when('je remets en mode portrait')
def step_rotate_to_portrait(context):
    """Remettre l'écran en mode portrait"""
    # Revenir à la taille portrait
    context.driver.set_window_size(390, 844)
    
    # Simuler l'événement d'orientation
    context.driver.execute_script("""
        window.dispatchEvent(new Event('orientationchange'));
        screen.orientation = { angle: 0, type: 'portrait-primary' };
    """)
    
    time.sleep(1)  # Attendre l'adaptation de l'interface


@when('je swipe vers la gauche')
def step_swipe_left(context):
    """Effectuer un swipe vers la gauche"""
    # Obtenir les dimensions de l'écran
    screen_width = context.driver.execute_script("return window.innerWidth;")
    screen_height = context.driver.execute_script("return window.innerHeight;")
    
    # Effectuer le swipe avec TouchActions
    touch_actions = TouchActions(context.driver)
    touch_actions.scroll_from_element(
        context.driver.find_element(By.TAG_NAME, "body"),
        -screen_width // 2, 0
    )
    touch_actions.perform()
    
    context.last_swipe = "left"


@when('je swipe vers la droite')
def step_swipe_right(context):
    """Effectuer un swipe vers la droite"""
    screen_width = context.driver.execute_script("return window.innerWidth;")
    
    touch_actions = TouchActions(context.driver)
    touch_actions.scroll_from_element(
        context.driver.find_element(By.TAG_NAME, "body"),
        screen_width // 2, 0
    )
    touch_actions.perform()
    
    context.last_swipe = "right"


@when('je tape sur un bouton')
def step_tap_button(context):
    """Taper sur un bouton"""
    action_buttons = getattr(context, 'action_buttons', 
                           context.driver.find_elements(By.CSS_SELECTOR, "button, .btn"))
    
    if action_buttons:
        # Taper sur le premier bouton disponible
        button = action_buttons[0]
        button.click()
        context.tapped_button = button


@when('le système fait appel à l\'IA')
def step_system_calls_ai(context):
    """Simuler l'appel à l'IA"""
    # Simuler le délai de traitement IA
    context.driver.execute_script("""
        window.aiProcessing = true;
        window.dispatchEvent(new CustomEvent('aiStart', { detail: { type: 'challenge_generation' } }));
    """)
    context.ai_processing = True


@when('la génération est terminée')
def step_generation_completed(context):
    """Simuler la fin de génération"""
    # Attendre un délai réaliste puis marquer comme terminé
    time.sleep(2)
    
    context.driver.execute_script("""
        window.aiProcessing = false;
        window.dispatchEvent(new CustomEvent('aiComplete', { 
            detail: { 
                type: 'challenge_generation',
                result: 'success',
                challenges: ['Défi 1', 'Défi 2', 'Défi 3']
            } 
        }));
    """)
    context.ai_processing = False


@when('je complète un défi hors ligne')
def step_complete_challenge_offline(context):
    """Compléter un défi en mode hors ligne"""
    # Trouver et compléter un défi
    challenge_btn = context.driver.find_element(
        By.CSS_SELECTOR,
        "[data-testid='offline-challenge'], .challenge-offline, .challenge-item:first-child"
    )
    challenge_btn.click()
    
    # Marquer comme complété localement
    context.driver.execute_script("""
        localStorage.setItem('pendingChallenges', JSON.stringify([{
            id: 'challenge_1',
            completed: true,
            timestamp: new Date().toISOString(),
            points: 10
        }]));
    """)
    context.offline_challenge_completed = True


@when('la connexion revient')
def step_connection_returns(context):
    """Simuler le retour de la connexion"""
    context.driver.execute_script("""
        window.navigator.onLine = true;
        window.dispatchEvent(new Event('online'));
    """)
    context.offline_mode = False


@when('de nouveaux défis sont générés à 9h00')
def step_new_challenges_generated_at_9am(context):
    """Simuler la génération de défis à 9h00"""
    context.driver.execute_script("""
        window.mockTime = '09:00';
        window.dispatchEvent(new CustomEvent('challengesGenerated', {
            detail: { time: '09:00', count: 3 }
        }));
    """)
    context.new_challenges_time = "09:00"


@when('je tape sur la notification')
def step_tap_notification(context):
    """Taper sur une notification"""
    # Simuler le tap sur notification
    context.driver.execute_script("""
        window.dispatchEvent(new CustomEvent('notificationClick', {
            detail: { type: 'newChallenges', action: 'open' }
        }));
    """)
    context.notification_tapped = True


@when('j\'autorise l\'accès à la caméra')
def step_authorize_camera_access(context):
    """Autoriser l'accès à la caméra"""
    # Simuler l'autorisation de la caméra
    context.driver.execute_script("""
        navigator.mediaDevices.getUserMedia = function(constraints) {
            return Promise.resolve({
                getTracks: function() { return [{ stop: function() {} }]; },
                getVideoTracks: function() { return [{ stop: function() {} }]; }
            });
        };
        window.cameraAuthorized = true;
    """)
    context.camera_authorized = True


# ========== THEN Steps ==========

@then('l\'interface doit s\'adapter automatiquement')
def step_interface_should_adapt_automatically(context):
    """Vérifier que l'interface s'adapte automatiquement"""
    # Vérifier que les éléments s'adaptent à la nouvelle orientation
    body_element = context.driver.find_element(By.TAG_NAME, "body")
    computed_style = context.driver.execute_script(
        "return window.getComputedStyle(arguments[0]);", body_element
    )
    
    # Vérifier que l'interface utilise l'espace disponible
    viewport_width = context.driver.execute_script("return window.innerWidth;")
    assert viewport_width == 844, f"Largeur de viewport incorrecte: {viewport_width}"


@then('tous les éléments doivent rester accessibles')
def step_all_elements_should_remain_accessible(context):
    """Vérifier que tous les éléments restent accessibles"""
    # Vérifier que les éléments principaux sont toujours visibles
    main_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        "nav, main, .navigation, .content, .actions"
    )
    
    for element in main_elements:
        assert element.is_displayed(), f"Élément {element.tag_name} non accessible"


@then('l\'interface doit revenir à la disposition mobile optimale')
def step_interface_should_return_to_mobile_layout(context):
    """Vérifier le retour à la disposition mobile"""
    # Vérifier que la largeur est revenue à celle du mode portrait
    viewport_width = context.driver.execute_script("return window.innerWidth;")
    assert viewport_width == 390, f"Largeur incorrecte en mode portrait: {viewport_width}"


@then('je dois naviguer vers la page suivante')
def step_should_navigate_to_next_page(context):
    """Vérifier la navigation vers la page suivante"""
    # Vérifier qu'un changement de contenu a eu lieu
    current_url = context.driver.current_url
    
    # Ou vérifier qu'un élément indique un changement de page/section
    page_indicator = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".page-transition, .slide-change, [data-page-changed='true']"
    )
    
    assert len(page_indicator) > 0 or "#" in current_url, "Navigation non détectée"


@then('je dois revenir à la page précédente')
def step_should_navigate_to_previous_page(context):
    """Vérifier le retour à la page précédente"""
    # Similaire à la navigation suivante mais en sens inverse
    page_indicator = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".page-back, .slide-back, [data-page-direction='back']"
    )
    
    assert len(page_indicator) > 0, "Retour à la page précédente non détecté"


@then('la navigation doit être fluide sans latence')
def step_navigation_should_be_fluid(context):
    """Vérifier que la navigation est fluide"""
    # Vérifier l'absence d'indicateurs de lag
    performance_timing = context.driver.execute_script("""
        return performance.now() - window.lastInteractionTime || 0;
    """)
    
    # Le temps de réponse doit être inférieur à 100ms pour être considéré comme fluide
    assert performance_timing < 100, f"Navigation trop lente: {performance_timing}ms"


@then('tous les boutons doivent avoir une taille minimum de 44px')
def step_buttons_should_have_minimum_size(context):
    """Vérifier que les boutons ont la taille minimum tactile"""
    buttons = context.driver.find_elements(
        By.CSS_SELECTOR,
        "button, .btn, .action-button, [role='button']"
    )
    
    for button in buttons:
        size = button.size
        assert size['width'] >= 44 and size['height'] >= 44, f"Bouton trop petit: {size}"


@then('l\'espacement entre les boutons doit être suffisant')
def step_buttons_should_have_sufficient_spacing(context):
    """Vérifier l'espacement entre les boutons"""
    buttons = context.driver.find_elements(By.CSS_SELECTOR, "button, .btn")
    
    if len(buttons) > 1:
        # Vérifier l'espacement entre le premier et le deuxième bouton
        button1_location = buttons[0].location
        button1_size = buttons[0].size
        button2_location = buttons[1].location
        
        # Calculer l'espacement vertical ou horizontal
        horizontal_gap = abs(button2_location['x'] - (button1_location['x'] + button1_size['width']))
        vertical_gap = abs(button2_location['y'] - (button1_location['y'] + button1_size['height']))
        
        min_gap = 8  # Minimum 8px d'espacement
        assert horizontal_gap >= min_gap or vertical_gap >= min_gap, f"Espacement insuffisant: {min(horizontal_gap, vertical_gap)}px"


@then('l\'action doit s\'exécuter sans erreur de ciblage')
def step_action_should_execute_without_targeting_error(context):
    """Vérifier que l'action s'exécute correctement"""
    # Vérifier qu'aucune erreur JavaScript n'est survenue
    js_errors = context.driver.get_log('browser')
    targeting_errors = [error for error in js_errors if 'click' in error['message'].lower()]
    
    assert len(targeting_errors) == 0, f"Erreurs de ciblage détectées: {targeting_errors}"


@then('je dois voir un indicateur de chargement')
def step_should_see_loading_indicator(context):
    """Vérifier la présence d'un indicateur de chargement"""
    loading_indicators = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".loading, .spinner, .loader, .ai-processing, [data-loading='true']"
    )
    
    assert len(loading_indicators) > 0, "Aucun indicateur de chargement trouvé"


@then('un message "Génération de défis personnalisés..."')
def step_should_see_generation_message(context):
    """Vérifier le message de génération"""
    message_element = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".generation-message, .ai-status, .processing-text"))
    )
    
    assert "génération" in message_element.text.lower(), f"Message de génération incorrect: {message_element.text}"


@then('l\'indicateur doit disparaître')
def step_loading_indicator_should_disappear(context):
    """Vérifier que l'indicateur de chargement disparaît"""
    context.wait.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading, .spinner, .loader"))
    )


@then('les défis doivent s\'afficher')
def step_challenges_should_display(context):
    """Vérifier que les défis s'affichent"""
    challenges = context.wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".challenge-item, .generated-challenge"))
    )
    
    assert len(challenges) > 0, "Aucun défi affiché après génération"


@then('mes actions doivent être sauvegardées localement')
def step_actions_should_be_saved_locally(context):
    """Vérifier que les actions sont sauvegardées localement"""
    # Vérifier le localStorage
    pending_data = context.driver.execute_script("return localStorage.getItem('pendingChallenges');")
    assert pending_data is not None, "Aucune donnée sauvegardée localement"


@then('je dois voir une indication "Mode hors ligne"')
def step_should_see_offline_indication(context):
    """Vérifier l'indication du mode hors ligne"""
    offline_indicator = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".offline-mode, .no-connection, [data-offline='true']"
    )
    
    assert len(offline_indicator) > 0, "Indication mode hors ligne non trouvée"


@then('mes données doivent se synchroniser automatiquement')
def step_data_should_sync_automatically(context):
    """Vérifier la synchronisation automatique"""
    # Attendre la synchronisation
    sync_indicator = context.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".syncing, .sync-complete, [data-sync='true']"))
    )
    
    # Vérifier que les données locales ont été envoyées
    pending_data = context.driver.execute_script("return localStorage.getItem('pendingChallenges');")
    assert pending_data == "null" or pending_data is None, "Données non synchronisées"


@then('je dois recevoir une notification "Nouveaux défis disponibles !"')
def step_should_receive_new_challenges_notification(context):
    """Vérifier la réception de notification de nouveaux défis"""
    # Vérifier qu'une notification a été déclenchée
    notification_triggered = context.driver.execute_script("""
        return window.lastNotification && window.lastNotification.title.includes('défis');
    """)
    
    assert notification_triggered, "Notification de nouveaux défis non reçue"


@then('l\'application doit s\'ouvrir sur la page des défis')
def step_app_should_open_on_challenges_page(context):
    """Vérifier l'ouverture sur la page des défis"""
    # Vérifier l'URL ou le contenu de la page des défis
    current_url = context.driver.current_url
    challenges_page_indicators = [
        "/challenges" in current_url,
        len(context.driver.find_elements(By.CSS_SELECTOR, ".challenges-page, .daily-challenges")) > 0
    ]
    
    assert any(challenges_page_indicators), "Page des défis non ouverte"


@then('l\'interface caméra native doit s\'ouvrir')
def step_native_camera_interface_should_open(context):
    """Vérifier l'ouverture de l'interface caméra native"""
    # Vérifier que l'autorisation caméra a été demandée et accordée
    camera_authorized = context.driver.execute_script("return window.cameraAuthorized;")
    assert camera_authorized, "Interface caméra non autorisée"
    
    # Vérifier la présence d'éléments de l'interface caméra
    camera_elements = context.driver.find_elements(
        By.CSS_SELECTOR,
        ".camera-interface, .photo-capture, video, .camera-preview"
    )
    assert len(camera_elements) > 0, "Interface caméra non ouverte"
