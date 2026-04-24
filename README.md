# Analisis escalable de movilidad urbana con Apache Spark y Apache Zeppelin usando datos masivos de taxis de Nueva York

## 1. Descripcion del proyecto
Este repositorio contiene una base tecnica para un proyecto universitario de Big Data orientado al analisis historico de viajes de taxi en Nueva York (NYC TLC Trip Record Data, Yellow Taxi).

El objetivo no es generar una memoria final automatica, sino disponer de:
- infraestructura local reproducible;
- scripts claros para descarga, limpieza y analitica;
- guiones de notebooks para Zeppelin;
- documentacion tecnica defendible.

## 2. Objetivos
### Objetivo general
Construir un flujo Big Data local, escalable y defendible, basado en Spark y Zeppelin para procesar y analizar datos masivos de movilidad urbana.

### Objetivos especificos
- Descargar datos en formato Parquet desde la fuente oficial de NYC TLC.
- Aplicar limpieza de datos con reglas explicitas y trazables.
- Crear columnas derivadas utiles para analisis temporal y economico.
- Ejecutar consultas analiticas con DataFrames y Spark SQL.
- Comparar de forma didactica el rendimiento de Parquet vs CSV.
- Organizar una demo final rapida para defensa academica.

## 3. Tecnologias utilizadas
- Apache Spark (procesamiento distribuido con DataFrames y Spark SQL).
- Apache Zeppelin (exploracion, visualizacion y narrativa analitica).
- Python y PySpark (scripts ETL y benchmarking).
- Docker Compose (despliegue local simple).
- Formato Parquet (almacenamiento columnar eficiente para analitica).

## 4. Arquitectura general
Arquitectura principal (simple y defendible):
1. Un contenedor de Zeppelin con interprete Spark en modo local (`local[*]`).
2. Volumenes compartidos para datos, scripts, notebooks y resultados.
3. Scripts Python/PySpark ejecutados dentro del contenedor con `spark-submit`.

Flujo funcional:
1. Descarga de Parquet en `data/raw/`.
2. Limpieza y transformacion en Spark.
3. Salida limpia en `data/processed/clean_taxi_trips.parquet`.
4. Muestra CSV para comparativa en `data/processed/sample_taxi_trips.csv`.
5. Metricas de benchmark en `results/metricas_consultas.csv`.
6. Analisis y graficos en Zeppelin usando los guiones de `notebooks/`.

## 5. Dataset utilizado
Fuente oficial:
- NYC Taxi and Limousine Commission (TLC) Trip Record Data.
- Endpoint usado para ficheros Yellow Taxi Parquet:
  - `https://d37ci6vzurychx.cloudfront.net/trip-data/`

Columnas clave del analisis:
- `tpep_pickup_datetime`
- `tpep_dropoff_datetime`
- `passenger_count`
- `trip_distance`
- `PULocationID`
- `DOLocationID`
- `payment_type`
- `fare_amount`
- `tip_amount`
- `total_amount`
- `VendorID`
- `RatecodeID`

Archivo auxiliar opcional:
- `taxi_zone_lookup.csv` para mapear `LocationID` a `borough`, `zone`, `service_zone`.
- TODO: descargar manualmente y guardar en `data/lookup/taxi_zone_lookup.csv`.

## 6. Estructura del repositorio
```text
big-data-zeppelin-spark-taxi-analysis/
├── README.md
├── docker-compose.yml
├── .gitignore
├── requirements.txt
├── data/
│   ├── raw/
│   ├── processed/
│   └── lookup/
├── notebooks/
├── scripts/
├── docs/
├── figures/
└── results/
```

## 7. Instalacion y arranque
### Requisitos previos
- Docker Desktop + Docker Compose v2.
- Espacio en disco suficiente (varios GB segun meses descargados).
- Opcion A (recomendada): ejecutar scripts dentro del contenedor Zeppelin.
- Opcion B (local): Python 3.10+ y Java 11/17 para PySpark.

### Arranque rapido
Desde la raiz del proyecto:
```bash
docker compose up -d
```

Ver estado:
```bash
docker compose ps
```

Parar servicios:
```bash
docker compose down
```

## 8. Ejecucion del pipeline (paso a paso)
### Paso 1: Descargar datos
Ejemplo (enero-marzo 2023):
```bash
docker compose exec zeppelin python /opt/project/scripts/download_data.py --year 2023 --months 1 2 3
```

