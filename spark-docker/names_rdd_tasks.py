from pyspark.sql import SparkSession
import random

def main():
    cadena = "Juan, Jimena, Luis, Cristian, Laura, Lorena, Cristina, Jacobo, Jorge"
    # Quitar espacios y transformar en lista
    names = [name.strip() for name in cadena.split(",")]

    spark = SparkSession.builder.appName("names_rdd_tasks").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Crear RDD de nombres
    rdd = sc.parallelize(names)

    print("Lista de nombres:", rdd.collect())

    # 1. Agrupar por inicial
    grouped = rdd.groupBy(lambda name: name[0]) \
        .map(lambda x: (x[0], list(x[1]))) \
        .collect()
    print("Nombres agrupados por inicial:", grouped)

    # 2. Muestra de 5 elementos únicos
    muestra_unica = random.sample(names, 5)
    print("Muestra de 5 elementos únicos:", muestra_unica)

    # 3. Muestra de aproximadamente la mitad de registros (pueden repetirse)
    sample_size = len(names) // 2
    muestra_con_repetidos = random.choices(names, k=sample_size)
    print("Muestra de la mitad de registros (pueden repetirse):", muestra_con_repetidos)

    spark.stop()

if __name__ == "__main__":
    main()
