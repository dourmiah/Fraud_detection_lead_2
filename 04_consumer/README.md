<!-- 
* j'ai besoin de faire ma propre image Docker qui permet d'exécuter du code qui utilise des topics 
* J'arrive pas à utiliser celle de Jedha
* Comme le docker file de l'image de Jedha est pas dispo (merci les gars)
* Je repars de 0 et j'essaie de découvrir les lib à installer


```bash
conda install requests pandas librdkafka -c conda-forge -y
pip install confluent_kafka  avro-python3
```


```bash
pip list --format=freeze >> ./requirements.txt
```



docker-compose up 
On voir Hello à l'écran


docker-compose up -d
docker-compose logs app1
Pour voir Hello dans les logs


docker-compose logs app1
docker-compose logs app1

docker-compose ps

docker-compose down
docker-compose stop
docker-compose stop app1


 -->




<!-- ###################################################################### -->
<!-- ###################################################################### -->

# ******************  Still under major construction ******************

# Consumer 

Make sure you read the [producer](../03_producer/README.md) readme file first.




<!-- ###################################################################### -->
<!-- ###################################################################### -->
# Introduction

This document covers :
1. Create our own Docker image to run Pyton scripts that can read ``topic_1``
1. Testing a first version of a consumer for the `fraud_detection_2` application

<!-- 1. Add to the Docker image what is needed to make inferences
1. Technical: Implementation of a Kafka Topic in `fraud_detection_2`. -->



<!-- ###################################################################### -->
<!-- ###################################################################### -->
# Create our own Docker image to run Pyton scripts that can read ``topic_1``

After running a first version of the producer in the `jedha/confluent-image` image, rather than launching the `test_producer02.py` application from the Linux prompt I tried, without success, to automate its launch.

After several attempts, the decision was made to create a Docker image using the following method:
1. Creating a minimal conda virtual environment using only Python 3.12
1. Create a directory and copy the files needed to run `test_producer02.py` (``secrets.ps1``, ``client.properties``...)
1. Add modules required for Python code to read or write to ``topic_1``.
1. Organize directories to separate what is needed to create the image from the script code.
1. Anticipate the use of ``docker-compose``. Eventually, we'll be launching from a single ``docker-compose.yml`` :
    1. the producer writing to ``topic_1``, and
    1. The consumer, which reads from ``topic_1``, requests predictions from the model tracked by the MLflow Tracking Server and writes the results to ``topic_2``. The records in ``topic_2`` have the same format as those in topic_1.
    1. the script (as yet unnamed) that reads from `topic_2` and saves the inferences in a PostgreSQL database, remembering to add a ``fraud_confirmed`` column.

## Organization of subdirectories

Finally (remember CeCe Peniston, 1991 ?), the directories are organized as follows:

```
./
│   build_img.ps1
│   docker-compose.yml
│   run_app.ps1
│
├───app
│       ccloud_lib.py
│       client.properties
│       secrets.ps1
│       test_producer02.py
│
└───docker
        Dockerfile
        requirements.txt
```
* `build_img.ps1` = a script to create the image
* ``docker-compose.yml`` = application launch orchestration
* `run_app.ps1` = launches the application. Sets passwords, then invokes ``docker-compose.yml``.
* `./app` = the directory containing the consumer script. Contains `secrets.ps1` with passwords and other necessary files.
* ``./docker`` = the directory with the `Dockerfile` and `requirements.txt` files needed to create our home image.

Take the time to study the contents of the directories and files. One annoying thing is that a `librdkafka` library is required, but it has to be installed via an `apt-get` (see the content of `Dockerfile`).

To build the `my_confluent_img` image :

```
./build_img.ps1

```

We can see that, at this stage, the new image (`my_confluent_img`) is much lighter than the previous one (`custom-confluent-image`):

<p align="center">
<img src="./assets/img01.png" alt="drawing" width="600"/>
<p>









<!-- ###################################################################### -->
<!-- ###################################################################### -->
# Testing a first version of a consumer for the `fraud_detection_2` application

Run the consumer with the following command :

```
./run_app.ps1

```

Via the `run_app.ps1`, the consumer in launched in **detached mode**. This is why we don't see anything in the console. We must use docker-compose command to 
* list the running process (``docker-compose ps``)
* inspect the logs (`docker-compose logs consumer`) 
* gently close the app (`docker-compose down consumer`)

<p align="center">
<img src="./assets/img02.png" alt="drawing" width="600"/>
<p>

The reason we can read messages from ``topic_1`` is simply because we previously used the ``test_producer02.py`` to send them there. In fact, ``topic_1`` serves as a backlog for 7 days.


<p align="center">
<img src="./assets/img03.png" alt="drawing" width="600"/>
<p>
































<!-- 
## Create a topic

