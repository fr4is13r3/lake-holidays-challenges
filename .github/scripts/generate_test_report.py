#!/usr/bin/env python3
"""
Script de génération de rapport consolidé pour les tests BDD
Agrège les résultats de tous les tests et génère un rapport HTML et JSON
"""

import json
import os
import sys
import glob
from datetime import datetime
from pathlib import Path
import argparse

def load_test_results(artifacts_dir):
    """Charge tous les résultats de tests depuis les artifacts"""
    results = {
        'smoke': None,
        'features': {},
        'e2e': None,
        'performance': None
    }
    
    artifacts_path = Path(artifacts_dir)
    
    # Rechercher tous les fichiers JSON de résultats
    for json_file in artifacts_path.rglob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            filename = json_file.name
            
            if 'smoke-results' in filename:
                results['smoke'] = data
            elif 'e2e-results' in filename:
                results['e2e'] = data
            elif 'performance-results' in filename:
                results['performance'] = data
            elif '-results.json' in filename:
                # Feature tests (authentication-results.json, etc.)
                feature_name = filename.replace('-results.json', '')
                results['features'][feature_name] = data
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"⚠️  Erreur lors du chargement de {json_file}: {e}")
    
    return results

def calculate_stats(test_data):
    """Calcule les statistiques d'un ensemble de tests"""
    if not test_data:
        return {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0}
    
    stats = {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0}
    
    # Traitement selon le format de behave
    if isinstance(test_data, list):
        for feature in test_data:
            if 'elements' in feature:
                for scenario in feature['elements']:
                    if scenario.get('type') == 'scenario':
                        stats['total'] += 1
                        status = scenario.get('status', 'unknown')
                        if status == 'passed':
                            stats['passed'] += 1
                        elif status == 'failed':
                            stats['failed'] += 1
                        elif status == 'skipped':
                            stats['skipped'] += 1
    
    return stats

