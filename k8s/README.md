# Manifests Kubernetes - Lake Holidays Challenge

Ce dossier contient tous les manifests Kubernetes nécessaires pour déployer l'application Lake Holidays Challenge sur Azure Kubernetes Service (AKS).

## 📁 Structure des Fichiers

```
k8s/
├── 00-namespace-config.yaml    # Namespace, ServiceAccount, ConfigMap, Secrets
├── 01-backend-deployment.yaml  # Déploiement Backend (FastAPI + PostgreSQL + Redis)
├── 02-storage.yaml            # PersistentVolumeClaims pour la persistance
├── 03-frontend-deployment.yaml # Déploiement Frontend (React + Nginx)
├── 04-ingress.yaml            # Ingress + NetworkPolicy pour l'exposition
├── 05-autoscaling.yaml        # HPA et PodDisruptionBudget
├── 06-key-vault-secrets.yaml  # Intégration Azure Key Vault
└── README.md                  # Ce fichier
```

## 🚀 Déploiement

### Automatique (Recommandé)
Le déploiement se fait automatiquement via GitHub Actions lors du push sur `main` ou `develop`.

### Manuel
```bash
# Utiliser le script de déploiement
./scripts/deploy-k8s.sh dev latest

# Ou manuellement
cd k8s
for manifest in *.yaml; do
  envsubst < "$manifest" | kubectl apply -f -
done
```

## 📋 Variables à Substituer

Les manifests utilisent des variables qui doivent être substituées avant l'application :

| Variable | Description | Exemple |
|----------|-------------|---------|
| `{{ENVIRONMENT}}` | Environnement de déploiement | `dev`, `staging`, `prod` |
| `{{VERSION}}` | Version des images Docker | `latest`, `v1.2.3` |
| `{{CONTAINER_REGISTRY}}` | Registry des images | `myregistry.azurecr.io` |
| `{{KEY_VAULT_NAME}}` | Nom du Key Vault Azure | `lake-holidays-dev-kv` |
| `{{STORAGE_ACCOUNT_NAME}}` | Nom du Storage Account | `lakeholidaysdevstorage` |
| `{{FRONTEND_DOMAIN}}` | Domaine du frontend | `frontend-dev.example.com` |
| `{{BACKEND_DOMAIN}}` | Domaine du backend | `api-dev.example.com` |
| `{{OPENAI_ENDPOINT}}` | Endpoint Azure OpenAI | `https://myopenai.openai.azure.com/` |
| `{{SUBSCRIPTION_ID}}` | ID de souscription Azure | `12345678-1234-1234-1234-123456789012` |
| `{{RESOURCE_GROUP}}` | Nom du resource group | `lake-holidays-dev-rg` |
| `{{TENANT_ID}}` | ID du tenant Azure AD | `87654321-4321-4321-4321-210987654321` |
| `{{AKS_CLIENT_ID}}` | Client ID de l'identité AKS | `abcdef12-3456-7890-abcd-ef1234567890` |

## 🔧 Configuration par Environnement

### Développement (dev)
- **Namespace** : `lake-holidays-dev`
- **Replicas** : Backend=2, Frontend=2
- **Resources** : Limites réduites
- **Storage** : PVC 10Gi pour PostgreSQL, 5Gi pour Redis

### Staging
- **Namespace** : `lake-holidays-staging`
- **Replicas** : Backend=2, Frontend=2
- **Resources** : Limites modérées
- **Storage** : PVC 20Gi pour PostgreSQL, 10Gi pour Redis

### Production (prod)
- **Namespace** : `lake-holidays-prod`
- **Replicas** : Backend=3, Frontend=3
- **Resources** : Limites élevées
- **Storage** : PVC 50Gi pour PostgreSQL, 20Gi pour Redis

## 🏗️ Architecture des Applications

### Backend
```yaml
# Caractéristiques :
- Image: FastAPI avec PostgreSQL et Redis intégrés
- Ports: 8000 (HTTP), 5432 (PostgreSQL), 6379 (Redis)
- Volumes: postgres-pvc, redis-pvc, uploads-pvc
- Health checks: /health et /health/ready
- Auto-scaling: 2-10 replicas basé sur CPU/Memory
```

### Frontend
```yaml
# Caractéristiques :
- Image: React + Vite avec Nginx
- Port: 80 (HTTP)
- Configuration: Via variables d'environnement
- Health checks: GET /
- Auto-scaling: 2-5 replicas basé sur CPU
```

## 🔐 Secrets et Configuration

### ConfigMap (`lake-holidays-config`)
Contient la configuration non-sensible :
- Variables d'environnement de l'application
- Configuration des services Azure
- Paramètres de l'application

### Secrets Kubernetes (`lake-holidays-secrets`)
Synchronisé depuis Azure Key Vault :
- `JWT_SECRET_KEY` : Clé pour les tokens JWT
- `POSTGRES_PASSWORD` : Mot de passe PostgreSQL
- `REDIS_PASSWORD` : Mot de passe Redis
- `GOOGLE_CLIENT_SECRET` : Secret OAuth Google
- `MICROSOFT_CLIENT_SECRET` : Secret OAuth Microsoft
- `OPENAI_API_KEY` : Clé API OpenAI
- `AZURE_STORAGE_CONNECTION_STRING` : Chaîne de connexion du stockage

