# Utiliser une image de base Python
FROM python:3.8-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le répertoire de travail
COPY . /app

# Installer les dépendances du projet
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exécuter les tests
CMD ["/bin/bash"]
