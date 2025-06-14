<?php
// telecharger.php

require_once 'config.php';

if (isset($_GET['id']) && is_numeric($_GET['id'])) {
    $id = $_GET['id'];

    $stmt = $conn->prepare("SELECT nom_fichier, type_fichier, contenu_fichier FROM fichiers WHERE id = ?");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows == 1) {
        $stmt->bind_result($nom_fichier, $type_fichier, $contenu_fichier);
        $stmt->fetch();

        header("Content-Type: " . $type_fichier);
        header("Content-Disposition: attachment; filename=\"" . $nom_fichier . "\"");
        header("Content-Length: " . strlen($contenu_fichier));

        echo $contenu_fichier;
    } else {
        echo "Fichier non trouvé.";
    }

    $stmt->close();
} else {
    echo "ID de fichier invalide.";
}

$conn->close();
?>