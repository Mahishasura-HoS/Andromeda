

import sqlite3
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration de la Base de Données ---
DB_NAME = 'outils_manuels_complet.db'

# --- Chargement du modèle spaCy ---
try:
    nlp = spacy.load("fr_core_news_sm")
    print("Modèle spaCy 'fr_core_news_sm' chargé avec succès dans ia_core.")
except OSError:
    print("Erreur: Le modèle spaCy 'fr_core_news_sm' n'est pas trouvé. Veuillez l'installer avec :")
    print("python -m spacy download fr_core_news_sm")
    exit()

class IACore:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self._init_db()
        self._add_example_data() # Ajoutez les données d'exemple lors de l'initialisation de l'IA

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS outils (
                id INTEGER PRIMARY KEY,
                nom_outil TEXT NOT NULL UNIQUE,
                description TEXT,
                manuel_lien TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS problemes (
                id INTEGER PRIMARY KEY,
                outil_id INTEGER,
                titre_probleme TEXT NOT NULL,
                description_detaillee TEXT,
                vecteur_probleme BLOB,
                FOREIGN KEY (outil_id) REFERENCES outils(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY,
                probleme_id INTEGER,
                etape_solution TEXT NOT NULL,
                ordre INTEGER,
                FOREIGN KEY (probleme_id) REFERENCES problemes(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS symptomes (
                id INTEGER PRIMARY KEY,
                probleme_id INTEGER,
                phrase_symptome TEXT NOT NULL,
                vecteur_symptome BLOB,
                FOREIGN KEY (probleme_id) REFERENCES problemes(id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def _get_vector_from_text(self, text):
        """Génère le vecteur d'un texte en utilisant spaCy."""
        if not text:
            return np.zeros(nlp.vocab.vectors.shape[1], dtype=np.float32).tobytes() # Retourne un vecteur nul pour texte vide
        return nlp(text).vector.tobytes()

    def _add_example_data(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM outils")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return # Données déjà présentes

        print("Ajout des données d'exemple dans la base de données...")
        
        # Outils
        cursor.execute("INSERT INTO outils (nom_outil, description, manuel_lien) VALUES (?, ?, ?)", 
                       ("Perceuse sans fil", "Outil électrique pour percer des trous et visser.", "https://manuel-perceuse.fr"))
        perceuse_id = cursor.lastrowid

        cursor.execute("INSERT INTO outils (nom_outil, description, manuel_lien) VALUES (?, ?, ?)", 
                       ("Scie circulaire", "Outil pour couper le bois en ligne droite.", "https://manuel-scie-circulaire.fr"))
        scie_id = cursor.lastrowid

        cursor.execute("INSERT INTO outils (nom_outil, description, manuel_lien) VALUES (?, ?, ?)", 
                       ("Ponceuse excentrique", "Outil pour poncer des surfaces lisses.", "https://manuel-ponceuse.fr"))
        ponceuse_id = cursor.lastrowid

        # Problèmes et Solutions pour Perceuse
        probleme1_perceuse_titre = "Perceuse ne démarre pas"
        probleme1_perceuse_desc = "La perceuse ne s'allume pas ou ne tourne pas du tout lorsque le bouton est pressé."
        probleme1_perceuse_vec = self._get_vector_from_text(probleme1_perceuse_desc)
        cursor.execute("INSERT INTO problemes (outil_id, titre_probleme, description_detaillee, vecteur_probleme) VALUES (?, ?, ?, ?)", 
                       (perceuse_id, probleme1_perceuse_titre, probleme1_perceuse_desc, probleme1_perceuse_vec))
        pb1_perceuse_id = cursor.lastrowid

        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb1_perceuse_id, "Vérifiez que la batterie est complètement chargée et bien insérée.", 1))
        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb1_perceuse_id, "Nettoyez les contacts de la batterie et de l'outil.", 2))
        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb1_perceuse_id, "Testez avec une autre batterie si disponible.", 3))

        symptome1_perceuse_phrase = "Ma perceuse ne s'allume plus"
        cursor.execute("INSERT INTO symptomes (probleme_id, phrase_symptome, vecteur_symptome) VALUES (?, ?, ?)", 
                       (pb1_perceuse_id, symptome1_perceuse_phrase, self._get_vector_from_text(symptome1_perceuse_phrase)))
        symptome2_perceuse_phrase = "La perceuse ne tourne pas"
        cursor.execute("INSERT INTO symptomes (probleme_id, phrase_symptome, vecteur_symptome) VALUES (?, ?, ?)", 
                       (pb1_perceuse_id, symptome2_perceuse_phrase, self._get_vector_from_text(symptome2_perceuse_phrase)))

        probleme2_perceuse_titre = "Manque de puissance"
        probleme2_perceuse_desc = "La perceuse n'a pas assez de force pour percer ou visser correctement."
        probleme2_perceuse_vec = self._get_vector_from_text(probleme2_perceuse_desc)
        cursor.execute("INSERT INTO problemes (outil_id, titre_probleme, description_detaillee, vecteur_probleme) VALUES (?, ?, ?, ?)", 
                       (perceuse_id, probleme2_perceuse_titre, probleme2_perceuse_desc, probleme2_perceuse_vec))
        pb2_perceuse_id = cursor.lastrowid
        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb2_perceuse_id, "Vérifiez le niveau de charge de la batterie.", 1))
        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb2_perceuse_id, "Utilisez une mèche ou un embout adapté au matériau.", 2))
        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb2_perceuse_id, "Inspectez le mandrin pour tout blocage.", 3))

        symptome3_perceuse_phrase = "Ma perceuse est faible"
        cursor.execute("INSERT INTO symptomes (probleme_id, phrase_symptome, vecteur_symptome) VALUES (?, ?, ?)", 
                       (pb2_perceuse_id, symptome3_perceuse_phrase, self._get_vector_from_text(symptome3_perceuse_phrase)))
        symptome4_perceuse_phrase = "Elle n'a pas de force"
        cursor.execute("INSERT INTO symptomes (probleme_id, phrase_symptome, vecteur_symptome) VALUES (?, ?, ?)", 
                       (pb2_perceuse_id, symptome4_perceuse_phrase, self._get_vector_from_text(symptome4_perceuse_phrase)))


        # Problèmes et Solutions pour Scie Circulaire
        probleme1_scie_titre = "Coupes imprécises ou inégales"
        probleme1_scie_desc = "La scie ne coupe pas droit ou laisse des bords rugueux."
        probleme1_scie_vec = self._get_vector_from_text(probleme1_scie_desc)
        cursor.execute("INSERT INTO problemes (outil_id, titre_probleme, description_detaillee, vecteur_probleme) VALUES (?, ?, ?, ?)", 
                       (scie_id, probleme1_scie_titre, probleme1_scie_desc, probleme1_scie_vec))
        pb1_scie_id = cursor.lastrowid
        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb1_scie_id, "Vérifiez l'alignement de la lame par rapport au guide.", 1))
        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb1_scie_id, "Assurez-vous que la lame est propre et affûtée, remplacez-la si nécessaire.", 2))
        cursor.execute("INSERT INTO solutions (probleme_id, etape_solution, ordre) VALUES (?, ?, ?)", (pb1_scie_id, "Fixez solidement le matériau à couper.", 3))
        
        symptome1_scie_phrase = "Ma scie ne coupe pas droit"
        cursor.execute("INSERT INTO symptomes (probleme_id, phrase_symptome, vecteur_symptome) VALUES (?, ?, ?)", 
                       (pb1_scie_id, symptome1_scie_phrase, self._get_vector_from_text(symptome1_scie_phrase)))
        symptome2_scie_phrase = "Les bords sont rugueux après la coupe"
        cursor.execute("INSERT INTO symptomes (probleme_id, phrase_symptome, vecteur_symptome) VALUES (?, ?, ?)", 
                       (pb1_scie_id, symptome2_scie_phrase, self._get_vector_from_text(symptome2_scie_phrase)))

        print("Données d'exemple ajoutées à la base de données.")
        conn.commit()
        conn.close()

    def process_query(self, user_query):
        """
        Traite la requête de l'utilisateur et renvoie le conseil le plus pertinent.
        C'est la fonction principale que le chatbot appellera.
        """
        user_query_doc = nlp(user_query.lower())
        if not user_query_doc.has_vector:
            return {
                "status": "error",
                "message": "Le modèle spaCy n'a pas de vecteurs pour cette requête."
            }
        
        user_query_vector = user_query_doc.vector

        best_match, similarity = self._get_best_match(user_query_vector)

        if best_match and similarity > 0.6: # Seuil de confiance
            problem_id, problem_title, tool_name, _ = best_match
            solutions = self._get_solutions_for_problem(problem_id)
            manuel_link = self._get_tool_manual_link(tool_name)

            return {
                "status": "success",
                "tool_name": tool_name,
                "problem_title": problem_title,
                "solutions": solutions,
                "manuel_link": manuel_link,
                "confidence": float(similarity)
            }
        else:
            return {
                "status": "not_found",
                "message": "Désolé, je n'ai pas pu identifier un problème spécifique avec les informations que vous avez fournies. Pouvez-vous être plus précis sur l'outil ou le symptôme ?"
            }

    def _get_best_match(self, user_query_vector):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        best_match = None
        max_similarity = -1.0

        # D'abord, essayer de faire correspondre avec les symptômes
        cursor.execute("SELECT p.id, p.titre_probleme, o.nom_outil, s.vecteur_symptome FROM symptomes s JOIN problemes p ON s.probleme_id = p.id JOIN outils o ON p.outil_id = o.id")
        symptom_rows = cursor.fetchall()

        for problem_id, problem_title, tool_name, symptom_vec_bytes in symptom_rows:
            symptom_vector = np.frombuffer(symptom_vec_bytes, dtype=np.float32)
            if user_query_vector.shape == symptom_vector.shape:
                similarity = cosine_similarity(user_query_vector.reshape(1, -1), symptom_vector.reshape(1, -1))[0][0]
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_match = (problem_id, problem_title, tool_name, similarity)

        # Si pas de bonne correspondance via les symptômes ou similarité trop basse, essayer les problèmes
        if best_match is None or max_similarity < 0.6: # Seuil de similarité pour les symptômes
            cursor.execute("SELECT p.id, p.titre_probleme, o.nom_outil, p.vecteur_probleme FROM problemes p JOIN outils o ON p.outil_id = o.id")
            problem_rows = cursor.fetchall()
            for problem_id, problem_title, tool_name, problem_vec_bytes in problem_rows:
                problem_vector = np.frombuffer(problem_vec_bytes, dtype=np.float32)
                if user_query_vector.shape == problem_vector.shape:
                    similarity = cosine_similarity(user_query_vector.reshape(1, -1), problem_vector.reshape(1, -1))[0][0]
                    if similarity > max_similarity:
                        max_similarity = similarity
                        best_match = (problem_id, problem_title, tool_name, similarity)

        conn.close()
        return best_match, max_similarity

    def _get_solutions_for_problem(self, problem_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT etape_solution FROM solutions WHERE probleme_id = ? ORDER BY ordre", (problem_id,))
        solutions = [row[0] for row in cursor.fetchall()]
        conn.close()
        return solutions

    def _get_tool_manual_link(self, outil_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT manuel_lien FROM outils WHERE nom_outil = ?", (outil_name,))
        link = cursor.fetchone()
        conn.close()
        return link[0] if link else "Non disponible"

# Pour tester ia_core indépendamment (non nécessaire pour le fonctionnement global)
if __name__ == "__main__":
    ia_core_instance = IACore()
    print("\nTest de l'IA (ia_core.py) :")
    
    # Test 1: Problème connu
    result = ia_core_instance.process_query("Ma perceuse ne s'allume plus")
    print("\nRequête: Ma perceuse ne s'allume plus")
    print(result)

    # Test 2: Problème non connu
    result = ia_core_instance.process_query("Mon décapeur thermique fait un bruit bizarre")
    print("\nRequête: Mon décapeur thermique fait un bruit bizarre")
    print(result)

    # Test 3: Requête vague
    result = ia_core_instance.process_query("J'ai un souci avec ma scie")
    print("\nRequête: J'ai un souci avec ma scie")
    print(result)