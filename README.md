# Guía de Instalación — Análisis Taxis NYC con Zeppelin + Spark + Docker

## Opción rápida — Clonar el repositorio

Si clonas el repositorio Git del proyecto, puedes saltarte los pasos 2 y 3 de esta guía (estructura de carpetas y archivos de configuración) ya que el repositorio los incluye todos.

```powershell
git clone https://github.com/paabloo15/big-data-zeppelin-spark-taxi-analysis.git
cd big-data-zeppelin-spark-taxi-analysis
```

Después de clonar solo necesitas añadir los archivos de datos en la carpeta `./data` (si falta alguno) y continuar desde el **paso 4**.

> Si no clonas el repositorio, sigue la guía completa desde el paso 1.

---

## Requisitos previos

Antes de empezar necesitas tener instalado en tu máquina Windows:

- **Docker Desktop** — https://www.docker.com/products/docker-desktop
- **Git** (opcional, para clonar el proyecto) — https://git-scm.com
- **VS Code** (recomendado para editar archivos) — https://code.visualstudio.com

---

## 1. Configurar Docker Desktop

Una vez instalado Docker Desktop:

1. Abre Docker Desktop
2. Ve a **Settings → General** y asegúrate de que **"Use the WSL 2 based engine"** está activado
3. Haz clic en **Apply & Restart**

Verifica que Docker funciona abriendo PowerShell y ejecutando:
```powershell
docker version
```
Debes ver la versión del cliente y del servidor sin errores.

---

## 2. Estructura del proyecto

El proyecto debe tener esta estructura de carpetas:

```
big-data-zeppelin-spark-taxi-analysis/
├── data/                         ← Dataset y archivos de salida
│   ├── yellow_tripdata_2025-01.parquet
│   ├── taxi_zone_lookup.csv
│   ├── taxi_zones.shp
│   ├── taxi_zones.dbf
│   ├── taxi_zones.prj
│   ├── taxi_zones.shx
│   ├── taxi_zones.cpg
│   └── nyc_taxi_zones.geojson    ← se genera en el paso 5
├── notebooks/                    ← los notebooks de Zeppelin
├── logs/                         ← logs de Zeppelin
├── Dockerfile
└── docker-compose.yml
```

Crea las carpetas que no existan:
```powershell
mkdir data, notebooks, logs
```

---

## 3. Archivos de configuración

### docker-compose.yml

Crea el archivo `docker-compose.yml` en la raíz del proyecto con este contenido:

```yaml
services:
  zeppelin:
    build: .
    container_name: zeppelin
    ports:
      - "8080:8080"
    environment:
      ZEPPELIN_ADDR: 0.0.0.0
      SPARK_HOME: /opt/spark
      SPARK_MASTER: spark://spark-master:7077
    volumes:
      - ./notebooks:/zeppelin/notebook
      - ./data:/data
      - ./logs:/zeppelin/logs
      - spark_binaries:/opt/spark
    depends_on:
      - spark-master
    networks:
      - zeppelin-net

  spark-master:
    image: apache/spark:3.5.1
    container_name: spark-master
    command: /opt/spark/bin/spark-class org.apache.spark.deploy.master.Master
    ports:
      - "7077:7077"
      - "8081:8080"
    volumes:
      - spark_binaries:/opt/spark
    networks:
      - zeppelin-net

  spark-worker-1:
    image: apache/spark:3.5.1
    container_name: spark-worker-1
    command: /opt/spark/bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077
    environment:
      SPARK_WORKER_MEMORY: 3g
      SPARK_WORKER_CORES: 2
    volumes:
      - ./data:/data
    depends_on:
      - spark-master
    networks:
      - zeppelin-net

volumes:
  spark_binaries:

networks:
  zeppelin-net:
    driver: bridge
```

### Dockerfile

Crea el archivo `Dockerfile` en la raíz del proyecto:

```dockerfile
FROM apache/zeppelin:0.11.1
USER root
RUN find /opt/zeppelin/interpreter -name '._*' -delete
```

---

## 4. Arrancar el cluster

Abre PowerShell en la carpeta del proyecto y ejecuta:

```powershell
docker-compose up -d
```

La primera vez tardará varios minutos mientras descarga las imágenes. Verifica que los 3 contenedores están corriendo:

```powershell
docker ps
```

Debes ver `zeppelin`, `spark-master` y `spark-worker-1` con estado `Up`.

