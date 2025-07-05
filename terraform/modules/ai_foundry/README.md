# Azure AI Foundry Module
# Module moderne pour intégration IA complète - Lake Holidays Challenge

Ce module déploie une infrastructure Azure AI Foundry complète pour votre application Lake Holidays Challenge, remplaçant l'ancien module Azure OpenAI classique avec des fonctionnalités étendues.

## Fonctionnalités

### 🤖 Azure AI Hub
- **Centre de gestion IA unifié** pour tous vos modèles
- **Support multi-modèles** : OpenAI, Azure AI, modèles personnalisés
- **Gouvernance IA** : politiques, quotas, monitoring
- **Sécurité renforcée** : identités managées, RBAC

### 🧠 Azure OpenAI Intégré
- **Modèles OpenAI** : GPT-4o-mini optimisé pour votre cas d'usage
- **Déploiements flexibles** : scaling automatique selon la charge
- **Monitoring avancé** : métriques détaillées, alertes

### 🔐 Sécurité
- **Identités managées** : accès sans clés API
- **Key Vault intégré** : stockage sécurisé des configurations
- **RBAC Azure** : permissions granulaires

## Utilisation

```hcl
module "ai_foundry" {
  source = "./modules/ai_foundry"
  
  resource_group_name = "lake-holidays-prod-rg"
  location           = "East US"
  app_name          = "lake-holidays"
  environment       = "prod"
  
  model_deployments = [
    {
      name          = "gpt-4o-mini"
      model_name    = "gpt-4o-mini"
      model_version = "2024-07-18"
      scale_type    = "Standard"
      capacity      = 30
    }
  ]
  
  key_vault_id = module.key_vault.id
  managed_identity_principal_id = module.aks.kubelet_identity[0].object_id
  
  tags = local.common_tags
}
```

## Variables

| Nom | Description | Type | Défaut | Requis |
|-----|-------------|------|--------|---------|
| `resource_group_name` | Nom du resource group | string | - | ✅ |
| `location` | Région Azure | string | - | ✅ |
| `app_name` | Nom de l'application | string | - | ✅ |
| `environment` | Environnement (dev/staging/prod) | string | - | ✅ |
| `model_deployments` | Configuration des modèles | list(object) | gpt-4o-mini | ❌ |
| `sku_name` | SKU Azure AI | string | "S0" | ❌ |
| `key_vault_id` | ID du Key Vault | string | - | ✅ |
| `managed_identity_principal_id` | ID identité managée AKS | string | - | ✅ |

## Outputs

| Nom | Description | Sensible |
|-----|-------------|----------|
| `ai_hub_endpoint` | Endpoint Azure AI Hub | ✅ |
| `openai_endpoint` | Endpoint Azure OpenAI | ✅ |
| `deployed_models` | Configuration des modèles | ✅ |
| `ai_hub_id` | ID du AI Hub | ❌ |

## Régions supportées

- **East US** ⭐ (Recommandé - plus de modèles)
- **East US 2**
- **West US**
- **West US 2**
- **Sweden Central** (Proche Europe)
- **UK South** (Proche Europe)

## Avantages vs Azure OpenAI classique

| Fonctionnalité | Azure OpenAI | AI Foundry |
|----------------|--------------|------------|
| **Modèles supportés** | OpenAI uniquement | OpenAI + Azure AI + Custom |
| **Gestion centralisée** | ❌ | ✅ |
| **Prompt engineering** | Basique | Outils avancés |
| **Monitoring** | Basique | Complet |
| **Gouvernance** | Limitée | Complète |
| **Évolutivité** | Limitée | Excellente |

## Intégration application

Les configurations sont automatiquement stockées dans Key Vault :

```json
{
  "ai_hub": {
    "endpoint": "https://lake-holidays-prod-ai-hub.openai.azure.com/",
    "resource_id": "/subscriptions/.../lake-holidays-prod-ai-hub"
  },
  "openai": {
    "endpoint": "https://lake-holidays-prod-openai.openai.azure.com/",
    "models": {
      "gpt-4o-mini": {
        "deployment_name": "gpt-4o-mini",
        "model_name": "gpt-4o-mini",
        "model_version": "2024-07-18"
      }
    }
  }
}
```

## Cas d'usage Lake Holidays

- **Génération de défis quotidiens** : GPT-4o-mini optimisé
- **Analyse de contenu utilisateur** : AI Hub multi-modal
- **Personnalisation** : Modèles adaptés au contexte
- **Modération** : Services Azure AI intégrés
- **Analytics** : Insights sur l'engagement utilisateur

## Migration depuis OpenAI classique

Ce module remplace automatiquement l'ancien module `openai` avec :
- ✅ **Compatibilité** : mêmes endpoints et clés
- ✅ **Fonctionnalités étendues** : nouvelles capacités IA
- ✅ **Migration transparente** : aucun changement côté application
- ✅ **Performance améliorée** : optimisations Azure AI

---

**Généré par Terraform** - Lake Holidays Challenge 🏖️🎮
