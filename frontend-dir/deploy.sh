#!/bin/bash

docker build -t us-docker.pkg.dev/articulate-life-393421/flashcardapp/flashcardfrontend .

docker push us-docker.pkg.dev/articulate-life-393421/flashcardapp/flashcardfrontend

gcloud run deploy flashcardapp-fe \
  --image us-docker.pkg.dev/articulate-life-393421/flashcardapp/flashcardfrontend \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory=4Gi \
  --cpu=8 \
  --timeout=300s \
  --concurrency=300 \
  --max-instances=12 \
  --set-env-vars=NODE_ENV=production


