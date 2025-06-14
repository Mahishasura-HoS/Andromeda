<?php
// index.php

// Inclure le fichier de configuration de la base de données
require_once 'config.php';

$message = ''; // Pour afficher des messages de succès ou d'erreur

// --- Logique d'ajout de produit ---
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['action']) && $_POST['action'] == 'ajouter') {
    $nom = $_POST['nom'];
    $description = $_POST['description'];
    $prix = $_POST['prix'];

    // Validation simple
    if (!empty($nom) && !empty($description) && is_numeric($prix) && $prix >= 0) {
        $stmt = $conn->prepare("INSERT INTO produits (nom, description, prix) VALUES (?, ?, ?)");
        $stmt->bind_param("ssd", $nom, $description, $prix); // "ssd" pour string, string, double (pour le prix)

        if ($stmt->execute()) {
            $message = "<p style='color:green;'>Produit ajouté avec succès !</p>";
        } else {
            $message = "<p style='color:red;'>Erreur lors de l'ajout du produit : " . $stmt->error . "</p>";
        }
        $stmt->close();
    } else {
        $message = "<p style='color:red;'>Veuillez remplir tous les champs correctement pour ajouter un produit.</p>";
    }
}

// --- Logique de suppression de produit ---
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['action']) && $_POST['action'] == 'supprimer') {
    $id_a_supprimer = $_POST['id_produit_supprimer'];

    if (is_numeric($id_a_supprimer)) {
        $stmt = $conn->prepare("DELETE FROM produits WHERE id = ?");
        $stmt->bind_param("i", $id_a_supprimer); // "i" pour integer

        if ($stmt->execute()) {
            if ($stmt->affected_rows > 0) {
                $message = "<p style='color:green;'>Produit supprimé avec succès !</p>";
            } else {
                $message = "<p style='color:orange;'>Aucun produit trouvé avec cet ID.</p>";
            }
        } else {
            $message = "<p style='color:red;'>Erreur lors de la suppression du produit : " . $stmt->error . "</p>";
        }
        $stmt->close();
    } else {
        $message = "<p style='color:red;'>ID de produit invalide pour la suppression.</p>";
    }
}

// --- Récupération des données pour l'affichage ---
$sql = "SELECT id, nom, description, prix FROM produits";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestion des Produits</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 900px; margin: auto; }
        h1, h2 { color: #333; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        form { margin-top: 20px; padding: 15px; border: 1px solid #eee; border-radius: 5px; background-color: #f9f9f9; }
        form label { display: block; margin-bottom: 5px; font-weight: bold; }
        form input[type="text"],
        form input[type="number"],
        form textarea { width: calc(100% - 22px); padding: 10px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 4px; }
        form input[type="submit"] {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        form input[type="submit"]:hover { background-color: #45a049; }
        .message { margin-bottom: 15px; padding: 10px; border-radius: 5px; }
        .message p { margin: 0; }
        .delete-form { display: inline; } /* Pour aligner le bouton Supprimer */
    </style>
</head>
<body>
    <div class="container">
        <h1>Gestion des Produits</h1>

        <?php if (!empty($message)): ?>
            <div class="message"><?php echo $message; ?></div>
        <?php endif; ?>

        <h2>Liste des Produits</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nom</th>
                    <th>Description</th>
                    <th>Prix</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <?php
                if ($result->num_rows > 0) {
                    // Afficher chaque ligne de données
                    while($row = $result->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . $row["id"]. "</td>";
                        echo "<td>" . htmlspecialchars($row["nom"]). "</td>";
                        echo "<td>" . htmlspecialchars($row["description"]). "</td>";
                        echo "<td>" . number_format($row["prix"], 2, ',', ' ') . " €</td>";
                        echo "<td>";
                        // Formulaire de suppression pour chaque ligne
                        echo "<form class='delete-form' method='POST' action='index.php'>";
                        echo "<input type='hidden' name='action' value='supprimer'>";
                        echo "<input type='hidden' name='id_produit_supprimer' value='" . $row["id"] . "'>";
                        echo "<input type='submit' value='Supprimer' style='background-color:#f44336;'>";
                        echo "</form>";
                        echo "</td>";
                        echo "</tr>";
                    }
                } else {
                    echo "<tr><td colspan='5'>Aucun produit trouvé.</td></tr>";
                }
                ?>
            </tbody>
        </table>

        <h2>Ajouter un Nouveau Produit</h2>
        <form method="POST" action="index.php">
            <input type="hidden" name="action" value="ajouter">
            <label for="nom">Nom :</label>
            <input type="text" id="nom" name="nom" required><br>

            <label for="description">Description :</label>
            <textarea id="description" name="description" rows="4"></textarea><br>

            <label for="prix">Prix :</label>
            <input type="number" id="prix" name="prix" step="0.01" min="0" required><br>

            <input type="submit" value="Ajouter le Produit">
        </form>
    </div>

    <?php
    // Fermer la connexion à la base de données à la fin du script
    $conn->close();
    ?>
</body>
</html>