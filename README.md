
# 1. Algoritmo de Euclides

El algoritmo de Euclides es un método clásico y muy eficiente para calcular el **máximo común divisor (MCD)** de dos números enteros positivos. Se basa en la siguiente propiedad fundamental:

> **Propiedad.** Para $a, b \in \mathbb{Z}^+$ con $a \ge b$:

> $$
> \gcd(a, b) = \gcd\bigl(b,\,a \bmod b\bigr).
> $$

Iterando este paso (reemplazando $(a, b)$ por $(b,\,a \bmod b)$) hasta que el segundo término sea cero, el primer término restante es el MCD.

---

## ¿Para qué puede usarse?

- **Simplificación de fracciones.** Para reducir $\frac{a}{b}$ a su forma irreducible dividiendo numerador y denominador por $\gcd(a,b)$.
- **Criptografía.** En algoritmos como RSA, para calcular inversos modulares y en pruebas de primalidad.
- **Ecuaciones diofánticas lineales.** Para resolver $ax + by = c$ sólo si $\gcd(a,b)\mid c$.
- **Geometría computacional y gráficos.** Para determinar pasos enteros de un segmento de recta o en rasterización (algoritmo de Bresenham).
- **Teoría de números y análisis algorítmico.** Sirve de bloque básico en muchos teoremas y algoritmos que manipulan divisores.

---

## Ejemplo de ejecución en notación matemática

Calculemos $\gcd(48,18)$ paso a paso:

```latex
\begin{aligned}
48 &= 18 \times 2 \; + \; 12,      &\quad&\gcd(48,18) = \gcd(18,12)\\
18 &= 12 \times 1 \; + \; 6,       &\quad&\gcd(18,12) = \gcd(12,6)\\
12 &= 6  \times 2 \; + \; 0,       &\quad&\gcd(12,6) = 6
\end{aligned}
```

Como el resto llega a cero, el **MCD** es el último divisor distinto de cero:

$$
\boxed{\gcd(48,18) = 6}.
$$

---

## Comandos en `spark-docker`

Dentro del directorio `spark-docker`, ejecuta los siguientes comandos:

1. **Crear la red para Spark:**
   ```bash
   docker network create spark-network
   ```
2. **Construir la imagen personalizada:**
   ```bash
   docker build -t spark-custom:3.3.2 .
   ```
3. **Iniciar el contenedor maestro:**
   ```bash
   docker run -d --name spark-master-custom --network spark-network \
     -p 8080:8080 -p 7077:7077 \
     -v "${PWD}:/opt/spark/data" \
     spark-custom:3.3.2 tail -f /dev/null
   ```
4. **Arrancar el Master manualmente:**
   ```bash
   docker exec -d spark-master-custom bash -c "/opt/spark/bin/spark-class \
     org.apache.spark.deploy.master.Master --host 0.0.0.0 --port 7077 \
     --webui-port 8080"
   ```
5. **Ejecutar el script Euclid y filtrar resultados:**
   ```bash
   docker exec spark-master-custom bash -c "/opt/spark/bin/spark-submit \
     --master local[*] data/euclid.py 2>&1 | grep '^gcd'"
   ```

![[Pasted image 20250426015627.png]]

![[Pasted image 20250426015638.png]]

# 2. 

## 2.1. Ejecución movies_each_average

   ```bash
docker exec spark-master-custom bash -c "/opt/spark/bin/spark-submit --master local[*] data/movies_each_average.py 2>/dev/null"
   ```

Nota media de todas las votaciones de cada película. 
![[Pasted image 20250426020803.png]]

## 2.2 Ejecución  average_movie_mark

   ```bash
docker exec spark-master-custom bash -c "/opt/spark/bin/spark-submit --master local[*] data/average_movie_mark.py 2>/dev/null"
   ```
Notas medias superiores a 3
![[Pasted image 20250426021104.png]]

# 3.

```bash
docker exec spark-master-custom bash -c '/opt/spark/bin/spark-submit --master local[*] data/mapreduce.py'
```

