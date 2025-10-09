# bronze.py
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder.appName("ETL_to_Bronze").getOrCreate()
    print("✅ Sesión de Spark para Bronce iniciada.")

    db_url = "jdbc:mysql://mysql-db:3306/importar"
    db_properties = {
        "user": "root",
        "password": "tu_password_root",
        "driver": "com.mysql.cj.jdbc.Driver"
    }
    query = "(SELECT * FROM `online retail (3)`) AS t"

    try:
        print("📖 Leyendo desde MySQL...")
        df = spark.read.jdbc(url=db_url, table=query, properties=db_properties)
        
        bronze_path = "/home/jovyan/work/bronze/online_retail"
        print(f"💾 Guardando datos en la Capa Bronce: {bronze_path}")
        df.write.mode("overwrite").parquet(bronze_path)
        
        print("🎉 Capa Bronce creada exitosamente.")
    except Exception as e:
        print("❌ Ocurrió un error en el paso a Bronce:", e)
    finally:
        spark.stop()

if __name__ == "__main__":
    main()