<?php
// functions.php

/**
 * Gère le téléchargement d'un fichier dans la base de données.
 * @param mysqli $conn La connexion à la base de données.
 * @return string Le message de succès ou d'erreur HTML.
 */
function handleFileUpload(mysqli $conn): string {
    if (isset($_FILES['fichier']) && $_FILES['fichier']['error'] === UPLOAD_ERR_OK) {
        $nom_fichier = $_FILES['fichier']['name'];
        $type_fichier = $_FILES['fichier']['type'];
        $tmp_name = $_FILES['fichier']['tmp_name'];
        $contenu_fichier = file_get_contents($tmp_name);

        $stmt = $conn->prepare("INSERT INTO fichiers (nom_fichier, type_fichier, contenu_fichier) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $nom_fichier, $type_fichier, $contenu_fichier);

        if ($stmt->execute()) {
            $message = "<div class='alert success'>Fichier téléchargé avec succès !</div>";
        } else {
            $message = "<div class='alert error'>Erreur lors du téléchargement du fichier : " . $stmt->error . "</div>";
        }
        $stmt->close();
    } else {
        $message = "<div class='alert warning'>Veuillez sélectionner un fichier à télécharger ou une erreur est survenue lors de l'upload.</div>";
    }
    return $message;
}

/**
 * Gère la suppression d'un fichier de la base de données.
 * @param mysqli $conn La connexion à la base de données.
 * @param int $id_a_supprimer L'ID du fichier à supprimer.
 * @return string Le message de succès ou d'erreur HTML.
 */
function handleDeleteFile(mysqli $conn, int $id_a_supprimer): string {
    if (is_numeric($id_a_supprimer)) {
        $stmt = $conn->prepare("DELETE FROM fichiers WHERE id = ?");
        $stmt->bind_param("i", $id_a_supprimer);

        if ($stmt->execute()) {
            if ($stmt->affected_rows > 0) {
                $message = "<div class='alert success'>Fichier supprimé avec succès !</div>";
            } else {
                $message = "<div class='alert warning'>Aucun fichier trouvé avec cet ID.</div>";
            }
        } else {
            $message = "<div class='alert error'>Erreur lors de la suppression du fichier : " . $stmt->error . "</div>";
        }
        $stmt->close();
    } else {
        $message = "<div class='alert warning'>ID de fichier invalide pour la suppression.</div>";
    }
    return $message;
}

/**
 * Récupère la liste des fichiers depuis la base de données.
 * @param mysqli $conn La connexion à la base de données.
 * @return mysqli_result|false Les résultats de la requête ou false en cas d'erreur.
 */
function getFiles(mysqli $conn) {
    $sql = "SELECT id, nom_fichier, type_fichier FROM fichiers ORDER BY id DESC";
    return $conn->query($sql);
}
?>