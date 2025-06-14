<?php
// index.php

require_once 'config.php';

$message = ''; // Pour afficher des messages de succès ou d'erreur

// --- Logique de téléchargement de fichier ---
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['action']) && $_POST['action'] == 'telecharger') {
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
}

// --- Logique de suppression de fichier ---
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_POST['action']) && $_POST['action'] == 'supprimer') {
    $id_a_supprimer = $_POST['id_fichier_supprimer'];

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
}

// --- Récupération des données pour l'affichage ---
$sql = "SELECT id, nom_fichier, type_fichier FROM fichiers ORDER BY id DESC";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestionnaire de Fichiers</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        /* Variables CSS pour un thème rouge et bleu */
        :root {
            --primary-color: #E53935; /* Rouge vif */
            --secondary-color: #1976D2; /* Bleu profond */
            --tertiary-color: #FFEB3B; /* Jaune pour certains accents ou avertissements */
            --text-color: #333;
            --light-bg: #f5f5f5;
            --white-bg: #ffffff;
            --border-color: #e0e0e0;
            --box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            --header-text: #fff;
        }

        body {
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
            background-color: var(--light-bg);
            color: var(--text-color);
            line-height: 1.6;
        }

        .header {
            background-color: var(--primary-color);
            color: var(--header-text);
            padding: 15px 0;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .container {
            max-width: 960px;
            margin: 30px auto;
            padding: 25px;
            background-color: var(--white-bg);
            border-radius: 10px;
            box-shadow: var(--box-shadow);
        }

        h1, h2 {
            text-align: center;
            color: var(--secondary-color); /* Utilisez le bleu pour les titres */
            margin-bottom: 25px;
            font-weight: 700;
        }

        /* Styles des messages d'alerte */
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            font-weight: bold;
            display: flex;
            align-items: center;
        }
        .alert.success {
            background-color: #e8f5e9; /* Vert très pâle */
            color: #4CAF50;
            border: 1px solid #81C784;
        }
        .alert.error {
            background-color: #ffebee; /* Rouge très pâle */
            color: var(--primary-color);
            border: 1px solid #EF9A9A;
        }
        .alert.warning {
            background-color: #fffde7; /* Jaune très pâle */
            color: #FFC107;
            border: 1px solid #FFD54F;
        }
        .alert::before {
            content: 'ℹ️';
            margin-right: 10px;
            font-size: 1.2em;
        }
        .alert.success::before { content: '✅'; }
        .alert.error::before { content: '❌'; }
        .alert.warning::before { content: '⚠️'; }


        /* Styles du tableau */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 25px;
            background-color: var(--white-bg);
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }
        th {
            background-color: var(--secondary-color); /* En-têtes de tableau en bleu */
            color: var(--header-text);
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.9em;
        }
        tr:nth-child(even) {
            background-color: var(--light-bg);
        }
        tr:hover {
            background-color: var(--border-color);
            transition: background-color 0.3s ease;
        }
        td:last-child {
            text-align: center;
        }
        th:first-child { border-top-left-radius: 8px; }
        th:last-child { border-top-right-radius: 8px; }


        /* Styles des formulaires */
        form {
            background-color: var(--light-bg);
            padding: 25px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-top: 30px;
        }
        form label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--text-color);
        }
        input[type="file"] {
            display: block;
            width: calc(100% - 22px);
            padding: 12px;
            margin-bottom: 15px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            font-size: 1em;
            background-color: var(--white-bg);
            cursor: pointer;
            box-sizing: border-box;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }
        input[type="file"]:focus {
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.2); /* Ombre légère bleu au focus */
            outline: none;
        }
        
        /* Styles des boutons */
        .btn {
            display: inline-block;
            padding: 10px 20px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 600;
            text-align: center;
            text-decoration: none;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        .btn-primary {
            background-color: var(--secondary-color); /* Bouton principal en bleu */
            color: white;
        }
        .btn-primary:hover {
            background-color: #1565C0; /* Bleu plus foncé au survol */
            transform: translateY(-2px);
        }
        .btn-danger {
            background-color: var(--primary-color); /* Bouton supprimer en rouge */
            color: white;
            margin-left: 5px;
        }
        .btn-danger:hover {
            background-color: #C62828; /* Rouge plus foncé au survol */
            transform: translateY(-2px);
        }

        .delete-form {
            display: inline-block;
        }

        /* Lien de téléchargement de fichier */
        .file-link {
            text-decoration: none;
            color: var(--secondary-color); /* Lien en bleu */
            font-weight: 500;
        }
        .file-link:hover {
            text-decoration: underline;
        }

        /* Media queries pour la responsivité */
        @media (max-width: 768px) {
            .container {
                margin: 20px;
                padding: 15px;
            }
            table, thead, tbody, th, td, tr {
                display: block;
            }
            thead tr {
                position: absolute;
                top: -9999px;
                left: -9999px;
            }
            tr { border: 1px solid var(--border-color); margin-bottom: 15px; border-radius: 8px;}
            td {
                border: none;
                border-bottom: 1px solid var(--border-color);
                position: relative;
                padding-left: 50%;
                text-align: right;
            }
            td:before {
                position: absolute;
                top: 6px;
                left: 6px;
                width: 45%;
                padding-right: 10px;
                white-space: nowrap;
                text-align: left;
                font-weight: bold;
                color: var(--secondary-color); /* Labels en bleu */
            }
            /* Labels pour les colonnes en mode mobile */
            td:nth-of-type(1):before { content: "ID:"; }
            td:nth-of-type(2):before { content: "Nom Fichier:"; }
            td:nth-of-type(3):before { content: "Type:"; }
            td:nth-of-type(4):before { content: "Actions:"; }
            
            td:last-child {
                border-bottom: none;
            }
            .delete-form {
                display: block;
                text-align: center;
                margin-top: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Gestionnaire de Fichiers</h1>
    </div>

    <div class="container">
        <?php if (!empty($message)): ?>
            <?php echo $message; ?>
        <?php endif; ?>

        <h2>Liste des Fichiers</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nom du Fichier</th>
                    <th>Type</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <?php
                if ($result->num_rows > 0) {
                    while($row = $result->fetch_assoc()) {
                        echo "<tr>";
                        echo "<td>" . $row["id"]. "</td>";
                        echo "<td><a href='telecharger.php?id=" . $row["id"] . "' class='file-link' target='_blank'>" . htmlspecialchars($row["nom_fichier"]). "</a></td>";
                        echo "<td>" . htmlspecialchars($row["type_fichier"]). "</td>";
                        echo "<td>";
                        echo "<form class='delete-form' method='POST' action='index.php'>";
                        echo "<input type='hidden' name='action' value='supprimer'>";
                        echo "<input type='hidden' name='id_fichier_supprimer' value='" . $row["id"] . "'>";
                        echo "<button type='submit' class='btn btn-danger'>Supprimer</button>";
                        echo "</form>";
                        echo "</td>";
                        echo "</tr>";
                    }
                } else {
                    echo "<tr><td colspan='4'>Aucun fichier trouvé. Téléchargez-en un ci-dessous !</td></tr>";
                }
                ?>
            </tbody>
        </table>

        <h2>Télécharger un Nouveau Fichier</h2>
        <form method="POST" action="index.php" enctype="multipart/form-data">
            <input type="hidden" name="action" value="telecharger">
            <label for="fichier">Sélectionner un fichier :</label>
            <input type="file" id="fichier" name="fichier" required><br>

            <button type="submit" class="btn btn-primary">Télécharger le Fichier</button>
        </form>
    </div>

    <?php
    $conn->close();
    ?>
</body>
</html>