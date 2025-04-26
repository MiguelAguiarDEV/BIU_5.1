from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col

if __name__ == "__main__":
    # Iniciar Spark
    spark = SparkSession.builder \
        .appName("mapreduce_copenhagen") \
        .master("local[*]") \
        .getOrCreate()
    # Silenciar logs INFO/WARN
    spark.sparkContext.setLogLevel("ERROR")

    # Leer copenhagen.csv (encabezado 'city_name,datetime,temperature_avg')
    df = spark.read.option("header", True).csv("data/copenhagen.csv")

    # Convertir 'temperature_avg' a float
    df = df.withColumn("temperature_avg", col("temperature_avg").cast("float"))

    # Definir umbrales
    HOT_THRESHOLD = 25.0
    COLD_THRESHOLD = 5.0

    # Clasificar en hot, cold o neutral según 'temperature_avg'
    df2 = df.withColumn("category",
                       when(col("temperature_avg") >= HOT_THRESHOLD, "hot")
                       .when(col("temperature_avg") <= COLD_THRESHOLD, "cold")
                       .otherwise("neutral"))

    # Contar ocurrencias por categoría
    result = df2.groupBy("category").count()

    # Mostrar resultados
    print("=== Clasificación de temperaturas ===")
    result.orderBy("category").show(truncate=False)

    spark.stop()
