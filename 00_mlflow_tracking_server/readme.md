<!-- ###################################################################### -->
<!-- ###################################################################### -->
# Introduction
* The aim of the game here is to deploy an MLFlow Tracking Server on Heroku
* This server will track the different versions of our models
* Some data (train data and the artifacts) will be hosted on an AWS S3 disk
* Other data (metrics of the models) will be stored in a PostgreSQL database, also hosted on Heroku




<!-- ###################################################################### -->
<!-- ###################################################################### -->
# AWS

We will create a bucket, 2 directories, and a user who will have permissions on them.
* The first directory `data` will contain the training data.
* The second directory `artifacts` will receive the artifacts from the training of our various models.

## Create a Bucket on AWS S3

<p align="center">
<img src="./assets/img01.png" alt="drawing" width="600"/>
<p>

<p align="center">
<img src="./assets/img02.png" alt="drawing" width="600"/>
<p>

## Create 2 Directories in the Bucket

* In `data`, we will read the data to train the model.
* In `artifacts`, we will store the artifacts (images, parameters, etc.) during training.

<p align="center">
<img src="./assets/img03.png" alt="drawing" width="600"/>
<p>

<p align="center">
<img src="./assets/img04.png" alt="drawing" width="600"/>
<p>

* Copy and save the 2 URIs.

## Create a User on AWS IAM with S3 Full Access Rights

<p align="center">
<img src="./assets/img05.png" alt="drawing" width="600"/>
<p>

<p align="center">
<img src="./assets/img06.png" alt="drawing" width="600"/>
<p>

<p align="center">
<img src="./assets/img07.png" alt="drawing" width="600"/>
<p>

<p align="center">
<img src="./assets/img075.png" alt="drawing" width="600"/>
<p>

* Copy and save the access key ID and secret key in `./secrets.ps1`
* So far `./secrets.ps1` looks like : 

```
# fraud-detection-2-user full access S3
$env:AWS_REGION             = "eu-west-3"
$env:AWS_ACCESS_KEY_ID      = "AKI..."
$env:AWS_SECRET_ACCESS_KEY  = "vtL..."

```

<!-- ###################################################################### -->
<!-- ###################################################################### -->
# Dockerfile

Read the content of the `Dockerfile` located next to this `README.md`.


# Deploy an MLflow Tracking Server on Heroku

We will run an MLflow tracking server on Heroku.
* This server will use a PostgreSQL database (also on Heroku) to store the parameters and tags of each training session.
* If needed, it will fetch the training artifacts from the AWS S3 directory we just created.

To deploy the MLflow tracking server:
<!-- * Make sure **Docker is up and running** -->
* Open a terminal
    <!-- * `heroku login`
    * `heroku create fraud-202406`   
    * `heroku container:login` 
    * `heroku container:push web -a fraud-202406` 
    * `heroku container:release web -a fraud-202406`  
    -->
    * make sure you are at the root of the project directory

    ```
    heroku login
    heroku create fraud-detection-2
    ```
    * Note that these 2 urls have been created 
        * https://fraud-detection-2-ab95815c7127.herokuapp.com/ 
        * https://git.heroku.com/fraud-detection-2.git
        * are created for example
    <!-- * ~~git remote add heroku https://git.heroku.com/fraud-detection-2.git~~ -->

    ```
    git subtree push --prefix 00_mlflow_tracking_server heroku main
    ```

* At the start of the `git subtree push`

<p align="center">
<img src="./assets/img08.png" alt="drawing" width="600"/>
<p>

* At the end of the `git subtree push`
<p align="center">
<img src="./assets/img085.png" alt="drawing" width="600"/>
<p>

<!-- 


    * git push heroku main
    * heroku config:set FLASK_ENV=production
    * heroku config:set FLASHCARDS_SECRET_KEY=blablabla 
    * heroku open
    * This should work

 -->


<!-- ###################################################################### -->
<!-- ###################################################################### -->
# SQL Database for the MLflow Tracking Server

On the web page of the app `fraud-detection-2` (on Heroku):

* Click on Resources.
* Add an add-on.
* Search for Heroku Postgres.
* Agree to being charged.
* Wait...

<p align="center">
<img src="./assets/img09.png" alt="drawing" width="600"/>
<p>

* Click on Heroku Postgres.
* In the page that opens...
* Click on Settings.

<p align="center">
<img src="./assets/img10.png" alt="drawing" width="600"/>
<p>

* View credentials.
* Copy the URI link.
* Add "ql" to "postgres://…"
* Save it into the ``./secrets.ps1``

```
# fraud-detection-2-user full access S3
$env:AWS_REGION             = "eu-west-3"
$env:AWS_ACCESS_KEY_ID      = "AKI..."
$env:AWS_SECRET_ACCESS_KEY  = "vtL..."
# SQL sur Heroku
$env:BACKEND_STORE_URI      = "postgresql://uav..."

```


Return to the `settings` section of the app `fraud-detection-2`.

<p align="center">
<img src="./assets/img115.png" alt="drawing" width="600"/>
<p>

* Click on `Reveal Config Vars` 

<p align="center">
<img src="./assets/img125.png" alt="drawing" width="600"/>
<p>

* You could click ``Add`` and enter the various keys you saved in ``./secrets.ps1``
* Instead, go to the terminal and use the following commands

```
heroku config:set AWS_ACCESS_KEY_ID=AKI...
heroku config:set AWS_SECRET_ACCESS_KEY=vtL...
heroku config:set BACKEND_STORE_URI=postgresql://uav...

```
* Go back to `fraud-detection-2` web page on Heroku. You should see :

<p align="center">
<img src="./assets/img126.png" alt="drawing" width="600"/>
<p>

Return to the page of the app `fraud-202406`.

* Launch the app.
* There’s nothing there, but at least it displays.

<p align="center">
<img src="./assets/img13.png" alt="drawing" width="600"/>
<p>


<!-- ###################################################################### -->
<!-- ###################################################################### -->
# Testing

## Procfile
* In the ``00_mlflow_tracking_server`` create a file named `Procfile`
* Add this line and save the file

```
web: mlflow server --host 0.0.0.0 --port $PORT --backend-store-uri $BACKEND_STORE_URI --default-artifact-root $ARTIFACT_ROOT
```

* In the terminal, make sure you are at the root of the `fraud-detection-2`
* Push the subtree on Heroku

```
git subtree push --prefix 00_mlflow_tracking_server heroku main

```

Go to the directory `\02_train_code\01_sklearn\01_minimal` to read the `README.md` file.
