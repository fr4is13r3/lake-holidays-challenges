#!/bin/bash
#
# ===================================================================
# IMPORT USER STORIES TO GITHUB ISSUES
# ===================================================================
#
# Description:
#   This script automates the creation of GitHub issues from a markdown
#   file containing user stories organized by epics. It creates both
#   epic issues and individual user story issues with appropriate
#   labels, priorities, and sprint assignments.
#
# Author: Lake Holidays Challenge Team
# Version: 1.0
# Last Modified: $(date +%Y-%m-%d)
#
# Prerequisites:
#   - GitHub CLI (gh) installed and authenticated
#   - Access to the target GitHub repository
#   - UserStories.md file in the parent directory
#
# Usage:
#   ./import-user-stories.sh [OPTIONS]
#
# Options:
#   -d, --dry-run    Preview what would be created without making changes
#   -h, --help       Display this help message
#
# Examples:
#   # Normal execution
#   ./import-user-stories.sh
#
#   # Dry run to preview
#   ./import-user-stories.sh --dry-run
#
#   # Using environment variable
#   DRY_RUN=true ./import-user-stories.sh
#
# Configuration:
#   REPO           Target GitHub repository (owner/repo)
#   MARKDOWN_FILE  Path to the user stories markdown file
#   DRY_RUN        Set to true for preview mode
#
# Features:
#   - Creates epic issues for story organization
#   - Creates individual user story issues
#   - Assigns appropriate labels (epic, priority, sprint)
#   - Automatically determines priority based on story ID
#   - Supports dry-run mode for testing
#   - Color-coded console output
#
# Labels Created:
#   Epic labels: epic:authentication, epic:profiles, etc.
#   Priority: priority:critical, priority:high, priority:medium, priority:low
#   Sprint: sprint:1, sprint:2, sprint:3, sprint:4
#   Type: epic, story
#
# Expected Markdown Format:
#   ## Epic X: Title
#   ### US001 - Story Title
#   Story description...
#
# Exit Codes:
#   0 - Success
#   1 - Error (missing dependencies, file not found, etc.)
#
# ===================================================================

# Configuration
REPO="fr4is13r3/lake-holidays-challenges"
MARKDOWN_FILE="../UserStories.md"
DRY_RUN=${DRY_RUN:-false}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages
log() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check if GitHub CLI is installed and authenticated
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        error "GitHub CLI (gh) is not installed. Please install it first:"
        echo "https://cli.github.com/"
        exit 1
    fi
    
    if ! gh auth status &> /dev/null; then
        error "GitHub CLI is not authenticated. Please run: gh auth login"
        exit 1
    fi
    
    success "GitHub CLI is ready"
}

# Create labels if they don't exist
create_labels() {
    log "Creating project labels..."
    
    labels=(
        "epic:authentication|Epic: Authentication|#FF6B6B"
        "epic:profiles|Epic: User Profiles|#4ECDC4"
        "epic:seasons|Epic: Season Management|#45B7D1"
        "epic:challenges|Epic: Daily Challenges|#96CEB4"
        "epic:scoring|Epic: Scoring System|#FFEAA7"
        "epic:mobile|Epic: Mobile Interface|#DDA0DD"
        "epic:ai|Epic: AI Content|#98D8C8"
        "priority:critical|Priority: Critical|#E74C3C"
        "priority:high|Priority: High|#F39C12"
        "priority:medium|Priority: Medium|#F1C40F"
        "priority:low|Priority: Low|#95A5A6"
        "story|User Story|#3498DB"
        "epic|Epic|#9B59B6"
        "sprint:1|Sprint 1|#1ABC9C"
        "sprint:2|Sprint 2|#2ECC71"
        "sprint:3|Sprint 3|#F39C12"
        "sprint:4|Sprint 4|#E67E22"
    )
    
    for label_info in "${labels[@]}"; do
        IFS='|' read -r name description color <<< "$label_info"
        
        if $DRY_RUN; then
            log "Would create label: $name"
        else
            gh label create "$name" --description "$description" --color "$color" --repo "$REPO" 2>/dev/null || true
        fi
    done
}

