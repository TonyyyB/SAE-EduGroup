#!/bin/bash

# Fonction pour vérifier si c'est Windows
is_windows() {
    [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]
}

# Définir l'URL du dépôt Git (à personnaliser)
REPO_URL="https://github.com/TonyyyB/SAE-EduGroup.git"
PROJECT_DIR="EduGroup"

# Détecter l'OS
if is_windows; then
    echo "⚙️ Vous êtes sous Windows."

    # Vérifier si Git est installé sous Windows
    echo "🔄 Vérification de Git sous Windows..."
    if ! command -v git &> /dev/null; then
        echo "⚠️ Git n'est pas installé. Installation en cours..."
        
        # Si Git n'est pas installé, l'installer (en utilisant l'installateur de Git pour Windows)
        echo "📥 Téléchargement de Git..."
        curl -LO https://github.com/git-for-windows/git/releases/download/v2.34.0.windows.2/Git-2.34.0-64-bit.exe
        echo "📦 Installation de Git..."
        start Git-2.34.0-64-bit.exe /VERYSILENT

        # Attendre l'installation de Git
        echo "✅ Git installé !"
    else
        echo "✅ Git est déjà installé."
    fi

    # Cloner le dépôt si le dossier n'existe pas
    if [ ! -d "$PROJECT_DIR" ]; then
        echo "📥 Clonage du dépôt $REPO_URL..."
        git clone "$REPO_URL"
    else
        echo "✅ Le projet est déjà cloné."
    fi

    # Vérifier si Python est installé sous Windows
    echo "🔄 Vérification de Python sous Windows..."
    if ! command -v python &> /dev/null; then
        echo "⚠️ Python n'est pas installé. Installation en cours..."
        
        # Si Python n'est pas installé, on tente de l'installer (en utilisant l'installateur officiel de Python)
        echo "📥 Téléchargement de Python..."
        curl -O https://www.python.org/ftp/python/3.9.7/python-3.9.7.exe
        echo "📦 Installation de Python..."
        start python-3.9.7.exe /quiet InstallAllUsers=1 PrependPath=1
        
        # Attendre que Python soit installé
        echo "✅ Python installé !"
    else
        echo "✅ Python est déjà installé."
    fi

    # Vérifier si pip est installé sous Windows
    echo "🔄 Vérification de pip sous Windows..."
    if ! command -v pip &> /dev/null; then
        echo "⚠️ pip n'est pas installé. Installation en cours..."
        python -m ensurepip --upgrade
        echo "✅ pip installé !"
    else
        echo "✅ pip est déjà installé."
    fi

    # Installer les dépendances du projet
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        echo "📦 Installation des dépendances depuis requirements.txt..."
        pip install --upgrade pip
        pip install -r "$PROJECT_DIR/requirements.txt"
        echo "✅ Installation des dépendances terminée !"
    else
        echo "❌ Fichier requirements.txt introuvable !"
        exit 1
    fi

    # Exécuter le script Python
    echo "🚀 Démarrage du projet..."
    python "$PROJECT_DIR/src/app.py"

else
    echo "⚙️ Vous êtes sous Linux (Ubuntu)."

    # Cloner le dépôt si le dossier n'existe pas
    if [ ! -d "$PROJECT_DIR" ]; then
        echo "📥 Clonage du dépôt $REPO_URL..."
        git clone "$REPO_URL"
    else
        echo "✅ Le projet est déjà cloné."
    fi

    # Mettre à jour les paquets et installer Python si nécessaire
    echo "🔄 Vérification de Python sous Linux..."
    if ! command -v python3 &> /dev/null; then
        echo "⚠️ Python3 n'est pas installé. Installation en cours..."
        sudo apt update && sudo apt install -y python3 python3-pip
    else
        echo "✅ Python3 est déjà installé."
    fi

    # Vérifier que pip est bien installé sous Linux
    echo "🔄 Vérification de pip sous Linux..."
    if ! command -v pip3 &> /dev/null; then
        echo "⚠️ pip3 n'est pas installé. Installation en cours..."
        sudo apt install -y python3-pip
    fi

    # Installer les dépendances du projet
    if [ -f "$PROJECT_DIR/requirements.txt" ]; then
        echo "📦 Installation des dépendances depuis requirements.txt..."
        pip3 install --upgrade pip
        pip3 install -r "$PROJECT_DIR/requirements.txt"
        echo "✅ Installation des dépendances terminée !"
    else
        echo "❌ Fichier requirements.txt introuvable !"
        exit 1
    fi

    # Exécuter le script Python
    echo "🚀 Démarrage du projet..."
    python3 "$PROJECT_DIR/src/app.py"
fi