### Paso 2: Limpiar y transformar con Spark
```bash
docker compose exec zeppelin spark-submit /opt/project/scripts/prepare_data.py --max-duration-minutes 240 --max-speed-mph 80
```

### Paso 3: Exportar muestra CSV para comparativa
```bash
docker compose exec zeppelin spark-submit /opt/project/scripts/convert_sample_to_csv.py --sample-ratio 0.05 --sample-size 200000
```

### Paso 4: Ejecutar benchmark didactico
```bash
docker compose exec zeppelin spark-submit /opt/project/scripts/benchmark_queries.py
```

## 9. Abrir Zeppelin y usar notebooks
- URL: `http://localhost:8080`
- Los archivos de `notebooks/*.md` son guiones orientativos para copiar/adaptar en notebooks reales de Zeppelin.
- TODO: importar o recrear notebooks reales en Zeppelin segun el guion.

Orden sugerido de ejecucion:
1. `01_carga_datos.md`
2. `02_limpieza_transformacion.md`
3. `03_analisis_temporal.md`
4. `04_analisis_geografico_economico.md`
5. `05_comparativa_rendimiento.md`
6. `06_dashboard_final.md`

## 10. Resultados esperados (pendiente de ejecutar)
No se incluyen resultados inventados. Se espera generar, tras ejecutar en local:
- `results/resumen_limpieza.csv`
- `results/metricas_consultas.csv`
- Graficos en Zeppelin (viajes por hora, coste medio por hora, zonas top, etc.)

Etiqueta recomendada para entregables temporales:
- `ejemplo`
- `pendiente de ejecutar`

## 11. Que no se sube al repositorio
- Datasets masivos descargados (`data/raw/*.parquet`).
- Salidas pesadas de procesamiento (`data/processed/*.parquet`, `data/processed/*.csv`).
- Resultados generados en ejecucion (`results/*.csv`, salvo ejemplos pequenos si se acuerda).
- Artefactos temporales y caches.

## 12. Problemas frecuentes
1. Puerto 8080 ocupado.
- Cambiar el mapeo en `docker-compose.yml` (por ejemplo `18080:8080`).

2. Memoria insuficiente al procesar muchos meses.
- Reducir meses analizados.
- Aumentar memoria de Docker Desktop.
- Ajustar limites en scripts (muestra, particiones, etc.).

3. Error al leer CSV de muestra.
- Verificar que se ejecuto `convert_sample_to_csv.py` antes del benchmark.

4. Diferencias de rendimiento poco claras.
- Usar mismo tamano de muestra.
- Repetir consultas varias veces y comentar sesgos de cache.

## 13. Puntos clave para defensa tecnica
- Por que Spark: procesamiento distribuido, API DataFrame y Spark SQL para escalar analitica.
- Por que Zeppelin: cuaderno colaborativo para codigo, consultas y visualizaciones en una sola herramienta.
- Por que Parquet: formato columnar comprimido, lectura selectiva de columnas y mejor rendimiento analitico.
- Que es DataFrame: abstraccion tabular distribuida con optimizacion interna (Catalyst/Tungsten).
- Que aporta Spark SQL: consultas declarativas y optimizadas sobre datos distribuidos.
- Que limpieza se aplica: reglas sobre fechas, duracion, distancia, importes y velocidad.
- Limitaciones en local: recursos limitados, no hay cluster real ni tolerancia completa a fallos.
- Escalado futuro: migrar a cluster Spark real (Standalone/YARN/Kubernetes), almacenamiento distribuido y orquestacion.

## 14. TODOs de intervencion manual
- TODO: descargar `taxi_zone_lookup.csv` y guardarlo en `data/lookup/`.
- TODO: ajustar anios y meses de analisis para la entrega final.
- TODO: importar o recrear notebooks reales en Zeppelin.
- TODO: anadir capturas y tablas reales en la memoria/presentacion.
- TODO: validar resultados en el entorno local del grupo.

## 15. Creditos y declaracion de uso academico
Proyecto desarrollado con fines docentes para la asignatura Complementos de Bases de Datos.

El uso de IA se ha realizado como apoyo tecnico para:
- ideacion de estructura;
- asistencia en scripts y documentacion;
- revision conceptual.

Todo contenido debe ser revisado, comprendido y adaptado por el equipo antes de su entrega.
