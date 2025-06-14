CREATE TABLE IF NOT EXISTS fichiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_fichier VARCHAR(255) NOT NULL,
    type_fichier VARCHAR(100) NOT NULL,
    contenu_fichier LONGBLOB NOT NULL
);