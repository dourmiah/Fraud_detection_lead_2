<!-- ###################################################################### -->
<!-- ###################################################################### -->
# Introduction
* The aim of the game here is to deploy an MLFlow Tracking Server on Heroku
* This server will help to track the different versions of our models
* Some data (train data and artefacts) will be hosted on an AWS S3 disk
* Other data will be hosted in a PostgreSQL database, also hosted on Heroku




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

* Copy and save the access key ID and secret key.


<!-- ###################################################################### -->
<!-- ###################################################################### -->
# Dockerfile

Read the content of the `Dockerfile` located next to this `README.md`.


# Deploy an MLflow Tracking Server on Heroku

We will run an MLflow tracking server on Heroku.
* This server will use a PostgreSQL database (also on Heroku) to store the parameters and tags of each training session.
* If needed, it will fetch the training artifacts from the AWS S3 directory we just created.

To deploy the MLflow tracking server:
* Ensure that Docker is running.
* Open a terminal.
    * `heroku login`
    * `heroku create fraud-202406`   
    * `heroku container:login` 
    * `heroku container:push web -a fraud-202406` 
    * `heroku container:release web -a fraud-202406` 

<p align="center">
<img src="./assets/img08.png" alt="drawing" width="600"/>
<p>


<!-- ###################################################################### -->
<!-- ###################################################################### -->
# SQL Database for the MLflow Tracking Server

On the web page of the app `fraud-202406` (on Heroku):

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
* Save it.

Return to the `settings` section of the app `fraud-202406`.

<p align="center">
<img src="./assets/img11.png" alt="drawing" width="600"/>
<p>

* Click on `Reveal Config Vars` and enter the various keys you saved.

<p align="center">
<img src="./assets/img12.png" alt="drawing" width="600"/>
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

Go to the directory `\02_train_code\01_sklearn\01_minimal` to read the `README.md` file.
