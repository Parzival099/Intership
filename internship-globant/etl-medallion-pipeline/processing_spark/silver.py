# silver.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, round

def main():
    spark = SparkSession.builder \
        .appName("ETL_to_Silver") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    print("✅ Sesión de Spark para Plata iniciada.")

    try:
        bronze_path = "/home/jovyan/work/bronze/online_retail"
        df_bronze = spark.read.parquet(bronze_path)
        print("📖 Leyendo desde la Capa Bronce...")
        
        df_silver = df_bronze.filter(col("CustomerID").isNotNull()).filter(col("Quantity") > 0).filter(col("UnitPrice") > 0) \
            .withColumn("TotalSales", round(col("Quantity") * col("UnitPrice"), 2)) \
            .withColumn("Año", year(col("InvoiceDate"))) \
            .withColumn("Mes", month(col("InvoiceDate"))) \
            .select("Año", "Mes", "Country", col("CustomerID").alias("CustomerId"), "UnitPrice", "Quantity", "TotalSales")
        
        silver_path = "/home/jovyan/work/silver/online_sales"
        print(f"💾 Guardando datos en la Capa Plata: {silver_path}")
        df_silver.write.format("delta").mode("overwrite").save(silver_path)
        
        print("🎉 Capa Plata creada exitosamente.")
    except Exception as e:
        print("❌ Ocurrió un error en el paso a Plata:", e)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()