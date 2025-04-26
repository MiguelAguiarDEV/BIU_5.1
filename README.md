# Comandos para gestionar Spark en Docker

El siguiente listado describe cada comando y su función:

<!-- Elimina el contenedor y la imagen personalizada de Spark si existen -->

```bash
docker rm -f spark-master-custom && docker rmi spark-custom:3.3.2
```

# 1) (Opcional) Eliminar la red si ya existiera
docker network rm spark-network

# 2) Crear la red para Spark
docker network create spark-network

# 3) Detener y eliminar cualquier contenedor spark-master-custom previo
docker stop spark-master-custom && docker rm spark-master-custom

# 4) (Manual) Edita tu Dockerfile: cambia
#    FROM openjdk:25-jdk-slim
#    por
#    FROM openjdk:17-jdk-slim

# 5) Construir la nueva imagen con Java 17
docker build -t spark-custom:3.3.2 .

# 6) Levantar el contenedor maestro
docker run -d \
  --name spark-master-custom \
  --network spark-network \
  -p 8080:8080 \
  -p 7077:7077 \
  -v "${PWD}:/opt/spark/data" \
  spark-custom:3.3.2 \
  tail -f /dev/null

# 7) Instalar el binario `nice` (util-linux) dentro del contenedor
docker exec spark-master-custom apt-get update
docker exec spark-master-custom apt-get install -y util-linux

# 8) Arrancar el Master de Spark “a mano” (sin usar nice)
docker exec -d spark-master-custom bash -c "\
  /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master \
    --host 0.0.0.0 --port 7077 --webui-port 8080\
"

# 9) Enviar tu script Euclid a Spark
docker exec spark-master-custom \
  /opt/spark/bin/spark-submit --master local[*] data/euclid.py

# Ejemplo de red y ejecución conjunta

# Crear red Docker
docker network create spark-hadoop-net

# Levantar Hadoop
docker build -t hadoop-custom:3.3.2 ./hadoop-docker
docker run -d --name hadoop-namenode --network spark-hadoop-net hadoop-custom:3.3.2

# Inicializar HDFS (solo la primera vez)
docker exec -it hadoop-namenode bash -c "/opt/hadoop/bin/hdfs namenode -format"
docker exec -d hadoop-namenode bash -c "/opt/hadoop/sbin/start-dfs.sh"

# Levantar Spark conectado a la misma red
docker build -t spark-custom:3.3.2 ./spark-docker
docker run -d --name spark-master-custom --network spark-hadoop-net spark-custom:3.3.2 tail -f /dev/null

# Ejecutar el script de Spark
docker exec -it spark-master-custom bash -c "/opt/spark/bin/spark-submit quijote_word_count.py"
