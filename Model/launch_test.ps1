. "./secrets.ps1"

docker run -it `
-v "$(pwd):/home/app" `
-e APP_URI=$env:APP_URI `
tests-image bash