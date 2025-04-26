from pyspark.sql import SparkSession

if __name__ == "__main__":
    # Iniciar Spark
    spark = SparkSession.builder \
        .appName("average_movie_mark") \
        .master("local[*]") \
        .getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")
    
    # Leer ratings: userID::movieID::rating::timestamp
    ratings = sc.textFile("data/ratings.txt")

    # Mapear a (movieID, rating)
    movie_ratings = ratings \
        .map(lambda line: line.split("::")) \
        .map(lambda fields: (fields[1], float(fields[2])))

    # Combinar para (sumRatings, count)
    sums_counts = movie_ratings.combineByKey(
        lambda rating: (rating, 1),
        lambda acc, rating: (acc[0] + rating, acc[1] + 1),
        lambda acc1, acc2: (acc1[0] + acc2[0], acc1[1] + acc2[1])
    )

    # Calcular promedio y filtrar > 3.0
    high_avg = sums_counts \
        .mapValues(lambda sc: sc[0] / sc[1]) \
        .filter(lambda x: x[1] > 3.0)

    # Mostrar resultados
    for movie, avg in high_avg.collect():
        print(f"{movie}\t{avg:.2f}")

    spark.stop()
