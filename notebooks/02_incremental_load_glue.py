from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max as spark_max
import boto3

spark = SparkSession.builder.appName("IncrementalLoad").getOrCreate()

staging_path = "s3://ecommerce-data-pipeline-sanket/staging/sales/"
curated_path = "s3://ecommerce-data-pipeline-sanket/curated/sales/"

# 1️⃣ Read the new cleaned data from staging
df_staging = spark.read.parquet(staging_path)

# 2️⃣ Try reading existing curated data
try:
    existing_df = spark.read.parquet(curated_path)
    print("✅ Curated data found. Performing incremental load...")

    # Get the max Order_Date
    max_date = existing_df.select(spark_max("Order_Date")).collect()[0][0]
    print(f"🕒 Last processed Order_Date: {max_date}")

    # Filter only new records
    df_incremental = df_staging.filter(col("Order_Date") > max_date)

    if df_incremental.count() > 0:
        df_incremental.write.mode("append").parquet(curated_path)
        print("✅ New records appended successfully!")
    else:
        print("⚠️ No new records to load.")

except Exception as e:
    # 3️⃣ If curated is empty, run full load (first time only)
    print("⚠️ No curated data found. Performing full load for the first time...")
    df_staging.write.mode("overwrite").parquet(curated_path)
    print("✅ Full load completed successfully!")
