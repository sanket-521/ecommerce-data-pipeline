import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.job import Job
from pyspark.sql.functions import col, to_date, when

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read raw data
df = spark.read.option("header", "true").csv("s3://ecommerce-data-pipeline-sanket/raw/sales_data.csv")

# Clean and transform
df_clean = (df
    .withColumn("Order_Date", to_date(col("Order Date"), "MM/dd/yyyy"))
    .withColumn("Ship_Date", to_date(col("Ship Date"), "MM/dd/yyyy"))
    .withColumn("Sales", col("Sales").cast("double"))
    .withColumn("Profit", col("Profit").cast("double"))
    .dropna(subset=["Order ID", "Sales", "Profit"])
)

# Write to staging zone
df_clean.write.mode("overwrite").parquet("s3://ecommerce-data-pipeline-sanket/staging/sales/")
job.commit()