### Azure Key Vault Integration
Le CSI Secret Store Driver synchronise automatiquement les secrets depuis Azure Key Vault vers Kubernetes.

## 📦 Stockage

### PersistentVolumeClaims
1. **postgres-pvc** : Données PostgreSQL (managed-csi)
2. **redis-pvc** : Données Redis (managed-csi)  
3. **uploads-pvc** : Fichiers uploadés temporaires (azurefile-csi)

> **Note** : Les fichiers uploadés sont finalement stockés dans Azure Storage Account, le PVC est utilisé comme stockage temporaire.

## 🌐 Exposition et Réseau

### Ingress Controller
- **Type** : Azure Application Gateway Ingress Controller (AGIC)
- **SSL/TLS** : Certificats gérés automatiquement
- **WAF** : Web Application Firewall intégré
- **Load Balancing** : Répartition de charge automatique

### NetworkPolicy
- Isolation réseau entre namespaces
- Communication restreinte entre pods
- Accès contrôlé vers Azure services

## 📈 Auto-scaling et Haute Disponibilité

### Horizontal Pod Autoscaler (HPA)
```yaml
Backend:
  - Min: 2 replicas
  - Max: 10 replicas
  - Métriques: CPU 70%, Memory 80%

Frontend:
  - Min: 2 replicas
  - Max: 5 replicas
  - Métriques: CPU 70%
```

### PodDisruptionBudget (PDB)
- Maintient au moins 1 replica disponible pendant les mises à jour
- Assure la continuité de service

## 🔍 Monitoring et Debugging

### Health Checks
```bash
# Backend
kubectl exec -it deployment/backend -n lake-holidays-dev -- curl http://localhost:8000/health

# Frontend  
kubectl exec -it deployment/frontend -n lake-holidays-dev -- curl http://localhost:80/
```

### Logs
```bash
# Logs du backend
kubectl logs -l component=backend -n lake-holidays-dev -f

# Logs du frontend
kubectl logs -l component=frontend -n lake-holidays-dev -f

# Tous les logs de l'app
kubectl logs -l app=lake-holidays -n lake-holidays-dev -f
```

### Debug des Secrets
```bash
# Vérifier la synchronisation Key Vault
kubectl get secretproviderclass -n lake-holidays-dev
kubectl describe secretproviderclass lake-holidays-secrets -n lake-holidays-dev

# Vérifier les secrets
kubectl get secrets -n lake-holidays-dev
kubectl describe secret lake-holidays-secrets -n lake-holidays-dev
```

## 🛠️ Commandes Utiles

### État du Déploiement
```bash
# Vue d'ensemble
kubectl get all -n lake-holidays-dev

# Détails des pods
kubectl get pods -o wide -n lake-holidays-dev

# État des déploiements
kubectl get deployments -n lake-holidays-dev

# Services et ingress
kubectl get svc,ingress -n lake-holidays-dev
```

### Scaling Manuel
```bash
# Scaler le backend
kubectl scale deployment backend --replicas=5 -n lake-holidays-dev

# Scaler le frontend
kubectl scale deployment frontend --replicas=3 -n lake-holidays-dev
```

### Mises à Jour
```bash
# Mettre à jour l'image backend
kubectl set image deployment/backend backend=myregistry.azurecr.io/lake-holidays-backend:v1.2.3 -n lake-holidays-dev

# Mettre à jour l'image frontend
kubectl set image deployment/frontend frontend=myregistry.azurecr.io/lake-holidays-frontend:v1.2.3 -n lake-holidays-dev

# Vérifier le rollout
kubectl rollout status deployment/backend -n lake-holidays-dev
```

### Rollback
```bash
# Rollback vers la version précédente
kubectl rollout undo deployment/backend -n lake-holidays-dev

# Voir l'historique
kubectl rollout history deployment/backend -n lake-holidays-dev
```

## 🚨 Dépannage

### Problèmes Courants

1. **Pods en Pending**
   ```bash
   kubectl describe pod <pod-name> -n lake-holidays-dev
   # Vérifier les ressources et contraintes
   ```

2. **Images non trouvées**
   ```bash
   # Vérifier l'accès au registry
   kubectl get secrets -n lake-holidays-dev | grep regcred
   ```

3. **Secrets non synchronisés**
   ```bash
   # Vérifier Key Vault CSI Driver
   kubectl get pods -n kube-system | grep secrets-store
   kubectl logs -l app=secrets-store-csi-driver -n kube-system
   ```

4. **Problèmes de réseau**
   ```bash
   # Tester la connectivité
   kubectl exec -it deployment/backend -n lake-holidays-dev -- nslookup kubernetes.default
   ```

### Debugging Avancé
```bash
# Shell dans un pod
kubectl exec -it deployment/backend -n lake-holidays-dev -- /bin/bash

# Port forwarding pour test local
kubectl port-forward deployment/backend 8000:8000 -n lake-holidays-dev
kubectl port-forward deployment/frontend 3000:80 -n lake-holidays-dev

# Dump de la configuration
kubectl get configmap lake-holidays-config -o yaml -n lake-holidays-dev
```

## 📚 Ressources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AKS Documentation](https://docs.microsoft.com/en-us/azure/aks/)
- [Azure Key Vault CSI Driver](https://azure.github.io/secrets-store-csi-driver-provider-azure/)
- [Application Gateway Ingress Controller](https://docs.microsoft.com/en-us/azure/application-gateway/ingress-controller-overview)
