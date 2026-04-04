apply:
	terraform apply -auto-approve

destroy:
	terraform destroy -auto-approve

.PHONY: monitoring
monitoring:
	kubectl apply -f config/servicemonitor-fraud-api.yaml
	kubectl apply -f config/prometheusrule-fraud-api.yaml
	kubectl apply -f config/alertmanager-config.yaml
	#kubectl apply -f config/dashboard-model-api-configmap.yaml
	#kubectl apply -f config/dashboard-model-api-scaling-configmap.yaml

.PHONY: app
app:
	kubectl apply -f config/deployment-fraud-api.yaml
	kubectl apply -f config/service-fraud-api.yaml

.PHONY: all
all: app monitoring