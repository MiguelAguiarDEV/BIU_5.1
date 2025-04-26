from pyspark.sql import SparkSession

def parse_line(line):
    parts = line.strip().split(",")
    return (parts[0], float(parts[1]))

def main():
    spark = SparkSession.builder.appName("marks_rdd_tasks").getOrCreate()
    sc = spark.sparkContext
    sc.setLogLevel("ERROR")

    # Cargar datos
    matematicas = sc.textFile("data/notas_matematicas").map(parse_line)
    ingles = sc.textFile("data/notas_ingles").map(parse_line)
    fisica = sc.textFile("data/notas_fisica").map(parse_line)

    print("=== Notas de Matemáticas ===")
    for alumno, nota in matematicas.collect():
        print(f"{alumno}: {nota}")
    print("\n=== Notas de Inglés ===")
    for alumno, nota in ingles.collect():
        print(f"{alumno}: {nota}")
    print("\n=== Notas de Física ===")
    for alumno, nota in fisica.collect():
        print(f"{alumno}: {nota}")

    # 2. Un solo RDD con todas las notas (añadiendo asignatura)
    mat = matematicas.map(lambda x: (x[0], ("Matematicas", x[1])))
    ing = ingles.map(lambda x: (x[0], ("Inglés", x[1])))
    fis = fisica.map(lambda x: (x[0], ("Física", x[1])))
    todas = mat.union(ing).union(fis)
    print("\n=== Todas las notas (alumno, (asignatura, nota)) ===")
    for alumno, (asig, nota) in todas.collect():
        print(f"{alumno}: {asig} -> {nota}")

    # 3. Nota más baja por alumno
    notas_por_alumno = todas.groupByKey().mapValues(list)
    nota_minima = notas_por_alumno.mapValues(lambda notas: min([n[1] for n in notas]))
    print("\n=== Nota más baja por alumno ===")
    for alumno, nota in nota_minima.collect():
        print(f"{alumno}: {nota}")

    # 4. Nota media por alumno
    nota_media = notas_por_alumno.mapValues(lambda notas: sum([n[1] for n in notas]) / len(notas))
    print("\n=== Nota media por alumno ===")
    for alumno, media in nota_media.collect():
        print(f"{alumno}: {media:.2f}")

    # 5. ¿Cuántos estudiantes suspenden cada asignatura?
    susp_mat = matematicas.filter(lambda x: x[1] < 5).count()
    susp_fis = fisica.filter(lambda x: x[1] < 5).count()
    susp_ing = ingles.filter(lambda x: x[1] < 5).count()
    print("\n=== Suspensos por asignatura ===")
    print(f"Matemáticas: {susp_mat}")
    print(f"Física: {susp_fis}")
    print(f"Inglés: {susp_ing}")

    # 6. ¿En qué asignatura suspende más gente?
    suspensos = [("Matematicas", susp_mat), ("Física", susp_fis), ("Inglés", susp_ing)]
    max_susp = max(suspensos, key=lambda x: x[1])
    print("\n=== Asignatura con más suspensos ===")
    print(f"{max_susp[0]}: {max_susp[1]}")

    # 7. Total de notables o sobresalientes por alumno (notas >= 7)
    notables = todas.groupByKey().mapValues(lambda notas: sum(1 for n in notas if n[1] >= 7))
    print("\n=== Notables/sobresalientes por alumno (notas >= 7) ===")
    for alumno, total in notables.collect():
        print(f"{alumno}: {total}")

    # 8. ¿Qué alumno no se ha presentado a inglés?
    alumnos_todas = todas.map(lambda x: x[0]).distinct()
    alumnos_ingles = ingles.map(lambda x: x[0]).distinct()
    no_ingles = alumnos_todas.subtract(alumnos_ingles)
    print("\n=== Alumnos que no se han presentado a inglés ===")
    for alumno in no_ingles.collect():
        print(alumno)

    # 9. ¿A cuántas asignaturas se ha presentado cada alumno?
    asignaturas_por_alumno = todas.groupByKey().mapValues(lambda notas: len(notas))
    print("\n=== Asignaturas presentadas por alumno ===")
    for alumno, cantidad in asignaturas_por_alumno.collect():
        print(f"{alumno}: {cantidad}")

    # 10. RDD con cada alumno y sus notas
    alumno_notas = todas.groupByKey().mapValues(list)
    print("\n=== Alumno con sus notas ===")
    for alumno, notas in alumno_notas.collect():
        notas_str = ", ".join([f"{asig}: {nota}" for asig, nota in notas])
        print(f"{alumno}: {notas_str}")

    spark.stop()

if __name__ == "__main__":
    main()
