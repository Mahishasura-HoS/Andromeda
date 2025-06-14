<?php
// index.php

require_once 'config.php';       // Inclut la configuration de la base de données
require_once 'functions.php';     // Inclut les fonctions de gestion des fichiers

$message = ''; // Variable pour les messages d'alerte

// --- Traitement des requêtes POST (téléchargement ou suppression) ---
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_POST['action']) && $_POST['action'] == 'telecharger') {
        $message = handleFileUpload($conn);
    } elseif (isset($_POST['action']) && $_POST['action'] == 'supprimer') {
        $id_a_supprimer = isset($_POST['id_fichier_supprimer']) ? (int)$_POST['id_fichier_supprimer'] : 0;
        $message = handleDeleteFile($conn, $id_a_supprimer);
    }
}

// --- Récupération des données pour l'affichage ---
$result = getFiles($conn);

// --- Inclusion du template HTML ---
// Les variables $message et $result seront disponibles dans template.php
include 'template.php';

// --- Fermeture de la connexion à la base de données ---
$conn->close();
?>