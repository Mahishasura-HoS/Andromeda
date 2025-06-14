<?php
// config.php
$servername = "localhost";
$username = "root";
$password = "your_password"; // Modifiez ceci avec votre mot de passe
$dbname = "votre_base_de_donnees"; // Modifiez ceci avec le nom de votre base de données

// Créer une connexion
$conn = new mysqli($servername, $username, $password, $dbname);

// Vérifier la connexion
if ($conn->connect_error) {
    die("Connexion échouée : " . $conn->connect_error);
}
?>