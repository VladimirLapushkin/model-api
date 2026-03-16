from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    transaction_id: float = Field(..., description="Transaction ID")
    customer_id: float = Field(..., description="Customer ID")
    terminal_id: float = Field(..., description="Terminal ID")
    tx_amount: float = Field(..., description="Transaction amount")
    tx_time_seconds: float = Field(..., description="Time in seconds")
    tx_time_days: float = Field(..., description="Time in days")
    tx_fraud_scenario: float = Field(..., description="Fraud scenario ID")

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": 1,
                "customer_id": 1001,
                "terminal_id": 501,
                "tx_amount": 150.50,
                "tx_time_seconds": 123456.78,
                "tx_time_days": 45.67,
                "tx_fraud_scenario": 1
            }
        }

    @staticmethod
    def spark_schema():
        from pyspark.sql.types import StructType, StructField, DoubleType

        return StructType([
            StructField("tranaction_id", DoubleType(), True),
            StructField("customer_id", DoubleType(), True),
            StructField("terminal_id", DoubleType(), True),
            StructField("tx_amount", DoubleType(), True),
            StructField("tx_time_seconds", DoubleType(), True),
            StructField("tx_time_days", DoubleType(), True),
            StructField("tx_fraud_scenario", DoubleType(), True),
        ])


class PredictResponse(BaseModel):
    prediction: float = Field(..., description="Fraud prediction (0/1)")
    probability: float = Field(..., description="Probability of fraud")
