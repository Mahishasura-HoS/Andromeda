# Utilise une image Python slim comme base pour une taille réduite
FROM python:3.9-slim-buster

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installe les dépendances Python
# --no-cache-dir pour éviter de stocker le cache pip, réduisant la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# Télécharge le modèle linguistique SpaCy directement dans l'image
# "fr_core_news_md" est le modèle français de taille moyenne.
# Utilise "en_core_web_md" si tu préfères l'anglais, ou "fr_core_news_lg" pour le grand modèle.
RUN python -m spacy download fr_core_news_md

# Copie tous les autres fichiers du répertoire local dans le répertoire de travail du conteneur
# Ceci inclut chatbot_spacy.py et intents.json
COPY .. .

# Commande à exécuter quand le conteneur démarre
# C'est le point d'entrée de ton application
CMD ["python", "chatbot_spacy.py"]