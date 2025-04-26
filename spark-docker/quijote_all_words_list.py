from pyspark.sql import SparkSession
import re

# 1) Iniciar Spark
spark = SparkSession.builder \
    .appName("quijote_listado_palabras") \
    .master("local[*]") \
    .getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("ERROR")

# 2) Leer el texto y extraer palabras (minúsculas, sin signos)
lines = sc.textFile("data/quijote.txt")
words_rdd = lines.flatMap(lambda line: re.findall(r"[A-Za-zÀ-ÿ]+", line.lower()))

# 3) Materializar en el driver como lista de Python
word_list = words_rdd.collect()

# 4) Mostrar cuántas palabras hay y las primeras 50 ejemplos
print("Lista de palabras:", word_list)
print("\n")
print("===============================================")
print("===============================================")
print(f"Total de palabras: {len(word_list)}")
print("Primeras 50 palabras:", word_list[:50])

spark.stop()
