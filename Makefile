
git_secres:
	yc iam key create --service-account-name admin --output ./secrets/sa-key.json && \
	sed -i '/^YC_SA_JSON_CREDENTIALS=/d' .env && \
	jq -c . ./secrets/sa-key.json | sed "s/^/YC_SA_JSON_CREDENTIALS=/" >> .env

push_secrets:
	python3 ./utils/push_secrets_to_github_repo.py

kubeconf:
	rm ~/.kube/config
	yc managed-kubernetes cluster get-credentials mlops-k8s --external
	kubectl apply -f k8s/deployment.yaml

k8s_balancer_to_vars_airflow:
	BALANCER_IP=$$(kubectl get svc fraud-api -n default -o json | jq -r '.status.loadBalancer.ingress[0].ip'); \
	PARENT_ENV_FILE="$$(cd ../ml-anti-fraud-system/infra && pwd)/terraform.tfvars"; \
	sed -i '/^k8s_balancer_ip[[:space:]]*=/d' "$$PARENT_ENV_FILE"; \
	echo "k8s_balancer_ip = \"$$BALANCER_IP\"" >> "$$PARENT_ENV_FILE"


deploy_secrets: kubeconf git_secres push_secrets k8s_balancer_to_vars_airflow