* Connect to the [Confluent](https://confluent.cloud/home) 
* Select the `fraud_detection_2_clstr` cluster

<p align="center">
<img src="./assets/img01.png" alt="drawing" width="600"/>
<p>

* Add a topic
* Name it `topic_2`
* Do not add a contract

<p align="center">
<img src="./assets/img02.png" alt="drawing" width="300"/>
<p>

* Copy the `secrets.ps1` you used with the producer and paste it in the directory




# 4. Running the producer of the `fraud_detection_2` application

## Configure client application access

* This is a Python code that retrieves simulated bank transactions from the "Real-time Data producer" and deposits them in ``topic_1``. 
* It produces data insofar as it deposits them in the topic
* This code must have the credentials to access ``topic_1`` this is why we need to go back to the Confluent web page

<p align="center">
<img src="./assets/img065.png" alt="drawing" width="600"/>
<p>


* Return to the `fraud_detection_2_clstr` page then click on "Set up client"

<p align="center">
<img src="./assets/img07.png" alt="drawing" width="600"/>
<p>

* Choose a language
* If a form asks for the topic name, enter `topic_1`

<p align="center">
<img src="./assets/img08.png" alt="drawing" width="600"/>
<p>


<p align="center">
<img src="./assets/img09.png" alt="drawing" width="600"/>
<p>


* On the web page we are offered to save a `clients.properties` file that contains the ``Key`` and the ``Secret`` in clear text (or that we will have to enter later in clear text in the `clients.properties` file in question)
* **IMPORTANT**: Once the `clients.properties` file is saved in the project directory, edit it and delete the 2 lines below:

```
sasl.username=6KQ...
sasl.password=zBV...
```

* In fact, `$env:SASL_USERNAME` and `$env:SASL_PASSWORD` have already been saved in a `secrets.ps1` file.







## Testing the producer 

* To test the producer you must :
    1. Open a terminal in the
    1. Launch the Docker image in interactive mode using the `run_confluent_image.ps1` script.

```powershell
./run_confluent_image.ps1
```


<p align="center">
<img src="./assets/img10.png" alt="drawing" width="600"/>
<p>

* When the Linux prompt is on the screen, we launch the producer code itself

```bash
python test_producer02.py 
```

<p align="center">
<img src="./assets/img11.png" alt="drawing" width="600"/>
<p>

* Given the speed of the ``Real-time Data producer``, the code displays transactions every 15 seconds.
* To stop the code, press ``CTRL+C`` in the Linux console. 
* To return to PowerShell, type `exit` at the Linux prompt.


## It's a kind of magic...
The aim here is to explain how the producer starts up and how the Confluent API's ``Key'' and ``Secret'' pass from PowerShell to Linux.

### The `run_confluent_image.ps1` script

```powershell
. "./secrets.ps1"
docker run -it -v "$(pwd):/home/app" -e SASL_USERNAME="$env:SASL_USERNAME" -e SASL_PASSWORD="$env:SASL_PASSWORD" jedha/confluent-image bash

```

* The script begins by checking that the `secrets.ps1` script is running.
* On the Windows side, it's the execution of the `secrets.ps1` script that defines the 2 environment variables `$env:SASL_USERNAME` and `$env:SASL_PASSWORD`.
* Once these two variables are in place, the ``run_confluent_image.ps1`` script passes them on to the Docker image (via the command line).
* Once launched, the Docker image can access a volume pointing to the current directory, and remains in interactive mode with a ``bash`` prompt.


### The `read_ccloud_config()` function in the `ccloud_lib` file. 

For the `fraud_detection_2` project, this function has been modified to :
1. Read the ``client.properties`` file 
1. retrieve the contents of environment variables ``SASL_USERNAME`` and ``SASL_PASSWORD``.

```python
def read_ccloud_config(config_file: str) -> dict:
    """Read Confluent Cloud configuration for librdkafka clients""""

    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split("=", 1)
                conf[parameter] = value.strip()

    sasl_username = os.getenv("SASL_USERNAME")
    sasl_password = os.getenv("SASL_PASSWORD")

    # Check if environment var are defined
    if not sasl_username or not sasl_password:
        raise EnvironmentError(
            "The SASL_USERNAME or SASL_PASSWORD environment variables are not defined."
        )

    # Get credentials from environment variables
    conf["sasl.username"] = sasl_username
    conf["sasl.password"] = sasl_password

    # conf['ssl.ca.location'] = certifi.where()

    return conf
```

### The producer code ``test_producerXY.py`` 

See the definition of "constants" below at the very beginning of the code.   

```python
k_Topic = "topic_1"
k_Client_Prop = "client.properties"
k_RT_Data_Producer = "https://real-time-payments-api.herokuapp.com/current-transactions"
``` -->


<!-- ###################################################################### -->
<!-- ###################################################################### -->
# What's next ?
<!-- Go to the directory `03_consumer` and read the `README.md` file.  -->