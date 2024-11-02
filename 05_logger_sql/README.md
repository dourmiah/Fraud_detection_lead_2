<!-- ###################################################################### -->
<!-- ###################################################################### -->

# *****  Still under construction *****


# Logger_SQL 

```powershell
conda create --name logger_sql python=3.12 -y
conda activate logger_sql
conda install pandas  -c conda-forge -y

heroku login
heroku create logger-sql 
heroku addons:create heroku-postgresql:essential-0 --app logger-sql
```


Sur heroku.com sur la page de l'application
<p align="center">
<img src="./assets/img01.png" alt="drawing" width="600"/>
<p>

Cliquer sur Heroku PostgreSQL

<p align="center">
<img src="./assets/img02.png" alt="drawing" width="600"/>
<p>

lick on Settings 
View credentials.
<p align="center">
<img src="./assets/img03.png" alt="drawing" width="600"/>
<p>

Copy the URI link : postgres://ucn...
Add "ql" to "postgres://…"  => postgresql://ucn...
Save it into the ./secrets.ps1

```powershell
$env:LOGGER_SQL_URI = "postgresql://ucn..."
```


```powershell
conda install psycopg2-binary -c conda-forge -y
conda install sqlalchemy -c conda-forge -y
```

<p align="center">
<img src="./assets/img04.png" alt="drawing" width="600"/>
<p>

<p align="center">
<img src="./assets/img05.png" alt="drawing" width="600"/>
<p>

<p align="center">
<img src="./assets/img06.png" alt="drawing" width="600"/>
<p>