def generate_html_report(results, output_dir):
    """Génère un rapport HTML consolidé"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calcul des statistiques globales
    all_stats = {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0}
    
    smoke_stats = calculate_stats(results['smoke'])
    e2e_stats = calculate_stats(results['e2e'])
    performance_stats = calculate_stats(results['performance'])
    
    feature_stats = {}
    for feature_name, feature_data in results['features'].items():
        feature_stats[feature_name] = calculate_stats(feature_data)
    
    # Agrégation des stats
    for stats in [smoke_stats, e2e_stats, performance_stats] + list(feature_stats.values()):
        for key in all_stats:
            all_stats[key] += stats[key]
    
    # Calcul du taux de réussite
    success_rate = (all_stats['passed'] / all_stats['total'] * 100) if all_stats['total'] > 0 else 0
    
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧪 Rapport Tests BDD - Vacances Gamifiées</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f7fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .skipped {{ color: #ffc107; }}
        .total {{ color: #007bff; }}
        .content {{
            padding: 30px;
        }}
        .test-suite {{
            margin-bottom: 30px;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            overflow: hidden;
        }}
        .test-suite-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e9ecef;
            font-weight: bold;
        }}
        .test-suite-body {{
            padding: 20px;
        }}
        .progress-bar {{
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            margin: 2px;
        }}
        .badge-success {{ background: #d4edda; color: #155724; }}
        .badge-danger {{ background: #f8d7da; color: #721c24; }}
        .badge-warning {{ background: #fff3cd; color: #856404; }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
        }}
        .status-icon {{
            font-size: 1.2em;
            margin-right: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 Rapport Tests BDD</h1>
            <p>Application Vacances Gamifiées</p>
            <p>Généré le {timestamp}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number total">{all_stats['total']}</div>
                <div>Tests Total</div>
            </div>
            <div class="stat-card">
                <div class="stat-number passed">{all_stats['passed']}</div>
                <div>Réussis</div>
            </div>
            <div class="stat-card">
                <div class="stat-number failed">{all_stats['failed']}</div>
                <div>Échoués</div>
            </div>
            <div class="stat-card">
                <div class="stat-number skipped">{all_stats['skipped']}</div>
                <div>Ignorés</div>
            </div>
        </div>
        
        <div class="content">
            <h2>📊 Taux de Réussite Global</h2>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {success_rate}%"></div>
            </div>
            <p><strong>{success_rate:.1f}%</strong> de tests réussis</p>
            
            <h2>🚀 Tests de Smoke</h2>
            <div class="test-suite">
                <div class="test-suite-header">
                    <span class="status-icon">{'✅' if smoke_stats['failed'] == 0 else '❌'}</span>
                    Tests de Smoke
                </div>
                <div class="test-suite-body">
                    <span class="badge badge-success">{smoke_stats['passed']} réussis</span>
                    <span class="badge badge-danger">{smoke_stats['failed']} échoués</span>
                    <span class="badge badge-warning">{smoke_stats['skipped']} ignorés</span>
                </div>
            </div>
            
            <h2>🎯 Tests par Feature</h2>
"""
    
    # Ajout des tests par feature
    for feature_name, stats in feature_stats.items():
        status_icon = '✅' if stats['failed'] == 0 else '❌'
        html_content += f"""
            <div class="test-suite">
                <div class="test-suite-header">
                    <span class="status-icon">{status_icon}</span>
                    Feature: {feature_name.title()}
                </div>
                <div class="test-suite-body">
                    <span class="badge badge-success">{stats['passed']} réussis</span>
                    <span class="badge badge-danger">{stats['failed']} échoués</span>
                    <span class="badge badge-warning">{stats['skipped']} ignorés</span>
                </div>
            </div>
"""
    
    # Tests E2E
    e2e_status_icon = '✅' if e2e_stats['failed'] == 0 else '❌'
    html_content += f"""
            <h2>🔄 Tests End-to-End</h2>
            <div class="test-suite">
                <div class="test-suite-header">
                    <span class="status-icon">{e2e_status_icon}</span>
                    Tests E2E Complets
                </div>
                <div class="test-suite-body">
                    <span class="badge badge-success">{e2e_stats['passed']} réussis</span>
                    <span class="badge badge-danger">{e2e_stats['failed']} échoués</span>
                    <span class="badge badge-warning">{e2e_stats['skipped']} ignorés</span>
                </div>
            </div>
"""
    
    # Tests de performance (si disponibles)
    if results['performance']:
        perf_status_icon = '✅' if performance_stats['failed'] == 0 else '❌'
        html_content += f"""
            <h2>⚡ Tests de Performance</h2>
            <div class="test-suite">
                <div class="test-suite-header">
                    <span class="status-icon">{perf_status_icon}</span>
                    Tests de Performance
                </div>
                <div class="test-suite-body">
                    <span class="badge badge-success">{performance_stats['passed']} réussis</span>
                    <span class="badge badge-danger">{performance_stats['failed']} échoués</span>
                    <span class="badge badge-warning">{performance_stats['skipped']} ignorés</span>
                </div>
            </div>
"""
    
    html_content += f"""
        </div>
        
        <div class="footer">
            <p>🏖️ Vacances Gamifiées - Tests BDD automatisés</p>
            <p>Rapport généré automatiquement par GitHub Actions</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Écriture du fichier HTML
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    html_file = output_path / "consolidated-test-report.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_file

def generate_json_summary(results, output_dir):
    """Génère un résumé JSON des résultats"""
    timestamp = datetime.now().isoformat()
    
    # Calcul des statistiques pour chaque suite
    summary = {
        'timestamp': timestamp,
        'overall': {'total': 0, 'passed': 0, 'failed': 0, 'skipped': 0},
        'suites': {
            'smoke': calculate_stats(results['smoke']),
            'features': {},
            'e2e': calculate_stats(results['e2e']),
            'performance': calculate_stats(results['performance'])
        }
    }
    
    # Features individuelles
    for feature_name, feature_data in results['features'].items():
        summary['suites']['features'][feature_name] = calculate_stats(feature_data)
    
    # Calcul des totaux
    for suite_stats in [summary['suites']['smoke'], summary['suites']['e2e'], summary['suites']['performance']]:
        for key in summary['overall']:
            summary['overall'][key] += suite_stats[key]
    
    for feature_stats in summary['suites']['features'].values():
        for key in summary['overall']:
            summary['overall'][key] += feature_stats[key]
    
    # Calcul du taux de réussite
    if summary['overall']['total'] > 0:
        summary['overall']['success_rate'] = summary['overall']['passed'] / summary['overall']['total'] * 100
    else:
        summary['overall']['success_rate'] = 0
    
    # Écriture du fichier JSON
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    json_file = output_path / "test-summary.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    return json_file

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Génère un rapport consolidé des tests BDD')
    parser.add_argument('artifacts_dir', help='Répertoire contenant les artifacts de tests')
    parser.add_argument('output_dir', help='Répertoire de sortie pour les rapports')
    parser.add_argument('--verbose', '-v', action='store_true', help='Mode verbeux')
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"🔍 Recherche des résultats de tests dans: {args.artifacts_dir}")
        print(f"📁 Génération des rapports dans: {args.output_dir}")
    
    # Chargement des résultats
    try:
        results = load_test_results(args.artifacts_dir)
        
        if args.verbose:
            print(f"✅ Résultats chargés:")
            print(f"   - Smoke tests: {'✓' if results['smoke'] else '✗'}")
            print(f"   - Features: {len(results['features'])} trouvées")
            print(f"   - E2E tests: {'✓' if results['e2e'] else '✗'}")
            print(f"   - Performance: {'✓' if results['performance'] else '✗'}")
        
        # Génération des rapports
        html_file = generate_html_report(results, args.output_dir)
        json_file = generate_json_summary(results, args.output_dir)
        
        print(f"📊 Rapport HTML généré: {html_file}")
        print(f"📋 Résumé JSON généré: {json_file}")
        
        # Affichage du résumé
        with open(json_file, 'r') as f:
            summary = json.load(f)
        
        overall = summary['overall']
        print(f"\n🧪 Résumé des tests:")
        print(f"   📈 Total: {overall['total']}")
        print(f"   ✅ Réussis: {overall['passed']}")
        print(f"   ❌ Échoués: {overall['failed']}")
        print(f"   ⏭️  Ignorés: {overall['skipped']}")
        print(f"   📊 Taux de réussite: {overall['success_rate']:.1f}%")
        
        # Code de sortie basé sur les échecs
        if overall['failed'] > 0:
            print(f"\n⚠️  {overall['failed']} test(s) ont échoué!")
            sys.exit(1)
        else:
            print(f"\n🎉 Tous les tests sont passés!")
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Erreur lors de la génération du rapport: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
