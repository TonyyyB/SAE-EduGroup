#!/bin/bash

# Activer le mode strict pour arrêter en cas d'erreur
set -e

# Mettre à jour les paquets et installer Python si nécessaire
echo "🔄 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "⚠️ Python3 n'est pas installé. Installation en cours..."
    sudo apt update && sudo apt install -y python3 python3-pip
else
    echo "✅ Python3 est déjà installé."
fi

# Vérifier que pip est bien installé
if ! command -v pip3 &> /dev/null; then
    echo "⚠️ pip3 n'est pas installé. Installation en cours..."
    sudo apt install -y python3-pip
fi

# Installer les dépendances du projet
if [ -f "requirement.txt" ]; then
    echo "📦 Installation des dépendances depuis requirement.txt..."
    pip3 install --upgrade pip
    pip3 install -r requirement.txt
    echo "✅ Installation des dépendances terminée !"
else
    echo "❌ Fichier requirement.txt introuvable !"
    exit 1
fi

# Exécuter le script Python
echo "🚀 Démarrage du projet..."
python3 src/app.py
