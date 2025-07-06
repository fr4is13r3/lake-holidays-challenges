# Configurations d'Environnement Terraform

Ce dossier contient les fichiers de configuration spécifiques à chaque environnement pour le déploiement de Lake Holidays Challenge sur Azure Kubernetes Service (AKS).

## 📁 Structure

```
environments/
├── dev/
│   └── terraform.tfvars      # Configuration développement
├── staging/
│   └── terraform.tfvars      # Configuration pré-production
├── prod/
│   └── terraform.tfvars      # Configuration production
└── README.md                 # Ce fichier
```

## 🚀 Utilisation

### Déploiement par Environnement

```bash
# Depuis le dossier terraform/
cd terraform

# Développement
terraform plan -var-file="environments/dev/terraform.tfvars"
terraform apply -var-file="environments/dev/terraform.tfvars"

# Staging
terraform plan -var-file="environments/staging/terraform.tfvars"
terraform apply -var-file="environments/staging/terraform.tfvars"

# Production
terraform plan -var-file="environments/prod/terraform.tfvars"
terraform apply -var-file="environments/prod/terraform.tfvars"
```

### Avec Backend Séparé par Environnement

```bash
# Configuration du backend pour chaque environnement
# Dev
terraform init -backend-config="key=lake-holidays-dev.terraform.tfstate"

# Staging
terraform init -backend-config="key=lake-holidays-staging.terraform.tfstate"

# Production
terraform init -backend-config="key=lake-holidays-prod.terraform.tfstate"
```

## ⚙️ Configuration des Secrets

### Variables Sensibles

Les secrets ne doivent **JAMAIS** être stockés dans les fichiers `.tfvars` versionnés. Utilisez une des méthodes suivantes :

#### 1. Variables d'Environnement (Recommandé pour CI/CD)
```bash
export TF_VAR_jwt_secret_key="votre-jwt-secret-super-securise"
export GOOGLE_CLIENT_SECRET="votre-google-oauth-secret"
export MICROSOFT_CLIENT_SECRET="votre-microsoft-oauth-secret"
export TF_VAR_openai_api_key="votre-openai-api-key"
```

#### 2. Fichier Local Non-Versionné
```bash
# Créer un fichier secrets.tfvars (ajouté au .gitignore)
cat > environments/dev/secrets.tfvars << EOF
jwt_secret_key         = "votre-jwt-secret-dev"
google_client_secret   = "votre-google-oauth-secret-dev"
microsoft_client_secret = "votre-microsoft-oauth-secret-dev"
openai_api_key        = "votre-openai-api-key-dev"
EOF

# Utiliser avec -var-file
terraform apply \
  -var-file="environments/dev/terraform.tfvars" \
  -var-file="environments/dev/secrets.tfvars"
```

#### 3. GitHub Secrets (pour GitHub Actions)
Configurez ces secrets dans votre repository GitHub :
- `AZURE_CREDENTIALS`
- `TF_VAR_JWT_SECRET_KEY`
- `GOOGLE_CLIENT_SECRET`
- `MICROSOFT_CLIENT_SECRET`
- `TF_VAR_OPENAI_API_KEY`

## 🔧 Différences par Environnement

### Développement (dev)
- **AKS** : 2 nœuds Standard_D2s_v3, auto-scaling 1-3
- **Storage** : LRS (Local Redundant)
- **OpenAI** : Désactivé par défaut
- **Monitoring** : Basique
- **Coût** : ~50-100€/mois

### Staging (staging)
- **AKS** : 2 nœuds Standard_D2s_v3, auto-scaling 2-5
- **Storage** : ZRS (Zone Redundant)
- **OpenAI** : Activé avec capacité réduite
- **Monitoring** : Complet pour tests
- **Coût** : ~100-200€/mois

### Production (prod)
- **AKS** : 3 nœuds Standard_D4s_v3, auto-scaling 2-10
- **Storage** : GRS (Geo Redundant)
- **OpenAI** : Activé avec capacité complète
- **Monitoring** : Complet avec alertes
- **Coût** : ~300-800€/mois (selon usage)

## 🛡️ Sécurité

### Bonnes Pratiques
1. **Jamais de secrets en clair** dans les fichiers versionnés
2. **Rotation régulière** des clés et secrets
3. **Accès restreint** aux fichiers de production
4. **Audit** des modifications via Git
5. **Chiffrement** des states Terraform

### Fichiers Sensibles à Exclure
Ajoutez à votre `.gitignore` :
```gitignore
# Secrets Terraform
environments/*/secrets.tfvars
environments/*/*.tfvars.local
terraform.tfstate*
.terraform/
*.tfplan
```

## 📊 Monitoring par Environnement

### Variables de Monitoring
Chaque environnement peut avoir sa propre configuration de monitoring :

```hcl
# dev: monitoring basique
notification_email = ""

# staging: monitoring pour tests
notification_email = "staging-team@company.com"

# prod: monitoring complet
notification_email = "alerts@company.com"
```

## 🔄 Workflow Recommandé

### 1. Développement Local
```bash
# Test en local avec dev
terraform plan -var-file="environments/dev/terraform.tfvars"
```

### 2. Tests en Staging
```bash
# Déploiement staging pour validation
terraform apply -var-file="environments/staging/terraform.tfvars"
```

### 3. Déploiement Production
```bash
# Déploiement production après validation
terraform apply -var-file="environments/prod/terraform.tfvars"
```

## 🚨 Points d'Attention

### Coûts
- **Dev** : Peut être arrêté la nuit (tag AutoShutdown=true)
- **Staging** : Utilisé ponctuellement pour les tests
- **Prod** : Fonctionnement 24/7, coûts optimisés mais performance prioritaire

### Données
- **Dev/Staging** : Données de test, pas de sauvegarde critique
- **Prod** : Données réelles, sauvegarde et haute disponibilité

### Scaling
- **Dev** : Scaling minimal (1-3 nœuds)
- **Staging** : Scaling modéré (2-5 nœuds)
- **Prod** : Scaling élevé (2-10 nœuds)

## 📞 Support

Pour modifier ces configurations :
1. Créer une branch dédiée
2. Modifier le fichier d'environnement approprié
3. Tester avec `terraform plan`
4. Créer une Pull Request
5. Reviewer et merger après validation

Pour les secrets, contacter l'équipe DevOps ou utiliser Azure Key Vault.

## 🔗 Liens Utiles

- [Guide de Déploiement Principal](../../docs/Azure-Deployment-Guide.md)
- [Variables Terraform](../variables.tf)
- [Modules Terraform](../modules/)
- [Documentation AKS](https://docs.microsoft.com/en-us/azure/aks/)
