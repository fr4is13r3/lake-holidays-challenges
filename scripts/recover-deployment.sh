#!/bin/bash

# Script de récupération pour déploiement bloqué
# Usage: ./recover-deployment.sh [NAMESPACE]

NAMESPACE=${1:-"lake-holidays-prod"}

echo "🔄 Récupération du déploiement dans le namespace: $NAMESPACE"
echo "============================================================"

echo ""
echo "🛑 Arrêt du rollout en cours..."
kubectl rollout pause deployment/backend -n $NAMESPACE

echo ""
echo "🔍 État actuel des pods backend:"
kubectl get pods -n $NAMESPACE -l component=backend

echo ""
echo "📋 Événements récents pour le backend:"
kubectl get events -n $NAMESPACE --field-selector involvedObject.name=backend

echo ""
echo "🗑️ Suppression des pods en échec..."
kubectl get pods -n $NAMESPACE -l component=backend --field-selector=status.phase!=Running -o jsonpath='{.items[*].metadata.name}' | xargs -r kubectl delete pod -n $NAMESPACE

echo ""
echo "⏱️ Attente de 30 secondes..."
sleep 30

echo ""
echo "▶️ Reprise du rollout..."
kubectl rollout resume deployment/backend -n $NAMESPACE

echo ""
echo "⏳ Attente de la stabilisation (5 minutes max)..."
kubectl rollout status deployment/backend -n $NAMESPACE --timeout=300s

echo ""
echo "✅ État final:"
kubectl get pods -n $NAMESPACE -l component=backend

echo ""
echo "============================================================"
echo "🎉 Récupération terminée"
