import json
import random
import spacy
import subprocess
from datetime import datetime

# Importer les modules scikit-learn nécessaires
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- 1. Charger les intentions ---
with open('intents.json', 'r', encoding='utf-8') as file:
    intents = json.load(file)

# --- 2. Charger le modèle SpaCy (le modèle français que nous allons télécharger dans Docker) ---
try:
    nlp = spacy.load("fr_core_news_md")
    print("Modèle SpaCy 'fr_core_news_md' chargé avec succès.")
except OSError:
    print("Le modèle SpaCy 'fr_core_news_md' n'a pas été trouvé. Assurez-vous qu'il est téléchargé.")
    print("Lancez 'python -m spacy download fr_core_news_md' si vous exécutez localement sans Docker.")
    exit()  # Quitte si le modèle n'est pas là

# --- 3. Préparer les données pour la vectorisation TF-IDF ---
# Nous allons créer une liste de tous les patterns et les mapper à leurs tags
all_patterns = []
pattern_to_tag = {}

for intent in intents['intents']:
    for pattern in intent['patterns']:
        all_patterns.append(pattern)
        pattern_to_tag[pattern] = intent['tag']

# Initialiser le vectoriseur TF-IDF
# Ceci va transformer nos phrases en vecteurs numériques
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_patterns)


# --- 4. Fonction pour traiter la requête utilisateur et prédire l'intention ---
def predict_intent(user_message):
    # Convertir le message utilisateur en vecteur TF-IDF
    user_tfidf = vectorizer.transform([user_message])

    # Calculer la similarité cosinus entre le message utilisateur et tous les patterns d'entraînement
    similarities = cosine_similarity(user_tfidf, tfidf_matrix)

    # Trouver l'indice du pattern le plus similaire
    best_match_index = np.argmax(similarities)
    best_score = similarities[0, best_match_index]

    # Définir un seuil de confiance. Tu peux ajuster cette valeur.
    # Si le score est trop bas, on considère que le chatbot n'a pas compris.
    confidence_threshold = 0.45  # Ajuste selon tes tests

    if best_score < confidence_threshold:
        return "fallback", 0.0  # Retourne un tag de repli et une faible confiance

    # Récupérer le tag correspondant au pattern le plus similaire
    matched_pattern = all_patterns[best_match_index]
    predicted_tag = pattern_to_tag[matched_pattern]

    return predicted_tag, best_score


# --- 5. Fonction pour obtenir la réponse basée sur le tag prédit ---
def get_response(tag):
    if tag == "fallback":
        return "Désolé, je n'ai pas compris. Pouvez-vous reformuler ?"

    for intent in intents['intents']:
        if intent['tag'] == tag:
            response = random.choice(intent['responses'])

            # Traiter les placeholders
            if "%TIME%" in response:
                response = response.replace("%TIME%", datetime.now().strftime("%H:%M"))
            # Ajouter d'autres placeholders ici si nécessaire

            return response

    # Devrait théoriquement ne jamais être atteint si le fallback est géré
    return "Une erreur inattendue est survenue."


# --- 6. Boucle principale du Chatbot ---
if __name__ == "__main__":
    print("Bienvenue dans votre chatbot SpaCy ! Tapez 'au revoir' pour quitter.")
    while True:
        user_input = input("Vous : ")
        if user_input.lower() in ["au revoir", "bye", "quitter"]:
            print("Chatbot : Au revoir !")
            break

        # Prédire l'intention
        tag, confidence = predict_intent(user_input)

        # Obtenir la réponse
        response = get_response(tag)

        print(f"Chatbot : {response}")
        # Optionnel: afficher la confiance pour le débogage
        # print(f"(DEBUG: Tag prédit: {tag}, Confiance: {confidence:.2f})")