---

## 5. Generar el GeoJSON de zonas

Copia los archivos del shapefile de zonas (`.shp`, `.dbf`, `.prj`, `.shx`, `.cpg`) a la carpeta `./data`.

Instala las dependencias Python necesarias:

```powershell
docker exec -u root -it zeppelin bash -c "/opt/conda/envs/python_3_with_R/bin/pip install geopandas pyogrio"
```

Instala las dependencias de numpy:

```powershell
docker exec -u root -it zeppelin bash -c "/opt/conda/envs/python_3_with_R/bin/pip install 'numpy<2' pyarrow folium"
```

Crea el archivo `convert.py` en tu carpeta `./data` con este contenido:

```python
import geopandas as gpd
import pandas as pd

gdf = gpd.read_file('/data/taxi_zones.shp')
gdf = gdf.to_crs(epsg=4326)

lookup = pd.read_csv('/data/taxi_zone_lookup.csv')
gdf = gdf.merge(lookup[['LocationID', 'service_zone']], on='LocationID', how='left')

gdf.to_file('/data/nyc_taxi_zones.geojson', driver='GeoJSON')
print('GeoJSON generado correctamente')
print(gdf.columns.tolist())
```

Ejecútalo:

```powershell
docker exec -u root -it zeppelin bash -c "/opt/conda/envs/python_3_with_R/bin/python3 /data/convert.py"
```

Verás el mensaje `GeoJSON generado correctamente` al finalizar.

---

## 6. Configurar el intérprete Spark en Zeppelin

1. Abre el navegador y ve a **http://localhost:8080**
2. Haz clic en tu usuario (arriba derecha) → **Interpreter**
3. Busca `spark` y haz clic en **Edit**
4. Configura estas propiedades:

| Propiedad | Valor |
|---|---|
| `master` | `spark://spark-master:7077` |
| `SPARK_HOME` | `/opt/spark` |
| `spark.executor.memory` | `2g` |
| `spark.driver.memory` | `1g` |
| `spark.executor.cores` | `2` |

5. Haz clic en **Save** y luego en **Restart**

---

## 7. Ejecutar los notebooks

1. En Zeppelin haz clic en **Import note**
2. Ejecuta las celdas **en orden**, empezando siempre por la **Celda 1** que carga y preprocesa los datos
3. Verifica que la Celda 1 termina con el mensaje `Total registros: XXXXXXX`

> **Importante:** Cada vez que reinicias los contenedores hay que volver a ejecutar la Celda 1 para recrear el DataFrame `dfFinal` en memoria.

---

## 8. Accesos útiles

| Servicio | URL |
|---|---|
| Zeppelin (notebooks) | http://localhost:8080 |
| Spark Master UI | http://localhost:8081 |

---

## 9. Comandos útiles

**Arrancar el cluster:**
```powershell
docker-compose up -d
```

**Parar el cluster:**
```powershell
docker-compose down
```

**Reiniciar solo Zeppelin:**
```powershell
docker restart zeppelin
```

**Limpiar archivos basura (ejecutar tras cada reinicio si es necesario):**
```powershell
docker exec -u root -it zeppelin bash -c "find /opt/zeppelin/interpreter -name '._*' -delete"
```

---

## 10. Solución de problemas frecuentes

### Zeppelin no arranca
Comprueba los logs con `docker logs zeppelin`. Si ves `exec /usr/bin/tini: no such file or directory`, reconstruye la imagen:
```powershell
docker-compose down
docker rmi big-data-zeppelin-spark-taxi-analysis-zeppelin
docker builder prune -f
docker-compose up -d --build
```

### El intérprete Spark da error de conexión
Verifica que los 3 contenedores están corriendo con `docker ps`. Si falta alguno, ejecuta `docker-compose up -d` de nuevo.

### Error "dfFinal not found"
El intérprete se reinició y perdió el DataFrame. Vuelve a ejecutar la Celda 1 del notebook.

### Los mapas no se generan
Verifica que folium está instalado:
```powershell
docker exec -u root -it zeppelin bash -c "/opt/conda/envs/python_3_with_R/bin/pip install folium"
```
Y reinicia el intérprete Python en Zeppelin → Interpreter → python → Restart.

### Puerto 8080 ocupado
Cambia el mapeo en `docker-compose.yml`:
```yaml
ports:
  - "8888:8080"
```
Y accede por `http://localhost:8888`.
