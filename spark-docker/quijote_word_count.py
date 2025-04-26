import re
import sys
from pyspark.sql import SparkSession

def main(target):
    spark = SparkSession.builder \
        .appName("quijote_count_word") \
        .master("local[*]") \
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Leer el texto y extraer palabras en minúsculas
    lines = sc.textFile("data/quijote.txt")
    words = lines.flatMap(lambda line: re.findall(r"[A-Za-zÀ-ÿ]+", line.lower()))

    # Contar ocurrencias de la palabra objetivo
    count = words.filter(lambda w: w == target.lower()).count()

    print(f"La palabra '{target}' aparece {count} veces en El Quijote.")

    spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: spark-submit quijote_count.py <palabra>")
        sys.exit(1)
    TARGET = sys.argv[1]
    main(TARGET)