# Parse markdown file and extract user stories
parse_user_stories() {
    local file="$1"
    local current_epic=""
    local current_epic_label=""
    local in_user_story=false
    local story_title=""
    local story_body=""
    local story_id=""
    local story_labels=()
    
    log "Parsing $file..."
    
    while IFS= read -r line; do
        # Detect Epic
        if [[ $line =~ ^##[[:space:]]*Epic[[:space:]]*[0-9]+:[[:space:]]*(.*) ]]; then
            current_epic="${BASH_REMATCH[1]}"
            case $current_epic in
                "Authentification"*) current_epic_label="epic:authentication" ;;
                "Profils"*) current_epic_label="epic:profiles" ;;
                *"Saisons"*) current_epic_label="epic:seasons" ;;
                *"Défis"*) current_epic_label="epic:challenges" ;;
                *"Scoring"*) current_epic_label="epic:scoring" ;;
                *"Mobile"*) current_epic_label="epic:mobile" ;;
                *"IA"*|*"AI"*) current_epic_label="epic:ai" ;;
                *) current_epic_label="epic" ;;
            esac
            log "Found epic: $current_epic"
            
            # Create epic issue
            create_epic_issue "$current_epic" "$current_epic_label"
            
        # Detect User Story
        elif [[ $line =~ ^###[[:space:]]*(US[0-9]+)[[:space:]]*-[[:space:]]*(.*) ]]; then
            # Save previous story if exists
            if [[ $in_user_story == true && -n $story_title ]]; then
                create_user_story "$story_id" "$story_title" "$story_body" "${story_labels[@]}"
            fi
            
            # Start new story
            story_id="${BASH_REMATCH[1]}"
            story_title="${BASH_REMATCH[2]}"
            story_body="## Epic: $current_epic\n\n"
            story_labels=("story" "$current_epic_label")
            in_user_story=true
            
            # Determine priority based on sprint
            if [[ $story_id =~ US00[1-8]|US018 ]]; then
                story_labels+=("priority:critical" "sprint:1")
            elif [[ $story_id =~ US00[9]|US01[0-1]|US014|US015|US021 ]]; then
                story_labels+=("priority:high" "sprint:2")
            elif [[ $story_id =~ US012|US013|US016|US017|US019|US020 ]]; then
                story_labels+=("priority:medium" "sprint:3")
            else
                story_labels+=("priority:low" "sprint:4")
            fi
            
        # Skip section separators
        elif [[ $line =~ ^---*$ ]]; then
            continue
            
        # Add content to current story
        elif [[ $in_user_story == true ]]; then
            if [[ -n $line ]]; then
                story_body+="\n$line"
            fi
        fi
        
    done < "$file"
    
    # Save last story
    if [[ $in_user_story == true && -n $story_title ]]; then
        create_user_story "$story_id" "$story_title" "$story_body" "${story_labels[@]}"
    fi
}

# Create epic issue
create_epic_issue() {
    local title="$1"
    local label="$2"
    
    local body="# Epic: $title

This epic groups related user stories for the **$title** functionality.

## Objectives
- Implement core functionality for $title
- Ensure BDD test coverage
- Maintain mobile-first approach

## User Stories
This epic will be populated with related user stories.

---
*Generated automatically from UserStories.md*"
    
    if $DRY_RUN; then
        log "Would create epic: $title"
    else
        local issue_url
        issue_url=$(gh issue create \
            --title "Epic: $title" \
            --body "$body" \
            --label "epic,$label,priority:high" \
            --repo "$REPO")
        success "Created epic: $title ($issue_url)"
    fi
}

# Create user story issue
create_user_story() {
    local story_id="$1"
    local title="$2"
    local body="$3"
    shift 3
    local labels=("$@")
    
    # Join labels with comma
    local label_string
    label_string=$(IFS=','; echo "${labels[*]}")
    
    local full_title="$story_id - $title"
    
    if $DRY_RUN; then
        log "Would create story: $full_title"
        log "  Labels: $label_string"
    else
        local issue_url
        issue_url=$(gh issue create \
            --title "$full_title" \
            --body "$body" \
            --label "$label_string" \
            --repo "$REPO")
        success "Created story: $full_title ($issue_url)"
    fi
}

# Main execution
main() {
    log "Starting GitHub Issues import from $MARKDOWN_FILE"
    
    if [[ ! -f "$MARKDOWN_FILE" ]]; then
        error "Markdown file $MARKDOWN_FILE not found!"
        exit 1
    fi
    
    if $DRY_RUN; then
        warn "DRY RUN MODE - No actual issues will be created"
    fi
    
    check_gh_cli
    create_labels
    parse_user_stories "$MARKDOWN_FILE"
    
    success "Import completed!"
    
    if ! $DRY_RUN; then
        log "View your issues: https://github.com/$REPO/issues"
        log "Set up project board: https://github.com/$REPO/projects"
    fi
}

# Handle command line arguments
case "${1:-}" in
    "--dry-run"|"-d")
        DRY_RUN=true
        main
        ;;
    "--help"|"-h")
        echo "Usage: $0 [--dry-run|--help]"
        echo "  --dry-run, -d    Run without creating issues"
        echo "  --help, -h       Show this help"
        ;;
    "")
        main
        ;;
    *)
        error "Unknown option: $1"
        echo "Use --help for usage information"
        exit 1
        ;;
esac