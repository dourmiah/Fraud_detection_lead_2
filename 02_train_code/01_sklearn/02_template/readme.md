# Faire tourner un code de training qui utilise sklearn

On parle ici de sklearn, la méthode serait la même si on souhaitait utiliser TensorFlow. Dans tous les cas, il va falloir :

1. Construire une image Dockerfile qui contiendra sklearn ainsi que les autres bibliothèque nécessaire à l'execution du code d'entrainement ``train.py``
1. Construire un code d'entrainement du modèle qui :
    * Va chercher les données sur un serveur S3
    * Definit un modèle
    * Entraine ce dernier sur le jeu de train
    * Fait des prédictions sur le jeu de test
    * Calcul les différents métrics
    * Envoie les paramètres, les métrics et les tags de l'entrainement du modèle sur le serveur mlflow tracking qui est sur Heroku
    * Envoie les artifacts du training sur le disque AWS S3

## Adpatation et construction de l'image Docker
* Aller dans ``01_images_for_model_trainers\01_sklearn_trainer``
* Modifier le fichier ``requirements.txt`` comme indiqué ci-dessous

Bien sûr on pourrait choisir de dupliquer le répertoire afin de faire sans altérer le répertoire initial.

<p align="center">
<img src="./assets/img19.png" alt="drawing" width="600"/>
<p>

* Executer ``.\build_sklearn_fraud_trainer.ps1``

## Code d'entrainement du modèle
* À titre d'exemple on va partir sur un modèle à base de SMOTE et de RandomForest
* Le code va aller chercher les données sur un disque S3
* Il va stocker les paramètres et les résultats sur le serveur mlflow tracking
* Il va sauvegarder le modèle ainsi que les artifacts de l'entrainement sur un disque S3
    * Outre tous les paramètres du modèle
    * Il sauvegarde une matrice de confusion et une courbe ROC AUC sous forme d'image ``.png``
    * Il y aura une copie locale des images dans un sous répertoire ``./img``
        * les images sont time-stampées
* Le code va mettre aussi en place un mécanisme de log
* Enfin le code permet (mais ce n'est pas obligatoire) de gérer des paramètres
* Le code est 
    * largment commenté
    * objet 
    * d'une longueur de 250 lignes
    * on instancie une classe `ModelTrainer` et on appelle la méthode ``run()`` 

Pour lancer le code : 
* Dans le répertoire ``02_train_code\01_sklearn\02_template``
* Il peut être utile de préciser dans le fichier ``secrets.ps1`` le nom de l'expérience sous lequelle vous souhaitez retrouver ce ou ces entrainements. Le nom de l'expérience se retrouve en haut à gauche de la page web sur serveur mlflow tracking.
* Si vous avez renommé l'image Docker dans laquelle va s'exécuter le ``train.py`` il faut le préciser dans le fichier `MLproject`
* Quand tout est prêt, il faut executer ``./run_training.ps1``

Retrouvez ensuite les paramètres, les tags et les résultats (metrics) de l'entrainement sur le serveur mlflow tracking

<p align="center">
<img src="./assets/img20.png" alt="drawing" width="600"/>
<p>


Retrouvez aussi et les artifacts de l'entrainement

<p align="center">
<img src="./assets/img21.png" alt="drawing" width="600"/>
<p>


Outre les informations pour pouvoir inférer vous retrouvez aussi sous forme d'artifacts, des graphes

<p align="center">
<img src="./assets/img22.png" alt="drawing" width="600"/>
<p>


Si besoin, le réperoire local comprend un fichier de log et le répertoire ``./img`` contient une copie des images ``.png``

<p align="center">
<img src="./assets/img23.png" alt="drawing" width="600"/>
<p>




## Comment faire pour écrire son propre code d'entrainement ?

1. Dupliquer le répertoire `02_train_code\01_sklearn\02_template`
1. Supprimer le répertoire ``./assets``
1. Supprimer le répertoire ``./img``
1. Supprimer ce fichier `readme.md`
1. Supprimer le fichier `train.log`
1. Vérifier que le fichier ``MLproject`` 
    * Mentionne l'image dans laquelle vous souahitez que le code ``train.py`` s'exécute
    * Si le code ``train.py`` doit accepter des paramètres, inspirez-vous de la section ``parameters`` qui est pour l'instant commentée.
1. Dans le fichier `secrets.ps1` ajuster la valeur de la variable ``MLFLOW_EXPERIMENT_NAME``
1. Modifier le code ``train.py``
    * Commencez peut être par modifier la méthode ``train_model()`` afin d'utiliser un autre modèle dans le pipeline
        * Le coeur de la méthode est un pipeline dans lequel on retrouve le modèle
        * Ensuite il y a un ``.fit()``
        * Autour de ces quelques lignes on a le code nécessaire pour mesurer le temps d'execution. Ni touchez pas pour l'instant.
        * Le temps d'execution est inscrit dans le fichier de log ainsi qu'en tant que metric de l'entrainement sur le serveur mlflwo tracking
    
```python
def train_model(self, X_train, y_train):

    start_time = time.time()

    # SMOTE + RandomForest
    pipeline = imbpipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("smote", SMOTE(random_state=42)),
            (
                "classifier",
                RandomForestClassifier(n_estimators=k_N_Estimators, random_state=42, class_weight="balanced"),
            ),
        ]
    )

    pipeline.fit(X_train[self.numeric_columns], y_train)

    mlflow.log_metric("train_model_time", round(time.time() - start_time, 2))
    logger.info(f"train_model : {round(time.time() - start_time, 2)} sec.")
    return pipeline
```
    
Dans un seconde temps :     
* Si votre modèle utilise des valeurs de paramètres (`n_estimators`, `C`, `gamma`...) je vous propose 
    1. de les déclarer sous forme de constantes en haut du code source. Inspirez-vous de la ligne `k_N_Estimators = 100` par exemple. 
    1. D'enregitrer ce paramètre dans la méthode `log_tags_and_parameters()`. Inspirez-vous de la ligne : `mlflow.log_param("N Estimators", k_N_Estimators)`
* Si votre entrainement nécessite des tags supplémentaires, appliquez la même méthode :
    1. définition sous forme de constante au début du code source
    1. sauvegarde du tag dans la méthode `log_tags_and_parameters()`
    1. Par exemple, pensez à metre à jour ``k_Author`` avec votre propre nom








