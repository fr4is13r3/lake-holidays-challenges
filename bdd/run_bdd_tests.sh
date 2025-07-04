#!/bin/bash

# Script d'exécution des tests BDD pour l'application Vacances Gamifiées
# Usage: ./run_bdd_tests.sh [options]

set -e  # Arrêt en cas d'erreur

# Configuration par défaut
DEFAULT_ENV="dev"
DEFAULT_TAGS=""
DEFAULT_FORMAT="pretty"
HEADLESS="true"
PARALLEL="false"
INSTALL_DEPS="false"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'aide
show_help() {
    echo -e "${BLUE}Script d'exécution des tests BDD - Vacances Gamifiées${NC}"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -e, --env ENV          Environnement de test (dev|staging|prod). Default: dev"
    echo "  -t, --tags TAGS        Tags à exécuter (ex: @smoke, @authentication)"
    echo "  -f, --format FORMAT    Format de sortie (pretty|json|html). Default: pretty"
    echo "  -h, --headless         Mode headless pour navigateur (true|false). Default: true"
    echo "  -p, --parallel         Exécution parallèle des tests"
    echo "  -i, --install          Installer les dépendances avant exécution"
    echo "  --help                 Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 --tags @smoke                    # Tests de smoke uniquement"
    echo "  $0 --env staging --headless false   # Tests staging avec interface"
    echo "  $0 --parallel --tags @authentication # Tests auth en parallèle"
    echo "  $0 --install --format html          # Installation + rapport HTML"
}

# Fonction de log
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            TEST_ENV="$2"
            shift 2
            ;;
        -t|--tags)
            TAGS="$2"
            shift 2
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -h|--headless)
            HEADLESS="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL="true"
            shift
            ;;
        -i|--install)
            INSTALL_DEPS="true"
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            error "Option inconnue: $1"
            show_help
            exit 1
            ;;
    esac
done

# Valeurs par défaut
TEST_ENV=${TEST_ENV:-$DEFAULT_ENV}
TAGS=${TAGS:-$DEFAULT_TAGS}
FORMAT=${FORMAT:-$DEFAULT_FORMAT}

# Vérification de l'environnement
if [[ ! "$TEST_ENV" =~ ^(dev|staging|prod)$ ]]; then
    error "Environnement invalide: $TEST_ENV. Utilisez: dev, staging, ou prod"
    exit 1
fi

# Vérification du répertoire
if [[ ! -d "bdd" ]]; then
    error "Répertoire 'bdd' non trouvé. Exécutez ce script depuis la racine du projet."
    exit 1
fi

cd bdd

log "🧪 Démarrage des tests BDD - Environnement: $TEST_ENV"

# Installation des dépendances si demandé
if [[ "$INSTALL_DEPS" == "true" ]]; then
    log "📦 Installation des dépendances..."
    
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements.txt
    else
        error "pip non trouvé. Installez Python et pip."
        exit 1
    fi
    
    log "✅ Dépendances installées"
fi

# Vérification que behave est installé
if ! command -v behave &> /dev/null; then
    error "Behave non installé. Utilisez: pip install -r requirements.txt"
    exit 1
fi

# Configuration des variables d'environnement
export TEST_ENV=$TEST_ENV
export HEADLESS=$HEADLESS

case $TEST_ENV in
    "dev")
        export BASE_URL="http://localhost:3000"
        ;;
    "staging")
        export BASE_URL="https://staging-vacances.azurewebsites.net"
        ;;
    "prod")
        export BASE_URL="https://vacances.azurewebsites.net"
        ;;
esac

log "🌐 URL de base: $BASE_URL"

# Préparation des répertoires de rapport
mkdir -p ../reports/screenshots
mkdir -p ../reports/html

# Construction de la commande behave
BEHAVE_CMD="behave"

# Tags
if [[ -n "$TAGS" ]]; then
    BEHAVE_CMD="$BEHAVE_CMD --tags=$TAGS"
    log "🏷️  Tags: $TAGS"
fi

# Format de sortie
case $FORMAT in
    "html")
        BEHAVE_CMD="$BEHAVE_CMD -f html -o ../reports/behave_report.html"
        log "📄 Rapport HTML: ../reports/behave_report.html"
        ;;
    "json")
        BEHAVE_CMD="$BEHAVE_CMD -f json -o ../reports/behave_report.json"
        log "📄 Rapport JSON: ../reports/behave_report.json"
        ;;
    "pretty")
        BEHAVE_CMD="$BEHAVE_CMD -f pretty"
        ;;
    *)
        warn "Format non reconnu: $FORMAT. Utilisation de 'pretty'"
        BEHAVE_CMD="$BEHAVE_CMD -f pretty"
        ;;
esac

# Exécution parallèle
if [[ "$PARALLEL" == "true" ]]; then
    if command -v behave-parallel &> /dev/null; then
        log "🚀 Exécution en parallèle..."
        BEHAVE_CMD=$(echo $BEHAVE_CMD | sed 's/behave/behave-parallel --processes 4/')
    else
        warn "behave-parallel non installé. Exécution séquentielle."
    fi
fi

# Affichage de la commande
log "🔧 Commande: $BEHAVE_CMD"

# Configuration du mode headless
if [[ "$HEADLESS" == "true" ]]; then
    log "🖥️  Mode headless activé"
else
    log "🖥️  Mode avec interface graphique"
fi

# Vérification de la connectivité (pour dev uniquement)
if [[ "$TEST_ENV" == "dev" ]]; then
    log "🔍 Vérification de la connectivité locale..."
    if ! curl -s "$BASE_URL" > /dev/null; then
        warn "L'application locale ne semble pas accessible sur $BASE_URL"
        warn "Assurez-vous que l'application est démarrée localement."
    fi
fi

# Exécution des tests
log "🎯 Exécution des tests..."
echo ""

if eval $BEHAVE_CMD; then
    log "✅ Tests terminés avec succès!"
    
    # Affichage des rapports générés
    if [[ "$FORMAT" == "html" ]] && [[ -f "../reports/behave_report.html" ]]; then
        log "📊 Rapport HTML généré: $(pwd)/../reports/behave_report.html"
        
        # Ouverture automatique du rapport si possible
        if command -v xdg-open &> /dev/null; then
            xdg-open "../reports/behave_report.html" 2>/dev/null &
        elif command -v open &> /dev/null; then
            open "../reports/behave_report.html" 2>/dev/null &
        fi
    fi
    
    # Affichage des captures d'écran s'il y en a
    SCREENSHOTS_COUNT=$(find ../reports/screenshots -name "*.png" 2>/dev/null | wc -l)
    if [[ $SCREENSHOTS_COUNT -gt 0 ]]; then
        warn "📸 $SCREENSHOTS_COUNT capture(s) d'écran générée(s) (échecs): ../reports/screenshots/"
    fi
    
    exit 0
else
    error "❌ Échec des tests"
    
    # Conseils de debugging
    echo ""
    echo -e "${BLUE}💡 Conseils de debugging:${NC}"
    echo "   • Vérifiez les logs ci-dessus pour les erreurs détaillées"
    echo "   • Consultez les captures d'écran dans ../reports/screenshots/"
    echo "   • Exécutez avec --headless false pour voir l'interface"
    echo "   • Utilisez --tags @smoke pour tester uniquement les cas critiques"
    echo "   • Vérifiez que l'application est démarrée et accessible"
    
    exit 1
fi
