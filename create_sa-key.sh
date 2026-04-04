yc iam key create   --service-account-name admin   --output ./secrets/sa-key.json
cat ./secrets/sa-key.json | jq -c . > ./secrets/sa-key.json.compact
