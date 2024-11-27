############# POUR LANCER LE CONTENEUR DU CONSUMER.PY ##################################

. "./secrets.ps1"

docker run -it `
-v "$(pwd):/home/app" `
-e BDD_URI=$env:BDD_URI `
-e AWS_ACCESS_KEY_ID=$env:AWS_ACCESS_KEY_ID `
-e AWS_SECRET_ACCESS_KEY=$env:AWS_SECRET_ACCESS_KEY `
-e ARTIFACT_STORE_URI=$env:ARTIFACT_STORE_URI `
consumer-image bash