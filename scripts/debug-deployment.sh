#!/bin/bash

# Script de diagnostic pour déploiement Kubernetes
# Usage: ./debug-deployment.sh [NAMESPACE]

NAMESPACE=${1:-"lake-holidays-prod"}

echo "🔍 Diagnostic du déploiement dans le namespace: $NAMESPACE"
echo "============================================================"

echo ""
echo "📊 État des déploiements:"
kubectl get deployments -n $NAMESPACE

echo ""
echo "📦 État des pods:"
kubectl get pods -n $NAMESPACE -o wide

echo ""
echo "🔍 Détails des pods en erreur:"
kubectl get pods -n $NAMESPACE --field-selector=status.phase!=Running --field-selector=status.phase!=Succeeded

echo ""
echo "📋 Événements récents:"
kubectl get events -n $NAMESPACE --sort-by='.firstTimestamp' | tail -20

echo ""
echo "🏥 Vérification des health checks backend:"
BACKEND_PODS=$(kubectl get pods -n $NAMESPACE -l component=backend -o jsonpath='{.items[*].metadata.name}')

for pod in $BACKEND_PODS; do
    echo "Pod: $pod"
    echo "  Status: $(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.phase}')"
    
    echo "  Readiness: $(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}')"
    
    echo "  Restart count: $(kubectl get pod $pod -n $NAMESPACE -o jsonpath='{.status.containerStatuses[0].restartCount}')"
    
    echo "  Last logs (30 lines):"
    kubectl logs $pod -n $NAMESPACE --tail=30 | sed 's/^/    /'
    
    echo ""
done

echo ""
echo "🔍 Configuration des services:"
kubectl get services -n $NAMESPACE

echo ""
echo "🌐 Configuration des ingress:"
kubectl get ingress -n $NAMESPACE

echo ""
echo "💾 État des PVC:"
kubectl get pvc -n $NAMESPACE

echo ""
echo "📊 Utilisation des ressources:"
kubectl top pods -n $NAMESPACE 2>/dev/null || echo "Metrics server non disponible"

echo ""
echo "🔧 Configuration des configmaps:"
kubectl get configmaps -n $NAMESPACE

echo ""
echo "🔐 Configuration des secrets:"
kubectl get secrets -n $NAMESPACE

echo ""
echo "============================================================"
echo "✅ Diagnostic terminé"
