# gold.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, round

def main():
    spark = SparkSession.builder \
        .appName("ETL_to_Gold") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    print("✅ Sesión de Spark para Oro iniciada.")

    try:
        silver_path = "/home/jovyan/work/silver/online_sales"
        df_silver = spark.read.format("delta").load(silver_path)
        print("📖 Leyendo desde la Capa Plata...")
        
        df_sales_by_country = df_silver.groupBy("Country") \
            .agg(round(spark_sum("TotalSales"), 2).alias("TotalVentas")) \
            .orderBy(col("TotalVentas").desc())
            
        gold_path = "/home/jovyan/work/gold/sales_by_country"
        print(f"💾 Guardando datos en la Capa Oro: {gold_path}")
        df_sales_by_country.write.format("delta").mode("overwrite").save(gold_path)
        
        print("🎉 Capa Oro 'Ventas por País' creada exitosamente.")
    except Exception as e:
        print("❌ Ocurrió un error en el paso a Oro:", e)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()