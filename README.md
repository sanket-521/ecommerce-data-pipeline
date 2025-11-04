# 🧱 End-to-End Data Engineering Project: E-Commerce Sales Data Pipeline

## 📖 Overview
This project demonstrates an **end-to-end data engineering pipeline** using **AWS Glue (PySpark)**, **Databricks**, and **Power BI**.  
It processes e-commerce sales data from raw files in S3 to analytics-ready fact and dimension tables using a **Star Schema**.

---

## 🧩 Architecture
![Architecture](screenshots/architecture_diagram.png)

---

## ⚙️ Tech Stack
- **AWS S3** – Data Lake Storage  
- **AWS Glue (PySpark)** – ETL & Data Cleaning  
- **Databricks** – Data Modeling & Analytics  
- **Power BI** – Visualization  
- **Python, SQL, PySpark** – Programming  

---

## 📊 Data Pipeline Flow

| Stage | Description | Output |
|--------|--------------|--------|
| Raw | Raw CSV from source | `s3://.../raw/` |
| Staging | Cleaned with PySpark (Glue) | `s3://.../staging/` |
| Curated | Incrementally updated | `s3://.../curated/` |
| Warehouse | Star schema: Fact & Dimensions | `s3://.../warehouse/` |
| Analytics | Aggregated KPIs | `s3://.../analytics/` |

---

## 🧱 Data Model (Star Schema)

**Fact Table:** `fact_sales`  
**Dimension Tables:** `dim_customer`, `dim_product`, `dim_region`, `dim_date`

![Schema](docs/schema_design.png)

---

## 🔁 Incremental ETL Logic
```python
max_date = existing_df.select(spark_max("Order_Date")).collect()[0][0]
df_incremental = df_new.filter(col("Order_Date") > max_date)
df_incremental.write.mode("append").parquet(curated_path)
