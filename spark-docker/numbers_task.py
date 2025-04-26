from pyspark.sql import SparkSession

def main():
    numbers = [4,6,34,7,9,2,3,4,4,21,4,6,8,9,7,8,5,4,3,22,34,56,98]
    spark = SparkSession.builder.appName("numbers").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Crear RDD, eliminar duplicados y ordenar descendentemente
    rdd = sc.parallelize(numbers).distinct().sortBy(lambda x: -x)
    sample = rdd.take(5)

    print("Muestra de 5 elementos únicos y ordenados descendentemente:", sample)
    print("Elemento mayor de la muestra:", max(sample))
    print("Dos elementos menores de la muestra:", sorted(sample)[0:2])

    spark.stop()

if __name__ == "__main__":
    main()
