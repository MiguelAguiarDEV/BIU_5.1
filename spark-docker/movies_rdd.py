from pyspark.sql import SparkSession
import re

def count_vowels(s: str) -> int:
    return len(re.findall(r'[aeiouAEIOU]', s))

if __name__ == "__main__":
    # Iniciar Spark
    spark = SparkSession.builder \
        .appName("movies_vowels_rdd") \
        .master("local[*]") \
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Leer CSV con header, inferir esquema para manejar comillas y comas en campos
    df = spark.read.option("header", True).option("inferSchema", True) \
        .csv("data/movies.csv")

    # Crear RDD de (Rank, Title)
    rdd = df.select("Rank", "Title").rdd.map(lambda row: (row["Rank"], row["Title"]))

    # Filtrar títulos con ≥4 vocales
    result = rdd.filter(lambda x: count_vowels(x[1]) >= 10)

    # Mostrar resultados
    for id_pelicula, titulo in result.collect():
        print(f"{id_pelicula}\t{titulo}")

    spark.stop()
