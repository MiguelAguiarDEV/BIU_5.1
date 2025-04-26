from pyspark.sql import SparkSession

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

    spark.stop()

if __name__ == "__main__":
    main()
