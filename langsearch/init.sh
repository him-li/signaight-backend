apt-get update && sudo apt-get install google-cloud-cli
gcloud config set project ${GOOGLE_PROJECT_ID}
gcloud services enable ${GOOGLE_SERVICE_API} 