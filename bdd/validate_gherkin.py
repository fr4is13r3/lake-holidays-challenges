#!/usr/bin/env python3
"""
Validation basique de la syntaxe Gherkin pour tous les fichiers .feature
"""

import re
import glob
from pathlib import Path

def validate_gherkin_syntax(feature_file):
    """Valide la syntaxe Gherkin basique d'un fichier"""
    errors = []
    
    with open(feature_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_step_context = False
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        
        # Ignorer les lignes vides et commentaires
        if not line or line.startswith('#'):
            continue
            
        # Lignes de structure Gherkin valides
        if re.match(r'^(Feature|Scenario|Background|Examples|Scenario Outline):', line):
            in_step_context = False
            continue
            
        # Tags valides
        if line.startswith('@'):
            continue
            
        # Descriptions de feature (indentées)
        if re.match(r'^(En tant qu|Je veux|Afin d)', line.strip()):
            continue
            
        # Steps Gherkin valides
        if re.match(r'^(Given|When|Then|And|But|Soit|Quand|Alors|Et|Mais|Étant donné)\s', line):
            in_step_context = True
            continue
            
        # Colonnes de tables de données (commencent par |)
        if line.startswith('|'):
            continue
            
        # Texte multiligne (""")
        if line.startswith('"""'):
            continue
            
        # Si on est dans un contexte de step et qu'on trouve une ligne qui ne commence pas par un mot-clé
        if in_step_context and re.match(r'^[A-Za-z]', line):
            errors.append(f"Ligne {line_num}: Possible étape manquant un mot-clé: '{line}'")
    
    return errors

def main():
    """Valide tous les fichiers .feature"""
    feature_files = glob.glob('/home/erwan/repos/lake-holidays-challenge/bdd/features/*.feature')
    
    total_errors = 0
    
    for feature_file in feature_files:
        errors = validate_gherkin_syntax(feature_file)
        if errors:
            print(f"\n❌ Erreurs dans {Path(feature_file).name}:")
            for error in errors:
                print(f"   {error}")
            total_errors += len(errors)
        else:
            print(f"✅ {Path(feature_file).name} - Syntaxe OK")
    
    if total_errors == 0:
        print(f"\n🎉 Tous les fichiers .feature sont valides!")
    else:
        print(f"\n⚠️ {total_errors} erreur(s) trouvée(s) au total")
    
    return total_errors

if __name__ == "__main__":
    exit(main())
