from app.schemas import PredictRequest


def create_spark(s3_endpoint: str, access_key: str, secret_key: str):
    from pyspark.sql import SparkSession

    endpoint = s3_endpoint.replace("https://", "").replace("http://", "")
    ssl_enabled = "true" if s3_endpoint.startswith("https://") else "false"

    spark = (
        SparkSession.builder
        .appName("FraudDetectionAPI")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262"
        )
        .config("spark.driver.memory", "2g")
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.hadoop.fs.s3a.endpoint", endpoint)
        .config("spark.hadoop.fs.s3a.endpoint.region", "ru-central1")
        .config("spark.hadoop.fs.s3a.access.key", access_key)
        .config("spark.hadoop.fs.s3a.secret.key", secret_key)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", ssl_enabled)
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
        )
        .getOrCreate()
    )

    return spark


def load_model(spark, model_path: str):
    from pyspark.ml import PipelineModel
    return PipelineModel.load(model_path)


def predict_one(spark, model, request: PredictRequest):
    df = spark.createDataFrame(
        [(
            float(request.transaction_id),
            float(request.customer_id),
            float(request.terminal_id),
            float(request.tx_amount),
            float(request.tx_time_seconds),
            float(request.tx_time_days),
            float(request.tx_fraud_scenario),
        )],
        schema=PredictRequest.spark_schema()
    )

    pred = model.transform(df).select("prediction", "probability").collect()[0]

    probability = (
        float(pred["probability"][1])
        if pred["probability"] is not None
        else float(pred["prediction"])
    )

    return {
        "prediction": float(pred["prediction"]),
        "probability": probability,
    }
