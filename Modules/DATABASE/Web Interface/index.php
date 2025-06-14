<?php
// config.php
// Assurez-vous d'avoir ce fichier avec vos identifiants de connexion à la base de données.
// Exemple :
/*
<?php
$servername = "localhost";
$username = "root";
$password = "your_password"; // Modifiez ceci
$dbname = "votre_base_de_donnees"; // Modifiez ceci

// Créer une connexion
$conn = new mysqli($servername, $username, $password, $dbname);

// Vérifier la connexion
if ($conn->connect_error) {
    die("Connexion échouée : " . $conn->connect_error);
}
?>
*/

require_once 'config.php'; // Inclut le fichier de configuration de la base de données

$message = ''; // Pour afficher des messages de succès ou d'erreur à l'utilisateur

// --- Logique de téléchargement de fichier ---
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['action']) && $_POST['action'] == 'telecharger') {
    if (isset($_FILES['fichier']) && $_FILES['fichier']['error'] === UPLOAD_ERR_OK) {
        $nom_fichier = $_FILES['fichier']['name'];
        $type_fichier = $_FILES['fichier']['type'];
        $tmp_name = $_FILES['fichier']['tmp_name'];
        $contenu_fichier = file_get_contents($tmp_name); // Lire le contenu binaire du fichier

        // Préparer la requête pour éviter les injections SQL
        $stmt = $conn->prepare("INSERT INTO fichiers (nom_fichier, type_fichier, contenu_fichier) VALUES (?, ?, ?)");
        // 'sss' indique que les trois paramètres sont des chaînes de caractères
        $stmt->bind_param("sss", $nom_fichier, $type_fichier, $contenu_fichier);

        if ($stmt->execute()) {
            $message = "<div class='alert success'>Fichier téléchargé avec succès !</div>";
        } else {
            $message = "<div class='alert error'>Erreur lors du téléchargement du fichier : " . $stmt->error . "</div>";
        }
        $stmt->close(); // Fermer la déclaration préparée
    } else {
        $message = "<div class='alert warning'>Veuillez sélectionner un fichier à télécharger ou une erreur est survenue lors de l'upload.</div>";
    }
}

// --- Logique de suppression de fichier ---
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['action']) && $_POST['action'] == 'supprimer') {
    $id_a_supprimer = $_POST['id_fichier_supprimer'];

    // S'assurer que l'ID est un nombre pour éviter les problèmes de sécurité
    if (is_numeric($id_a_supprimer)) {
        // Préparer la requête de suppression
        $stmt = $conn->prepare("DELETE FROM fichiers WHERE id = ?");
        $stmt->bind_param("i", $id_a_supprimer); // 'i' indique que le paramètre est un entier

        if ($stmt->execute()) {
            // Vérifier si des lignes ont été affectées (si un fichier a bien été supprimé)
            if ($stmt->affected_rows > 0) {
                $message = "<div class='alert success'>Fichier supprimé avec succès !</div>";
            } else {
                $message = "<div class='alert warning'>Aucun fichier trouvé avec cet ID.</div>";
            }
        } else {
            $message = "<div class='alert error'>Erreur lors de la suppression du fichier : " . $stmt->error . "</div>";
        }
        $stmt->close(); // Fermer la déclaration préparée
    } else {
        $message = "<div class='alert warning'>ID de fichier invalide pour la suppression.</div>";
    }
}

// --- Récupération des données pour l'affichage (toujours exécuté pour afficher la liste) ---
$sql = "SELECT id, nom_fichier, type_fichier FROM fichiers ORDER BY id DESC";
$result = $conn->query($sql); // Exécuter la requête SQL

// IMPORTANT : La connexion à la base de données doit être fermée à la fin du script ou après utilisation.
// Dans cet exemple, elle est fermée après la génération du HTML.
// $conn->close(); // Cette ligne est déplacée à la fin du fichier HTML pour s'assurer que toutes les opérations sont faites.
?>