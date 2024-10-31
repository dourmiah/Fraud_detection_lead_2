* j'ai besoin de faire ma propre image Docker qui permet d'exécuter du code qui utilise des topics 
* J'arrive pas à utiliser celle de Jedha
* Comme le docker file de l'image de Jedha est pas dispo (merci les gars)
* Je repars de 0 et j'essaie de découvrir les lib à installer

F5
Exception
./secrets.ps1 dans la console de Debug
F5
Ca tourne


<!-- conda install pandas -c conda-forge -y
conda install requests
conda install librdkafka -c conda-forge -->


```bash
conda install requests pandas librdkafka -c conda-forge -y
pip install confluent_kafka  avro-python3
```


```bash
pip list --format=freeze >> ./requirements.txt
```
