# OTUS. Инференс на потоке

терраформ создаёт kubernates кластер с необходимыми правами
предварительно: созать yc container registry командой
yc container registry create --name fraud-registry
Github Action  разворачивает в облачном кластере Kubernates приложение с api модели. Реалтзовано 2 ручки: health и predict. Приложение берёт модель из внешнего s3 backet
Для запуска необходимо в Github создать следующие Repository secrets:
YC_CLEAN_BUCKET_AK   - auth key для бакета с моделью
YC_CLEAN_BUCKET_SK   - sekret key для бакета с моделью
YC_K8S_CLUSTER_ID  - ID k8s кластера (yc managed-kubernetes cluster list)
YC_REGISTRY_ID       - id yc registry для рпазмещения образов Docker
YC_SA_JSON_CREDENTIALS - креды для SA
Для локального запуска необходим файл .env c параметрами, собирать образ из файла Dockerfile-local
После выполнения Github Action

kubectl get svc -A
kubectl get svc

curl http://<balancer EXTERNAL-IP>:8081/health

curl -X POST "http://<balancer EXTERNAL-IP >/predict"   -H "Content-Type: application/json"   -d '{
    "transaction_id": 1,
    "customer_id": 1001,
    "terminal_id": 501,
    "tx_amount": 250.75,
    "tx_time_seconds": 36000,
    "tx_time_days": 12,
    "tx_fraud_scenario": 0
  }'


![alt text](screen/screenshot_20260303_184837.jpeg)
![alt text](screen/screenshot_20260303_184900.jpeg)
![alt text](screen/screenshot_20260303_192452.jpeg)
![alt text](screen/screenshot_20260303_192720.jpeg)
![alt text](screen/screenshot_20260303_195801.jpeg)
![alt text](screen/screenshot_20260303_195950.jpeg)
![alt text](screen/screenshot_20260303_200632.jpeg)
![alt text](screen/screenshot_20260303_202058.jpeg)
![alt text](screen/screenshot_20260303_202207.jpeg)
![alt text](screen/screenshot_20260303_202401.jpeg)
![alt text](screen/screenshot_20260303_202441.jpeg)
