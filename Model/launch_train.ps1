. "./secrets.ps1"

docker run -it `
-v "$(pwd):/home/app" `
-e APP_URI=$env:APP_URI `
-e AWS_ACCESS_KEY_ID=$env:AWS_ACCESS_KEY_ID `
-e AWS_SECRET_ACCESS_KEY=$env:AWS_SECRET_ACCESS_KEY `
sklearn_fraud_trainer bash

