"""
Algoritmo de Euclides para el cálculo del Máximo Común Divisor (MCD)

Usos:
- Simplificar fracciones.
- Criptografía (RSA y otros algoritmos basados en teoría de números).
- Resolución de problemas de divisibilidad y teoría de números en general.

Descripción (notación Euclid):
  Para a = 1193, b = 661:
    1193 = 1·661 + 532
     661 = 1·532 + 129
     532 = 4·129 + 16
     129 = 8·16  + 1
      16 = 16·1  + 0
  ⇒ gcd(1193, 661) = 1

Implementación distribuida con PySpark:
- Creamos un RDD de pares (a, b).
- Aplicamos la función gcd a cada par en paralelo.
"""

from pyspark.sql import SparkSession

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("euclid") \
        .master("local[*]") \
        .getOrCreate()
    sc = spark.sparkContext
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Ejemplo de pares a procesar
    pairs = [(1193, 661), (3408, 824291), (1193, 3408)]
    rdd = sc.parallelize(pairs)

    # Calcula el MCD de cada par
    result = rdd.map(lambda pair: ((pair[0], pair[1]), gcd(pair[0], pair[1])))

    # Imprime resultados
    for (a, b), g in result.collect():
        print(f"gcd({a}, {b}) = {g}")

    spark.stop()