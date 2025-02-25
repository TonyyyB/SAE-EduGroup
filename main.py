import os
import subprocess
import sys

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirement.txt"])
        print("\n✅ Installation des dépendances terminée !\n")
    except subprocess.CalledProcessError:
        print("\n❌ Erreur lors de l'installation des dépendances.\n")
        sys.exit(1)

def launch_project():
    print("Lancement du projet...\n")
    try:
        subprocess.run([sys.executable, "src/app.py"])
    except FileNotFoundError:
        print("\n❌ Le fichier app.py n'existe pas.\n")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
    launch_project()
