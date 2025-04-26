import re
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("quijote_wordcount_to_hdfs") \
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Leer el texto y extraer palabras en minúsculas
    lines = sc.textFile("data/quijote.txt")
    words = lines.flatMap(lambda line: re.findall(r"[A-Za-zÀ-ÿ]+", line.lower()))

    # MapReduce: (palabra, 1) y reduceByKey
    word_counts = words.map(lambda w: (w, 1)).reduceByKey(lambda a, b: a + b)

    # Ordenar por conteo descendente
    sorted_counts = word_counts.sortBy(lambda x: -x[1])

    # Guardar en HDFS
    sorted_counts.map(lambda x: f"{x[0]}\t{x[1]}").saveAsTextFile("hdfs://hadoop-namenode:9000/quijote_wordcount")

    spark.stop()

if __name__ == "__main__":
    main()
