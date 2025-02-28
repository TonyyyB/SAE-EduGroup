#!/bin/bash

# Activer le mode strict pour arrêter en cas d'erreur
set -e

# Définir le dépôt Git et le répertoire du projet
REPO_URL="https://<USERNAME>:<TOKEN>@github.com/TonyyyB/SAE-EduGroup.git"  # Remplacer <USERNAME> et <TOKEN> par tes infos GitHub
PROJECT_DIR="SAE-EduGroup"

echo "🖥 Détection du système..."
OS_TYPE="linux"

# Détecter le système d'exploitation
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    OS_TYPE="windows"
fi
echo "⚙️ Système détecté : $OS_TYPE"

# Cloner le dépôt s'il n'existe pas déjà
echo "🔄 Vérification du dépôt..."
if [ ! -d "$PROJECT_DIR" ]; then
    echo "📥 Clonage du dépôt $REPO_URL..."
    git clone "$REPO_URL"
else
    echo "✅ Le dépôt existe déjà."
fi

# Aller dans le dossier du projet
echo "🔄 Aller dans le dossier du projet $PROJECT_DIR"
cd "$PROJECT_DIR"

# Vérifier si c'est un dépôt Git valide
echo "🔄 Vérification du dépôt Git..."
if [ ! -d ".git" ]; then
    echo "❌ Ce n'est pas un dépôt Git valide !"
    exit 1
fi

# Mettre à jour les informations du dépôt distant
echo "🔄 Récupération des informations du dépôt distant..."
git fetch origin

# Vérifier si la branche develop existe sur le dépôt distant
echo "🔄 Vérification de la branche develop sur le dépôt distant..."
if git show-ref --verify --quiet refs/remotes/origin/develop; then
    echo "🔄 Passage à la branche develop..."
    git checkout develop
else
    echo "⚠️ La branche develop n'existe pas sur le dépôt distant."
    # Tentons de nous placer sur la branche principale (main)
    if git show-ref --verify --quiet refs/remotes/origin/main; then
        echo "🔄 Passage à la branche main..."
        git checkout main
    else
        echo "❌ Aucune branche principale (main) trouvée. Veuillez vérifier le dépôt."
        exit 1
    fi
fi

# Installation des dépendances selon le système
if [ "$OS_TYPE" == "linux" ]; then
    echo "🐧 Configuration sous Linux..."

    # Vérifier si Python3 est installé
    echo "🔄 Vérification de Python3..."
    if ! command -v python3 &> /dev/null; then
        echo "⚠️ Python3 n'est pas installé. Installation..."
        sudo apt update && sudo apt install -y python3 python3-pip
    else
        echo "✅ Python3 est déjà installé."
    fi

    # Vérifier si Tkinter est installé
    echo "🔄 Vérification de Tkinter..."
    if ! dpkg -l | grep -q python3-tk; then
        echo "⚠️ Tkinter n'est pas installé. Installation..."
        sudo apt install -y python3-tk
    else
        echo "✅ Tkinter est déjà installé."
    fi

    # Vérifier si pip3 est installé
    echo "🔄 Vérification de pip3..."
    if ! command -v pip3 &> /dev/null; then
        echo "⚠️ pip3 n'est pas installé. Installation..."
        sudo apt install -y python3-pip
    else
        echo "✅ pip3 est déjà installé."
    fi

    # Installer les dépendances Python
    echo "📦 Installation des dépendances Python..."
    pip3 install --upgrade pip
    pip3 install --break-system-packages -r requirements.txt

elif [ "$OS_TYPE" == "windows" ]; then
    echo "🪟 Configuration sous Windows..."

    # Vérifier si Python est installé
    echo "🔄 Vérification de Python..."
    if ! command -v python &> /dev/null; then
        echo "❌ Python n'est pas installé. Installez-le manuellement depuis https://www.python.org/downloads/"
        exit 1
    else
        echo "✅ Python est déjà installé."
    fi

    # Vérifier si pip est installé
    echo "🔄 Vérification de pip..."
    if ! command -v pip &> /dev/null; then
        echo "❌ pip n'est pas installé. Installez-le avec Python."
        exit 1
    else
        echo "✅ pip est déjà installé."
    fi

    # Installer les dépendances Python
    echo "📦 Installation des dépendances Python..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Vérifier si tkinterdnd2 est bien installé
echo "🔄 Vérification de tkinterdnd2..."
if ! python3 -c "import tkinterdnd2" &> /dev/null; then
    echo "⚠️ tkinterdnd2 n'est pas installé. Installation..."
    pip3 install tkinterdnd2
else
    echo "✅ tkinterdnd2 est déjà installé."
fi

# Vérifier si le fichier app.py existe et est accessible
echo "🔄 Vérification de l'existence du fichier app.py..."
if [ ! -f "src/app.py" ]; then
    echo "❌ Le fichier src/app.py est manquant. Veuillez vérifier le projet."
    exit 1
else
    echo "✅ Le fichier src/app.py est présent."
fi

# Lancer l'application
echo "🚀 Démarrage de l'application..."
python3 src/app.py
if [ $? -ne 0 ]; then
    echo "❌ Erreur lors du lancement de l'application. Code de sortie : $?"
    exit 1
else
    echo "✅ L'application a démarré avec succès !"
fi

# Garder le terminal ouvert (évite qu'il se ferme immédiatement)
echo "✅ Script terminé ! Appuyez sur Entrée pour fermer..."
read -r
