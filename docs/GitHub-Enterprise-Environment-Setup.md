# Configuration des Environnements GitHub Enterprise

Ce document explique comment configurer et utiliser les environnements GitHub Enterprise pour le déploiement automatisé de Lake Holidays Challenge.

## 🏗️ Architecture des Environnements

### Environnement `prod`
- **Déclencheur** : Push sur la branche `main`
- **Namespace Kubernetes** : `lake-holidays-prod`
- **Domaines** :
  - Frontend : `frontend-prod.francecentral.cloudapp.azure.com`
  - Backend API : `api-prod.francecentral.cloudapp.azure.com`

### Environnement `staging`
- **Déclencheur** : Push sur la branche `develop`
- **Namespace Kubernetes** : `lake-holidays-staging`
- **Domaines** :
  - Frontend : `frontend-staging.francecentral.cloudapp.azure.com`
  - Backend API : `api-staging.francecentral.cloudapp.azure.com`

## 🔧 Configuration GitHub Enterprise

### Variables d'Environnement

Dans GitHub Enterprise, les variables suivantes sont configurées pour l'environnement `prod` :

| Variable | Valeur | Description |
|----------|---------|-------------|
| `AKS_CLUSTER_NAME` | `lake-holidays-prod-aks` | Nom du cluster AKS |
| `AZURE_CONTAINER_REGISTRY` | `lakeprodacr2h7yde` | Registry Azure Container |
| `AZURE_RESOURCE_GROUP` | `lake-holidays-prod-rg` | Groupe de ressources Azure |
| `DOMAIN_SUFFIX` | `francecentral.cloudapp.azure.com` | Suffixe de domaine |
| `KEY_VAULT_NAME` | `lake-prod-kv-1xnf` | Nom du Key Vault Azure |
| `STORAGE_ACCOUNT_NAME` | `lakeholidaysprodstorage` | Compte de stockage Azure |

### Secrets d'Environnement

| Secret | Description |
|--------|-------------|
| `AZURE_CREDENTIALS` | Credentials pour l'authentification Azure (inherited from repository) |

## 🚀 Workflow de Déploiement

### Déclenchement Automatique

Le workflow se déclenche automatiquement :
- Sur `main` → déploiement en environnement `prod`
- Sur `develop` → déploiement en environnement `staging`

### Étapes du Déploiement

1. **Tests Backend** - Exécution des tests Python avec PostgreSQL
2. **Tests Frontend** - Tests unitaires et lint avec Node.js
3. **Build & Push** - Construction et publication des images Docker
4. **Deploy to AKS** - Déploiement sur Azure Kubernetes Service
5. **Post-deployment Tests** - Vérifications de santé après déploiement

## 🔒 Règles de Protection

### Environnement `prod`

Les règles de protection configurées incluent :
- ✅ **Allow administrators to bypass configured protection rules**
- 🚀 **No deployment restrictions** (déploiement sur toutes les branches/tags)

### Secrets et Variables

- **Secrets** : Chiffrés et accessibles uniquement pendant l'exécution dans le contexte de l'environnement
- **Variables** : Configuration non-sensible accessible via `vars.VARIABLE_NAME`

## 🔍 Monitoring et Logs

### Accès aux Logs
- Les logs de déploiement sont disponibles dans l'onglet Actions
- Les rapports de déploiement sont générés automatiquement dans le summary GitHub

### Health Checks
- Vérification automatique de l'état des pods Kubernetes
- Timeout de 5 minutes pour les vérifications de santé
- Tests de fumée post-déploiement

## 🛠️ Utilisation des Variables dans le Code

### Dans le Workflow

```yaml
environment:
  name: ${{ github.ref_name == 'main' && 'prod' || 'staging' }}
  
env:
  ENVIRONMENT: ${{ github.ref_name == 'main' && 'prod' || 'staging' }}
  KEY_VAULT_NAME: lake-prod-kv-1xnf
  STORAGE_ACCOUNT_NAME: lakeholidaysprodstorage
  DOMAIN_SUFFIX: francecentral.cloudapp.azure.com
```

### Dans les Manifests Kubernetes

Les variables sont substituées dans les manifests K8s :
```yaml
# Exemple dans k8s/03-frontend-deployment.yaml
- name: REACT_APP_API_URL
  value: "https://api-{{ENVIRONMENT}}.{{DOMAIN_SUFFIX}}"
```

## 🔄 Migration depuis l'Ancienne Configuration

### Changements Apportés

1. **Environnement GitHub** : `production` → `prod`
2. **Variables** : Migration des secrets vers les variables d'environnement
3. **Domaines** : Utilisation cohérente des domaines basés sur l'environnement

### Compatibilité

Le workflow reste compatible avec les déploiements existants et utilise des fallbacks pour les configurations manquantes.

## 📋 Checklist de Vérification

Avant de déployer, vérifiez que :

- [ ] L'environnement `prod` est configuré dans GitHub Enterprise
- [ ] Toutes les variables d'environnement sont définies
- [ ] Les secrets Azure sont configurés
- [ ] Le cluster AKS est accessible
- [ ] Les domaines sont configurés dans Azure

## 🆘 Dépannage

### Erreurs Communes

1. **Variables non trouvées** : Vérifiez que l'environnement GitHub est correctement configuré
2. **Échec d'authentification Azure** : Vérifiez les credentials Azure dans les secrets
3. **Pods non prêts** : Vérifiez les logs Kubernetes et les ressources disponibles

### Support

Pour obtenir de l'aide :
1. Consultez les logs GitHub Actions
2. Vérifiez l'état des ressources Azure
3. Examinez les logs Kubernetes avec `kubectl logs`
