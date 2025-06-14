<?php
// telecharger.php
require_once 'config.php';

if (isset($_GET['id']) && is_numeric($_GET['id'])) {
    $id_fichier = $_GET['id'];

    $stmt = $conn->prepare("SELECT nom_fichier, type_fichier, contenu_fichier FROM fichiers WHERE id = ?");
    $stmt->bind_param("i", $id_fichier);
    $stmt->execute();
    $stmt->bind_result($nom_fichier, $type_fichier, $contenu_fichier);
    $stmt->fetch();
    $stmt->close();
    $conn->close();

    if ($nom_fichier) {
        // En-têtes HTTP pour forcer le téléchargement du fichier
        header('Content-Description: File Transfer');
        header('Content-Type: ' . $type_fichier);
        header('Content-Disposition: attachment; filename="' . basename($nom_fichier) . '"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . strlen($contenu_fichier));
        ob_clean(); // Nettoie le buffer de sortie (très important pour éviter les caractères indésirables avant l'envoi du binaire)
        flush();    // Force l'envoi des headers et du contenu du buffer
        echo $contenu_fichier;
        exit;
    } else {
        die("Fichier non trouvé.");
    }
} else {
    die("ID de fichier invalide.");
}
?>