![[Pasted image 20250426023011.png]]

# 4.

```bash
docker exec spark-master-custom bash -c "/opt/spark/bin/spark-submit --master local[*] data/movies_rdd.py"
```

![[Pasted image 20250426025133.png]]
Muestra muchas películas porque hay pocas o ninguna con menos de 4 letras en el nombre.
Aquí una prueba cambiando 4 por 10
![[Pasted image 20250426025448.png]]

# 5.
## 5.1

```bash
docker exec spark-master-custom bash -c "/opt/spark/bin/spark-submit --master local[*] data/quijote_all_words_list.py"
```
Lista de todas las palabras:
![[Pasted image 20250426030534.png]]

*Extras*
Total de palabras + 50 primeras palabras:
![[Pasted image 20250426030621.png]]

## 5.2

```bash
docker exec spark-master-custom bash -c "/opt/spark/bin/spark-submit --master local[*] data/quijote_word_count.py dichoso"  #Puedes cambiar la palabra
```

![[Pasted image 20250426030958.png]]

## 5.3

Dentro de la carpeta 'hadoop-docker'
1. Construir la imagen de Hadoop
```bash
docker build -t hadoop-custom:3.3.2 .
```

2. Iniciar el contenedor de Hadoop
```bash
docker run -d --name hadoop-namenode --network spark-network hadoop-custom:3.3.2 tail -f /dev/null
```

3. Formatear el NameNode (solo la primera vez)
```bash
docker exec -it hadoop-namenode bash -c "/opt/hadoop/bin/hdfs namenode -format"
```

4. Acceder al contenedor para iniciar los servicios manualmente
```bash
docker exec -it hadoop-namenode bash
```

5. Dentro del contenedor, ejecutar:

```bash
export HDFS_NAMENODE_USER=root
export HDFS_DATANODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
/opt/hadoop/sbin/hadoop-daemon.sh start namenode
/opt/hadoop/sbin/hadoop-daemon.sh start datanode
/opt/hadoop/sbin/hadoop-daemon.sh start secondarynamenode
```

6. (Opcional) Verificar HDFS dentro del contenedor
```bash
/opt/hadoop/bin/hdfs dfs -ls /
```

7. Salir del contenedor Hadoop
```bash
exit
```

8. Ejecutar el script de Spark para guardar el resultado en HDFS
```bash
docker exec -it spark-master-custom bash -c "/opt/spark/bin/spark-submit data/quijote_wordcount_to_hdfs.py"
```

9. Comprobar el resultado en HDFS

```bash
docker exec -it hadoop-namenode bash -c "/opt/hadoop/bin/hdfs dfs -ls /quijote_wordcount"

docker exec -it hadoop-namenode bash -c "/opt/hadoop/bin/hdfs dfs -cat /quijote_wordcount/part-* | head"
```

![[Pasted image 20250426035026.png]]


# 6.

```bash
docker exec -it spark-master-custom bash -c "/opt/spark/bin/spark-submit data/numbers_task.py"
```

![[Pasted image 20250426035942.png]]

# 7. 

```bash
docker exec -it spark-master-custom bash -c "/opt/spark/bin/spark-submit data/words_rdd_tasks.py"
```

![[Pasted image 20250426040206.png]]

# 8. 

```bash
docker exec -it spark-master-custom bash -c "/opt/spark/bin/spark-submit data/names_rdd_tasks.py"
```

![[Pasted image 20250426041515.png]]

# 9.

```bash
 docker exec -it spark-master-custom bash -c "/opt/spark/bin/spark-submit data/marks_rdd_tasks.py"
```
![[Pasted image 20250426042348.png]]
![[Pasted image 20250426042400.png]]
![[Pasted image 20250426042408.png]]
![[Pasted image 20250426042419.png]]
![[Pasted image 20250426042427.png]]
![[Pasted image 20250426042434.png]]
![[Pasted image 20250426042442.png]]
![[Pasted image 20250426042455.png]]
![[Pasted image 20250426042502.png]]
![[Pasted image 20250426042508.png]]
