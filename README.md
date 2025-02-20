Théo RICHARD - M2 EFREI - Groupe 2

# TP Final : Développer une API d'Analyse de Sentiments

Vous travaillez pour une entreprise fictive, SocialMetrics AI, spécialisée dans l’analyse de données pour les réseaux
sociaux. Le client, Daunale Treupe, souhaite surveiller les opinions exprimées sur X (anciennement Twitter). Votre
mission est de concevoir un service permettant d'évaluer le sentiment des tweets en fonction de leur contenu

## Installation
Pour installer les dépendances du projet, exécutez la commande suivante :

```bash
pip install -r requirements.txt
```

## Utilisation
Assurez-vous d'avoir MYSQL installé et lancé sur votre machine.
Ensuite lancer le sript de création de la base de données :

```bash
py init_db.py
```

Puis celui d'entraînement des modèles :

```bash
py train_model.py
```

Enfin, lancez le serveur :

```bash
py main.py
```

Par défaut, le serveur est accessible à l'adresse suivante : http://localhost:5000
L'API expose une route POST à l'adresse http://localhost:5000/analyze qui permet de prédire le sentiment d'un tweet.
Exemple de requête :

```bash
curl -X POST "http://127.0.0.1:5000/analyze" -H "Content-Type: application/json" -d '{"tweet": "Trump est un leader exceptionnel !"}'
```

Pour lancer un entraînement automatique du modèle, vous pouvez utiliser la commande suivante sur Mac ou Linux :

```bash
0 0 * * 1 /usr/bin/python3 /chemin/vers/train_model.py >> /chemin/vers/logs.txt 2>&1
```

Et sur Windaube, vous pouvez utiliser le planificateur de tâches.







