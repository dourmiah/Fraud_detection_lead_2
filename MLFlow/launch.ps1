. "./secrets.ps1"

# Local
# docker run -it -p 4000:4000 `
# -v "$(pwd):/home/app" `
# -e PORT=4000 `
# -e AWS_ACCESS_KEY_ID="AKIAZQ3DP4A2FZJWQ6A2" `
# -e AWS_SECRET_ACCESS_KEY="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" `
# -e BACKEND_STORE_URI="postgresql://u55kao1h651rg1:p2bec0f5c95b3bfca2b3ccf2413c5aa108961f5b13b6d10bd1ba46bf139fc42a8@cbdhrtd93854d5.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dg2qj03o22oh8" `
# -e ARTIFACT_STORE_URI="s3://dom-jedha-bucket/artefacts/" `
# sklearn_fraud_trainer

# Remote
docker run -it -p 4000:4000 `
-v "$(pwd):/home/app" `
-e PORT=4000 `
-e APP_URI=$env:APP_URI `
-e AWS_ACCESS_KEY_ID=$env:AWS_ACCESS_KEY_ID `
-e AWS_SECRET_ACCESS_KEY=$env:AWS_SECRET_ACCESS_KEY `
sklearn_fraud_trainer python train.py