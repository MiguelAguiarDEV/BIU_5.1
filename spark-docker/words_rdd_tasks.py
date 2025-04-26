from pyspark.sql import SparkSession

def main():
    english = ['hello', 'table', 'angel', 'cat', 'dog', 'animal', 'chocolate', 'dark', 'doctor', 'hospital', 'computer']
    spanish = ['hola', 'mesa', 'angel', 'gato', 'perro', 'animal', 'chocolate', 'oscuro', 'doctor', 'hospital', 'ordenador']

    spark = SparkSession.builder.appName("words_rdd_tasks").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Crear RDD de tuplas (ingles, español)
    rdd = sc.parallelize(zip(english, spanish))

    # Palabras que se escriben igual en inglés y español
    iguales = rdd.filter(lambda x: x[0] == x[1]).map(lambda x: x[0]).collect()
    print("Palabras que se escriben igual en ambos idiomas:", iguales)

    # Palabras que en español son distintas que en inglés
    distintas = rdd.filter(lambda x: x[0] != x[1]).map(lambda x: (x[0], x[1])).collect()
    print("Palabras distintas (pares inglés-español):", distintas)

    # Lista única con palabras distintas entre sí (solo las que no son iguales)
    distintas_unicas = rdd.filter(lambda x: x[0] != x[1]).flatMap(lambda x: [x[0], x[1]]).distinct().collect()
    print("Lista única de palabras distintas entre sí:", distintas_unicas)

    # Todas las palabras en ambos idiomas (sin repetir)
    all_words = sc.parallelize(english + spanish).distinct()

    # Grupo de palabras que empiezan por vocal
    vocales = all_words.filter(lambda w: w[0].lower() in 'aeiou').collect()
    print("Palabras que empiezan por vocal:", vocales)

    # Grupo de palabras que empiezan por consonante
    consonantes = all_words.filter(lambda w: w[0].lower() not in 'aeiou').collect()
    print("Palabras que empiezan por consonante:", consonantes)

    spark.stop()

if __name__ == "__main__":
    main()
