init:
	terraform init -upgrade

plan:
	terraform plan

apply:
	terraform apply -auto-approve

destroy:
	terraform destroy -auto-approve

kubeconf:
	rm ~/.kube/config
	yc managed-kubernetes cluster get-credentials mlops-k8s --external
	cat ~/.kube/config | base64 -w 0 >./config