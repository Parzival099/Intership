# ETL Pipeline with PySpark, Airflow, and Medallion Architecture

This repository contains the source code for an end-to-end, containerized ETL pipeline developed as an internship project. The pipeline extracts data from a legacy MySQL database, processes it through a multi-layered data lakehouse, and is fully orchestrated by Apache Airflow.

## 1. Overall Architecture Diagram

This diagram illustrates the complete data flow, from the source database to the final Gold layer, orchestrated by Airflow.
```
+----------------+      +--------------------+      +-----------------------+
|                |      |                    |      |                       |
| MySQL (Source) |-(1)->|  Airflow (Brain)   |-(2)->|   PySpark (Engine)    |
|  (Container)   |      |   (Container)      |      |     (Container)       |
|                |      |                    |      |                       |
+----------------+      +--------------------+      +-----------+-----------+
                                                                | (3)
                                                                |
                                             +------------------v-------------------+
                                             |        Data Lake (Medallion)        |
                                             |                                     |
                                             |  Bronze   ->   Silver   ->   Gold   |
                                             | (Parquet)    (Delta)      (Delta)  |
                                             +-------------------------------------+
```
* **(1) Trigger:** Airflow initiates the pipeline on a schedule or manually.
* **(2) Execution:** Airflow commands the PySpark container to execute the ETL scripts.
* **(3) Process:** PySpark reads from MySQL and processes the data through the Bronze, Silver, and Gold layers.

## 2. Technology Stack
* **Containerization:** Docker & Docker Compose
* **Orchestration:** Apache Airflow
* **Data Processing:** Apache Spark (PySpark)
* **Data Source:** MySQL
* **Storage Formats:** Parquet (Bronze Layer), Delta Lake (Silver & Gold Layers)

---
## 3. ETL Workflow & Code Highlights

The pipeline is structured following the Medallion architecture, ensuring data quality and traceability.

### 3.1. Bronze Layer: Raw Ingestion
The objective is to create a 1:1, raw copy of the source table. The `bronze.py` script connects to MySQL via JDBC, reads the entire table, and writes it without modification into the Bronze layer as a Parquet file.

* **Code Highlight (`bronze.py`):**
    ```python
    query = "(SELECT * FROM `online retail (3)`) AS t"
    df_bronze = spark.read.jdbc(url=db_url, table=query, properties=db_properties)
    df_bronze.write.mode("overwrite").parquet("bronze/online_retail")
    ```

### 3.2. Silver Layer: Cleansing & Enrichment
The objective is to clean and enrich the raw data into a trustworthy dataset. The `silver.py` script filters invalid records, calculates new columns like `TotalSales`, and standardizes the schema before saving the result as a Delta table.

* **Code Highlight (`silver.py`):**
    ```python
    from pyspark.sql.functions import col, year, round

    df_bronze = spark.read.parquet("bronze/online_retail")
    
    df_silver = df_bronze.filter(col("CustomerID").isNotNull()) \
        .filter(col("Quantity") > 0) \
        .withColumn("TotalSales", round(col("Quantity") * col("UnitPrice"), 2)) \
        .withColumn("Año", year(col("InvoiceDate")))
    
    df_silver.write.format("delta").mode("overwrite").save("silver/online_sales")
    ```

### 3.3. Gold Layer: Business Aggregation
The objective is to create pre-aggregated, business-ready tables. The `gold.py` script reads from the clean Silver layer, performs `groupBy` and `agg` operations, and saves the final analytical tables to the Gold layer.

* **Code Highlight (`gold.py`):**
    ```python
    from pyspark.sql.functions import sum as spark_sum

    df_silver = spark.read.format("delta").load("silver/online_sales")

    df_sales_by_country = df_silver.groupBy("Country") \
        .agg(round(spark_sum("TotalSales"), 2).alias("TotalVentas"))

    df_sales_by_country.write.format("delta").mode("overwrite").save("gold/sales_by_country")
    ```

---
## 4. Orchestration with Apache Airflow
The entire pipeline is automated using an Airflow DAG. The DAG ensures sequential execution and uses a `BashOperator` to trigger the PySpark scripts inside the dedicated Spark container, decoupling the orchestration layer from the execution layer.

* **DAG Structure:**
    ```
    [run_bronze_layer] >> [run_silver_layer] >> [run_gold_layer]
    ```

* **Code Highlight (`etl_medallion_dag.py`):**
    ```python
    from airflow.operators.bash import BashOperator

    docker_exec_command = "docker exec jupyter_spark_lab spark-submit /home/jovyan/work/"

    run_bronze = BashOperator(
        task_id='run_bronze_layer',
        bash_command=f"{docker_exec_command}bronze.py",
    )
    # ... (similar tasks for silver and gold) ...

    run_bronze >> run_silver >> run_gold
    ```
    
---
## 5. Key Learnings & Challenges Solved
* Successfully configured a multi-container Docker environment for a full ETL pipeline.
* Implemented the Medallion architecture to ensure data quality and allow for reprocessing.
* Automated a multi-step pipeline using Apache Airflow, managing dependencies between Spark jobs.
* Solved complex environment and networking issues, including JDBC/Delta driver loading (`ClassNotFoundException`), inter-container communication, and database permissioning.
